# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
```

<Callout icon="triangle-alert">
  Never expose your `OPENAI_API_KEY` in public repositories. Use environment variables or a secrets manager.
</Callout>

***

## 3. Chat Completion Helper

Create a helper function to send messages to the Chat API and return the assistant’s reply:

```python theme={null}
def get_chat_completion(messages):
    """
    Sends a list of messages to OpenAI’s ChatCompletion API
    and returns the assistant’s response text.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content
```

***

## 4. Bot Instructions

Define system-level instructions to guide BurgerBot’s behavior:

```python theme={null}
bot_instructions = """
You are BurgerBot, an automated service to collect orders at Burger Bliss.
1. Greet the customer.
2. Gather the full order; summarize before confirmation.
3. Ask for pickup or delivery (if delivery, request address).
4. Confirm payment details.
5. Clarify menu options with unique item identifiers.
"""
```

***

## 5. Conversation State and Widgets

Initialize the conversation context and Panel widgets:

```python theme={null}
# Starting context with system instructions
context = [{"role": "system", "content": bot_instructions}]

# TextInput widget for user messages
user_input = pn.widgets.TextInput(
    placeholder="Type your message here...", width=400
)

# List to hold UI panels for each message
panels = []
```

***

## 6. Processing User Messages

Define a function that handles user input, updates the chat context, and renders messages:

```python theme={null}
def collect_messages():
    prompt = user_input.value
    user_input.value = ""  # Clear the input field

    # Add user prompt to context and fetch assistant response
    context.append({"role": "user", "content": prompt})
    response = get_chat_completion(context)
    context.append({"role": "assistant", "content": response})

    # Display the user’s message
    panels.append(pn.Row("User:", pn.pane.Markdown(prompt, width=600)))
    # Display the assistant’s reply
    panels.append(
        pn.Row(
            "Assistant:",
            pn.pane.Markdown(
                response,
                width=600,
                styles={"background-color": "#F6F6F6"}
            )
        )
    )

    return pn.Column(*panels)
```

***

## 7. Building the Dashboard

Bind the message handler to a button and assemble the UI:

```python theme={null}
# Button to send messages
chat_button = pn.widgets.Button(name="Send", button_type="primary")

# Bind the function to the button click
interactive_chat = pn.bind(collect_messages, chat_button)

# Layout the dashboard
dashboard = pn.Column(
    user_input,
    pn.Row(chat_button),
    pn.panel(interactive_chat, loading_indicator=True, height=300),
)

dashboard
```

<Callout icon="lightbulb">
  Run this cell in your Jupyter notebook. Click **Send** after typing each message to interact with BurgerBot.
</Callout>

***

## 8. Dependencies

|    Package | Minimum Version | Purpose                            |
| ---------: | --------------: | ---------------------------------- |
|     openai |          0.27.0 | OpenAI ChatCompletion API client   |
|      panel |          0.14.0 | Interactive dashboards and widgets |
| jupyterlab |           3.0.0 | Jupyter notebook environment       |

***

## 9. Next Steps

In upcoming sections, you’ll learn how to:

* Craft more precise prompts for improved order accuracy
* Manage conversation state and handle edge cases
* Style the Panel UI for a polished user experience
* Integrate a real-time database for order tracking

***

## Links and References

* [OpenAI Chat API Documentation](https://platform.openai.com/docs/guides/chat)
* [Panel Documentation](https://panel.holoviz.org)
* [Jupyter Project](https://jupyter.org)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/fb5fb83d-53e8-48e9-9bee-fed2a26dcd44" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/098b2658-271b-4427-9b7d-e8e214f3cafc" />
</CardGroup>


# Section Intro

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Building-an-Interactive-Chatbot/Section-Intro/page

This comprehensive guide teaches building an interactive chatbot using OpenAI’s GPT-3.5 and GPT-4 models for customer service applications.

Welcome to this comprehensive guide on building an interactive chatbot powered by OpenAI’s GPT-3.5 and GPT-4 models. In this tutorial, you’ll learn how to:

* Craft effective prompts for both word-based and conversational APIs
* Manage conversation history to maintain context
* Assemble building blocks for a responsive customer-service chatbot
* Deploy a sample chatbot for a fictional fast-food burger restaurant

By the end of this lesson, you’ll have a solid understanding of how to integrate OpenAI’s chat completions into your applications and deliver a seamless conversational experience.

<Callout icon="lightbulb">
  Make sure you have an active OpenAI API key. You can sign up at [OpenAI](https://platform.openai.com/signup).
</Callout>

## Word Completion vs. Chat Completion

| Feature            | Word Completion                   | Chat Completion                                   |
| ------------------ | --------------------------------- | ------------------------------------------------- |
| API Endpoint       | `/v1/completions`                 | `/v1/chat/completions`                            |
| Input Format       | Plain prompt string               | Array of structured messages                      |
| Best Use Cases     | Short text generation, code fixes | Stateful conversations, multi-turn dialogues      |
| Model Examples     | `text-davinci-003`                | `gpt-3.5-turbo`, `gpt-4`                          |
| Context Management | Limited (token-based)             | Full message history, system/user/assistant roles |

## What You’ll Build

1. **Prompt Engineering**: Learn how to frame user requests for accurate responses.
2. **Context Storage**: Implement a history buffer to pass previous messages to the API.
3. **Chat Loop**: Create an interactive loop to send and receive messages.
4. **Fast-Food Bot**: Deploy a customer-service chatbot that takes orders, answers FAQs, and handles errors.

Let’s dive into the details!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/6be42d7c-95f5-40ec-aaae-d38ef0d950bf" />
</CardGroup>
