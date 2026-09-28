package com.example.agentzy;

import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.UserMessage;

/**
 * 示例 2：工具调用（Function Calling）——让 LLM 从"会说话"变成"会做事"。
 *
 * <p>这里演示：LLM 自己决定调用哪个工具、传什么参数，再根据工具返回值组织最终回答。
 *
 * <p>运行：
 * <pre>
 *   mvn -q compile exec:java -Dexec.mainClass=com.example.agentzy.ToolCallingExample
 * </pre>
 */
public final class ToolCallingExample {

    private ToolCallingExample() {
    }

    /** 声明式助手接口：LangChain4j 会在运行时生成实现。 */
    interface Assistant {
        String chat(@UserMessage String message);
    }

    /** 一组可被 LLM 调用的工具。 */
    static class DemoTools {

        @Tool("计算两个整数相加，返回结果")
        int add(int a, int b) {
            System.out.println("  [工具调用] add(" + a + ", " + b + ")");
            return a + b;
        }

        @Tool("查询指定城市的当前天气（演示用模拟数据）")
        String weather(String city) {
            System.out.println("  [工具调用] weather(" + city + ")");
            return city + "：晴，25℃，微风";
        }
    }

    public static void main(String[] args) {
        Assistant assistant = AiServices.builder(Assistant.class)
                .chatModel(ChatModels.deepSeek())
                .tools(new DemoTools())
                .build();

        String question = args.length > 0
                ? String.join(" ", args)
                : "北京今天天气怎么样？另外帮我算一下 123 + 456 等于多少。";

        System.out.println("提问：" + question);
        System.out.println("回复：" + assistant.chat(question));
    }
}
