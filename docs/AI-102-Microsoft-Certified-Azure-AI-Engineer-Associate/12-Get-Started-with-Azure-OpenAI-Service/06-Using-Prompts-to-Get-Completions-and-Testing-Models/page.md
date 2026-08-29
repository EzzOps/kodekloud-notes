# Using Prompts to Get Completions and Testing Models

Source: https://notes.kodekloud.com/docs/AI-102-Microsoft-Certified-Azure-AI-Engineer-Associate/Get-Started-with-Azure-OpenAI-Service/Using-Prompts-to-Get-Completions-and-Testing-Models/page

Guide to designing and testing prompts for generating model completions using Azure OpenAI Studio, with tips and example Python code

Prompts are how we instruct generative models (like GPT) to produce useful output. The model receives your prompt (the instruction or input) and returns a completion (the generated response). Clear, specific prompts lead to more accurate and relevant completions.

Below is a quick reference of common prompt types, example prompts, and the typical completions they produce.

| Prompt type         | Example prompt                             | Typical completion                                                    |
| ------------------- | ------------------------------------------ | --------------------------------------------------------------------- |
| Sentiment analysis  | "The weather is amazing today. Sentiment?" | "Positive"                                                            |
| Generation          | "Write a haiku about the ocean."           | A haiku poem about the ocean                                          |
| Translation         | "English: Hello. Spanish:"                 | "Hola"                                                                |
| Summarization       | "Summarize this article:"                  | A concise summary of the article                                      |
| Text completion     | "To bake a cake, first you need to"        | The continuation with steps or instructions                           |
| Question answering  | "What is the capital of Japan?"            | "Tokyo"                                                               |
| Conversational chat | "Tell me a joke."                          | A joke (e.g., "Why don't skeletons fight? They don't have the guts.") |

<Frame>
  <img alt="A slide titled &#x22;Using Prompts to Get Completions from Models&#x22; showing a three-column table listing tasks, example prompts, and example completions (e.g., sentiment analysis, haiku, translation, summarization, Q&A, and a joke). The table has teal headers on a dark blue background with sample prompt/completion pairs in each row." />
</Frame>

Key prompt-design tips:

* Be explicit about the role and expected format (e.g., “You are a travel planner. Return a 10-day itinerary as numbered days.”).
* Provide examples or constraints (length, tone, style) to guide the model’s output.
* Use system and context messages to control persistent behavior in chat-style interactions.

## Testing prompts in Azure OpenAI Studio (Chat Playground)

Azure OpenAI Studio provides a Chat Playground inside the Azure portal so you can experiment with prompts and deployed models interactively. The playground is ideal for:

* Iterating on prompt wording and role definitions.
* Verifying behavior of base or fine-tuned deployments.
* Generating sample outputs before integrating into an application.

How to use the playground:

* Select your deployment (for example, a GPT-3.5 or GPT-4.5 deployment).
* Enter a system instruction to set the model’s role (e.g., “You are an AI assistant that helps people find information.”).
* Type user prompts in the content box and observe the completion.
* Review chat history to test multi-turn interactions and context retention.
* Try the ready-made sample prompts (travel guides, recipes, code examples) and tweak them to fit your use case.
* Add custom data or test a fine-tuned model to evaluate specialized behavior.

<Frame>
  <img alt="A dark-mode screenshot of the Azure OpenAI &#x22;Chat playground&#x22; interface in a browser window. The UI shows deployment/setup controls on the left and a chat history with a travel itinerary (Day 7–9: Isle of Skye, Fort William, Glencoe & Loch Lomond) in the main pane." />
</Frame>

Example workflow in the playground:

1. Set the system instruction: "You are a travel planner that helps people plan trips."
2. Enter the user prompt: "Plan a 10-day trip to Scotland."
3. Inspect the model's day-by-day itinerary, then refine the system message or user prompt to change style, granularity, or constraints.

> **lightbulb** The playground is a quick way to validate how a fine-tuned model or a deployment responds to your prompts and any additional context before you integrate it into production.

## Example: Chat completion with the OpenAI Python client (Azure)

Below is a concise, working Python example that shows how to create a chat completion against an Azure-hosted model. Update the endpoint, key, and deployment name to match your Azure resource configuration.

```python theme={null}
