# Activate Panel in this notebook
pn.extension()
```

## Step 2: Import Panel and Define Widgets

Create a text input and a button. The text input will display the click count.

```python theme={null}
# TextInput widget initialized with a default message
text_input = pn.widgets.TextInput(value='Ready')

# Button widget with a primary style
button = pn.widgets.Button(name='Click me', button_type='primary')
```

## Step 3: Create an Event Handler

Define a callback function to update the text input whenever the button is clicked:

```python theme={null}
def increment_clicks(event):
    """Update the text_input value based on button.clicks."""
    text_input.value = f'Clicked {button.clicks} times'

# Register the handler
button.on_click(increment_clicks)
```

## Step 4: Display Widgets in a Layout

Arrange the button and text input side by side using `pn.Row`:

```python theme={null}
# Render the widgets in a single row
pn.Row(button, text_input)
```

After running the cell above, you’ll see:

* A **Click me** button
* A text box initially showing **Ready**

Each click updates the text box to reflect the total number of clicks, demonstrating a simple interactive interface.

## Widget Reference Table

| Widget    | Purpose                            | Key Property            |
| --------- | ---------------------------------- | ----------------------- |
| TextInput | Display and update dynamic text    | `value='Ready'`         |
| Button    | Capture and respond to user clicks | `button_type='primary'` |

## Additional Resources

* Panel Documentation: [https://panel.holoviz.org/](https://panel.holoviz.org/)
* JupyterLab: [https://jupyterlab.readthedocs.io/](https://jupyterlab.readthedocs.io/)

Build on this pattern to create dashboards, data explorers, and more within your Jupyter environment!

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/e92757cb-5675-4502-a171-1319ab63937b)


# Word Completion vs Chat Completion

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Building-an-Interactive-Chatbot/Word-Completion-vs-Chat-Completion/page

This article explains the differences between word completion and chat completion in OpenAIs GPT-3.5 Turbo model.

Before integrating a chatbot into your application, it’s essential to understand the difference between **word completion** and **chat completion**. Although both use the same underlying GPT-3.5-Turbo model, their usage patterns—and the way they manage context—are very different.

## What Is Word Completion?

Word completion is a **stateless** API call. You send a single prompt, and the model returns a continuation without retaining any memory of previous interactions.

Key characteristics:

* Single-shot responses
* No conversation history
* Simpler, lower token usage

![The image compares "Word Completion" and "Chat Completion," highlighting that word completion doesn't need memory, while chat completion expects context from previous conversations.](https://kodekloud.com/kk-media/image/upload/v1752881500/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Word-Completion-vs-Chat-Completion/word-completion-vs-chat-completion.jpg)

## What Is Chat Completion?

Chat completion is **stateful**. You maintain a record of all messages in a `messages` array, allowing the model to build on past user and assistant exchanges.

### How Chat Completion Works

1. You create an ordered `messages` list.
2. Each entry has a `role`: **system**, **user**, or **assistant**.
3. You submit the full history each time you call the API.
4. The model returns a response that accounts for all previous context.

### Roles in the `messages` Array

| Role      | Description                                                      | Example                                                          |
| --------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| system    | Sets global instructions or persona                              | “You are a physics professor.”                                   |
| user      | Represents the human’s input at each turn                        | “Explain quantum mechanics in simple terms.”                     |
| assistant | Model-generated responses that continue the conversation context | “Quantum mechanics is the study of matter at very small scales…” |

![The image illustrates the difference between word completion and chat completion, showing a user interacting with a system and an LLM (Large Language Model) using chat history as a message parameter.](https://kodekloud.com/kk-media/image/upload/v1752881501/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Word-Completion-vs-Chat-Completion/word-completion-vs-chat-completion-llm.jpg)

> **lightbulb** * Use **word completion** for simple text continuations, code generation, or single-turn tasks.
  * Use **chat completion** for multi-turn conversations, contextual assistants, and applications that require stateful interaction.

## Sample Chat Completion Request

```json theme={null}
POST https://api.openai.com/v1/chat/completions
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "model": "gpt-3.5-turbo",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user",   "content": "Explain photosynthesis." }
  ]
}
```

## Comparison at a Glance

| Feature           | Word Completion       | Chat Completion                  |
| ----------------- | --------------------- | -------------------------------- |
| Context Handling  | Stateless             | Stateful via `messages` array    |
| Best for          | Single-turn prompts   | Multi-turn conversations         |
| Token Efficiency  | Fewer overhead tokens | More overhead tokens for history |
| Recommended Model | GPT-3.5-Turbo         | GPT-3.5-Turbo                    |

## Further Reading and References

* [OpenAI Chat Completion API Reference](https://platform.openai.com/docs/guides/chat)
* [OpenAI Completion API Reference](https://platform.openai.com/docs/api-reference/completions)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/e97354a8-5b4c-44a6-b50b-4c5d38d8b729)
