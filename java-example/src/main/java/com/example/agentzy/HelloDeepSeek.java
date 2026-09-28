package com.example.agentzy;

import dev.langchain4j.model.chat.ChatModel;

/**
 * 示例 1：最基础的一次对话。
 *
 * <p>运行：
 * <pre>
 *   mvn -q compile exec:java -Dexec.mainClass=com.example.agentzy.HelloDeepSeek
 * </pre>
 */
public final class HelloDeepSeek {

    private HelloDeepSeek() {
    }

    public static void main(String[] args) {
        String prompt = args.length > 0
                ? String.join(" ", args)
                : "用一句话解释：什么是 AI Agent？";

        ChatModel model = ChatModels.deepSeek();

        System.out.println("提问：" + prompt);
        System.out.println("回复：" + model.chat(prompt));
    }
}
