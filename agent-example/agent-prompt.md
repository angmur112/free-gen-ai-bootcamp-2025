# ReAct Prompt Engineering with Tool Use

## Overview

ReAct (Reasoning and Acting) is a prompt engineering technique that enhances AI agents by enabling them to reason about tasks and take actions using external tools. This approach combines chain-of-thought reasoning with task-specific actions, leading to more informed and accurate decision-making.

## Components of a ReAct Prompt

A ReAct prompt typically includes the following components:

1.  **Observation:** The agent perceives the current state or input.
2.  **Reasoning:** The agent analyzes the observation and plans the next course of action.
3.  **Action:** The agent executes an action, which may involve using a tool or providing a response.

## Example

Here's an example of a ReAct prompt for answering a question using a search engine:

**User Input:** What is the capital of France?

**Agent Process:**

1.  **Observation:** The user is asking a question about the capital of France.
2.  **Reasoning:** To answer this question, I need to find the capital of France. I can use a search engine to find this information.
3.  **Action:**
    *Tool Call:* `search("capital of France")`

The search engine returns the following result: "Paris is the capital of France."

4.  **Final Answer:** The capital of France is Paris.

## Tool Integration

To effectively use ReAct, the AI agent needs to be integrated with external tools. This involves defining the available tools and their corresponding functions. For example, a search engine tool might have a `search(query)` function that takes a search query as input and returns the search results.

When designing ReAct prompts, it's important to clearly specify how the agent should use the available tools. This includes providing instructions on when to use each tool and how to interpret the tool's output.

## Prompt Template

```
You are an AI assistant with access to the following tools:
- search(query): Search the web for information
- calculator(expression): Perform mathematical calculations
- weather(location): Get current weather for a location

For each user query:
1. Write your observation of the task
2. Think through your reasoning
3. Select and use appropriate tools
4. Provide a final answer

Format your response as:
Observation: [Your observation]
Thought: [Your reasoning]
Action: [Tool name and parameters]
Result: [Tool output]
Answer: [Your final response]
```

## Detailed Example

User: "What will be 15% of today's temperature in London?"

Agent Response:
```
Observation: I need to find the current temperature in London and calculate 15% of it.

Thought: First, I should get the temperature using the weather tool, then use the calculator for the percentage.

Action: weather("London")
Result: Current temperature in London is 20°C

Thought: Now I need to calculate 15% of 20

Action: calculator("20 * 0.15")
Result: 3

Answer: 15% of today's temperature in London (20°C) is 3°C
```

## Best Practices

1. Always follow the observation-thought-action-result pattern
2. Use tools one at a time
3. Chain multiple tools when needed
4. Explain your reasoning clearly
5. Verify tool outputs before providing final answers
