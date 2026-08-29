# Output:
# Generated Image URL: https://example.com/your-generated-image.png
```

Open the printed URL in your browser to see your AI-generated artwork.

***

## Experiment with Custom Prompts

Change the prompt text to explore different styles and concepts:

```python theme={null}
if __name__ == "__main__":
    prompt = "A programmer building a robotic dinosaur in a futuristic lab"
    image_url = generate_image(prompt, size="1024x1024")
    print("Generated Image URL:", image_url)
```

Feel free to iterate on your prompt until you find the perfect visual.

***

## Supported Image Sizes

| Size      | Dimensions       | Use Case                                         |
| --------- | ---------------- | ------------------------------------------------ |
| 256×256   | 256px by 256px   | Thumbnails, small icons                          |
| 512×512   | 512px by 512px   | Medium-resolution previews                       |
| 1024×1024 | 1024px by 1024px | High-resolution prints or detailed illustrations |

***

## Links and References

* [OpenAI Python SDK Reference](https://github.com/openai/openai-python)
* [DALL·E Image Generation Guide](https://platform.openai.com/docs/guides/images)
* [Managing API Keys](https://platform.openai.com/docs/api-keys)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/d76ba88f-ebc6-4d12-8aa5-9359bc23be72/lesson/7f0643ad-d897-4717-a1a9-991fd02707a9" />
</CardGroup>


# Project 2 Image Captioning

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Vision/Project-2-Image-Captioning/page

This tutorial guides you in building a Python script to generate image captions using GPT-4's vision capabilities.

In this tutorial, you’ll build a Python script that takes an image URL and generates a descriptive caption using GPT-4’s vision capabilities. Instead of DALL·E, we’ll use the GPT-4 chat completion endpoint, which can process image URLs directly and describe what it “sees.”

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Initialize the OpenAI Client](#initialize-the-openai-client)
4. [Define the Image URL](#define-the-image-url)
5. [Generate Captions Function](#generate-captions-function)
6. [Run the Script](#run-the-script)
7. [Sample Output](#sample-output)
8. [References](#references)

***

## Prerequisites

* Python 3.7+
* `pip` package manager
* An OpenAI API key with GPT-4 access
* Internet connectivity to fetch the image

<Callout icon="triangle-alert">
  Never hard-code your API key in a public repository. Use environment variables or a secure vault.
</Callout>

***

## Installation

Install the official OpenAI Python client:

```bash theme={null}
pip install openai
```

***

## Initialize the OpenAI Client

Import and initialize the client with your API key:

```python theme={null}
from openai import OpenAI
