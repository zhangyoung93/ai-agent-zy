package com.example.agentzy;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;

/**
 * 构建指向 DeepSeek 的 ChatModel。
 *
 * <p>DeepSeek 兼容 OpenAI 协议，所以直接复用 LangChain4j 的 OpenAI 集成，
 * 只把 baseUrl 指向 DeepSeek 即可。
 */
public final class ChatModels {

    private ChatModels() {
    }

    public static ChatModel deepSeek() {
        return OpenAiChatModel.builder()
                .baseUrl(AppConfig.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"))
                .apiKey(AppConfig.require("DEEPSEEK_API_KEY"))
                .modelName(AppConfig.get("DEEPSEEK_MODEL", "deepseek-chat"))
                .temperature(0.7)
                // 打印原始请求/响应，便于学习时观察协议细节
                .logRequests(true)
                .logResponses(true)
                .build();
    }
}
