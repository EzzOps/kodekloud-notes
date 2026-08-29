# Initialize Panel extension
pn.extension()

# Configure your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
# Or hardcode your key (not recommended for production):
# openai.api_key = "YOUR_API_KEY"
```

> **lightbulb** Storing your API key in an environment variable keeps it secure. Avoid committing secrets to version control.

> **triangle-alert** Hardcoding your API key in source code can expose it publicly. Use environment variables or secret managers.

***

## 2. Chat Completion Function

Define a reusable function that sends the full conversation history to the OpenAI GPT-3.5 Turbo model and returns the assistant’s reply.

```python theme={null}
def get_chat_completion(messages):
    """
    Sends a list of message dicts to OpenAI and returns the assistant response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content
```

***

## 3. Collecting Messages & Refreshing the UI

The `collect_messages` callback does three things:

1. Reads the user’s input and clears the text field.
2. Appends user and assistant messages to the `context`.
3. Updates the Panel layout with the latest chat entries.

```python theme={null}
def collect_messages(_):
    # 1. Read and clear user input
    prompt = inp.value
    inp.value = ''

    # 2. Append user message and get reply
    context.append({'role': 'user', 'content': prompt})
    response = get_chat_completion(context)
    context.append({'role': 'assistant', 'content': response})

    # 3. Update the chat panels
    panels.append(pn.Row("**User:**", pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row(
            "**Assistant:**",
            pn.pane.Markdown(response, width=600),
            styles={'background-color': '#F6F6F6'}
        )
    )
    return pn.Column(*panels)
```

***

## 4. Designing the System Prompt

We steer the chatbot’s behavior using a detailed system prompt. This includes greetings, order flow, and a complete menu. Use a Markdown table for clarity and SEO.

```python theme={null}
bot_instructions = """
You are BurgerBot, an automated assistant for Burger Bliss. 
1. Greet the customer.
2. Collect the full order.
3. Ask if it’s pickup or delivery.
4. Summarize the order and confirm.
5. If delivery, request the address.
6. Collect payment.
Respond in a friendly, short conversational style.
"""
```

### Menu and Pricing

| Item                        | Category | Price (Rs.) |
| --------------------------- | -------- | ----------: |
| Crispy Veg Burger           | Burger   |       89.00 |
| BB Veggie Burger            | Burger   |      139.00 |
| Veg Chilli Cheese Burger    | Burger   |      165.00 |
| Paneer Bliss Burger         | Burger   |      189.00 |
| Crispy Chicken Burger       | Burger   |      109.00 |
| BB Grill Chicken Burger     | Burger   |      149.00 |
| Spicy Crispy Chicken Burger | Burger   |      179.00 |
| **Extras**                  |          |             |
| Extra Cheese                | Add-on   |       30.00 |
| Extra Fries                 | Add-on   |       45.00 |
| Extra Sauce                 | Add-on   |       20.00 |
| **Drinks**                  |          |             |
| Coke                        | Beverage |       30.00 |
| Fanta                       | Beverage |       30.00 |
| Sprite                      | Beverage |       30.00 |
| Bottled Water               | Beverage |       20.00 |

````text theme={null}

---

## 5. Building the UI with Panel

Initialize the conversation context and Panel widgets. Bind the “Chat” button to our `collect_messages` function.

```python
# Initialize state
panels = []
context = [{'role': 'system', 'content': bot_instructions}]

# Create input widget and button
inp = pn.widgets.TextInput(value="", placeholder="Type your message here...")
button_conversation = pn.widgets.Button(name="Chat", button_type="primary")

# Bind callback
interactive_conversation = pn.bind(collect_messages, button_conversation)

# Assemble the dashboard layout
dashboard = pn.Column(
    pn.pane.Markdown("## 🍔 Burger Bliss Chatbot"),
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=400),
)

# Display the UI
dashboard.show()
```text

---

## 6. Example Conversation & Inspecting Context

After launching the dashboard, try these sample exchanges:

1. “I want to order a chicken burger.”  
2. “Spicy Crispy Chicken Burger.”  
3. “Can I have the bill please?”  
4. “I am done.”  
5. “What’s the total?”  
6. “Delivery”

To inspect the stored message history:

```python
# In a separate cell, print the context
print(context)
```text

You’ll see a list of dictionaries:

```python
[
  {'role': 'system',    'content': '...bot instructions...'},
  {'role': 'assistant', 'content': 'Hi! Welcome to Burger Bliss!'},
  {'role': 'user',      'content': 'I want to order a chicken burger.'},
  {'role': 'assistant', 'content': 'Great choice! Which chicken burger would you like?'},
  ...
]
````

This history enables the model to maintain context across turns, crucial for coherent, multi-step conversations.

***

## Next Steps

* Persist `context` to a file or database for chat sessions.
* Customize `bot_instructions` and menu for other restaurants.
* Enhance the UI with dropdowns for menu items and add-on buttons.

***

## Links and References

* [OpenAI Python SDK Documentation](https://beta.openai.com/docs/api-reference/introduction)
* [Panel User Guide](https://panel.holoviz.org/)
* [Python `os` module](https://docs.python.org/3/library/os.html)
* [Environment Variables Best Practices](https://12factor.net/config)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/c11fdf11-ed65-4c3f-87e8-992a06e9b699)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/36c56a19-11f6-4db1-8bd7-bd6a96c82268/lesson/2d995331-76c9-4ad5-b235-271effda8247)


# Project Overview Creating a Chatbot for a Restaurant

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Building-an-Interactive-Chatbot/Project-Overview-Creating-a-Chatbot-for-a-Restaurant/page

This tutorial guides you in building a fast-food ordering chatbot named BurgerBot using OpenAI Chat API and HoloViz Panel in a Jupyter notebook.

In this tutorial, you’ll build a fast-food ordering chatbot—**BurgerBot**—using the [OpenAI Chat API](https://platform.openai.com/docs/guides/chat) and [HoloViz Panel](https://panel.holoviz.org) within a [Jupyter notebook](https://jupyter.org). We’ll start by experiencing the end-user flow and then break down each implementation step: environment setup, API integration, instruction design, state management, and UI assembly.

***

## Table of Contents

1. [End-User Experience](#1-end-user-experience)
2. [Setup: Imports and API Key](#2-setup-imports-and-api-key)
3. [Chat Completion Helper](#3-chat-completion-helper)
4. [Bot Instructions](#4-bot-instructions)
5. [Conversation State and Widgets](#5-conversation-state-and-widgets)
6. [Processing User Messages](#6-processing-user-messages)
7. [Building the Dashboard](#7-building-the-dashboard)
8. [Dependencies](#8-dependencies)
9. [Next Steps](#9-next-steps)

***

## 1. End-User Experience

Inside the notebook, Panel presents a simple chat interface. A typical conversation might look like this:

```text theme={null}
User: Hello
Assistant: Hello there! Welcome to Burger Bliss. How can I assist you today?
User: I want to order a chicken burger.
Assistant: We have two options: Crispy Chicken Burger and BB Grilled Chicken Burger. Which one would you like?
User: I’ll have the Spicy Crispy Chicken Burger.
Assistant: Excellent choice! Anything else you’d like to add, like extra fries or a drink?
User: Can I have extra fries please?
Assistant: Of course! Would you like anything to drink? We have Coke, Fanta, Sprite, and Bottled Water.
User: I am done.
Assistant: Alright, that’s a Spicy Crispy Chicken Burger with extra fries. Pickup or delivery?
User: It’s for pickup.
Assistant: Great! When would you like to pick it up?
User: In 10 minutes.
Assistant: Perfect. Your order will be ready for pickup in 10 minutes. Thank you for choosing Burger Bliss!
```

***

## 2. Setup: Imports and API Key

```python theme={null}
import os
import openai
import panel as pn
