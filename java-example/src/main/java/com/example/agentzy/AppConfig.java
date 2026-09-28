package com.example.agentzy;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 配置读取：优先环境变量，其次 .env 文件。
 *
 * <p>自带一个极简 .env 解析器（零第三方依赖），能容忍 BOM、注释、空行和引号，
 * 与 Python 项目共用项目根目录的 .env。
 *
 * <p>之所以不用 dotenv-java：它遇到 UTF-8 BOM 开头的文件会直接抛
 * {@code DotenvException: Malformed entry}，而记事本等编辑器很容易写出 BOM。
 */
public final class AppConfig {

    private static final Map<String, String> DOTENV = loadDotEnv();

    private AppConfig() {
    }

    /** 读取配置；找不到时返回默认值。 */
    public static String get(String key, String defaultValue) {
        String fromEnv = System.getenv(key);
        if (fromEnv != null && !fromEnv.isBlank()) {
            return fromEnv;
        }
        String fromDotEnv = DOTENV.get(key);
        if (fromDotEnv != null && !fromDotEnv.isBlank()) {
            return fromDotEnv;
        }
        return defaultValue;
    }

    /** 读取必填配置；缺失时抛出清晰可读的错误。 */
    public static String require(String key) {
        String value = get(key, null);
        if (value == null) {
            throw new IllegalStateException(
                    "缺少配置 " + key + "：请设置环境变量，或在项目根目录 .env 中配置（参考 .env.example）");
        }
        return value;
    }

    private static Map<String, String> loadDotEnv() {
        Map<String, String> result = new HashMap<>();
        Path file = locateEnvFile();
        if (file == null) {
            return result;
        }
        try {
            List<String> lines = Files.readAllLines(file, StandardCharsets.UTF_8);
            for (String raw : lines) {
                // 去掉可能存在的 BOM，再忽略空行与注释
                String line = raw.replace("\uFEFF", "").trim();
                if (line.isEmpty() || line.startsWith("#")) {
                    continue;
                }
                int idx = line.indexOf('=');
                if (idx <= 0) {
                    continue; // 非法行直接忽略，不让配置问题拖垮程序
                }
                String key = line.substring(0, idx).trim();
                String value = unquote(line.substring(idx + 1).trim());
                result.put(key, value);
            }
        } catch (IOException e) {
            throw new IllegalStateException("读取 .env 失败：" + file.toAbsolutePath(), e);
        }
        return result;
    }

    private static String unquote(String value) {
        boolean doubleQuoted = value.length() >= 2 && value.startsWith("\"") && value.endsWith("\"");
        boolean singleQuoted = value.length() >= 2 && value.startsWith("'") && value.endsWith("'");
        if (doubleQuoted || singleQuoted) {
            return value.substring(1, value.length() - 1);
        }
        return value;
    }

    /** 依次在本模块目录、项目根目录寻找 .env。 */
    private static Path locateEnvFile() {
        Path local = Path.of(".env");
        if (Files.exists(local)) {
            return local;
        }
        Path parent = Path.of("..", ".env");
        if (Files.exists(parent)) {
            return parent;
        }
        return null;
    }
}
