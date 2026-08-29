# Demo Image Generation

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Generating-Images/Demo-Image-Generation/page

Learn to generate images from text prompts using OpenAI's DALL·E API with customization options for outputs and resolution.

Learn how to generate stunning images from text prompts using the OpenAI DALL·E API. You can customize the prompt, choose the number of outputs, and select the resolution that best fits your application.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup and Helper Function](#setup-and-helper-function)
3. [Supported Image Sizes](#supported-image-sizes)
4. [Generate and Display a Single Image](#generate-and-display-a-single-image)
5. [Generate Multiple Images](#generate-multiple-images)
6. [Base64-Encoded Output](#base64-encoded-output)
7. [Integrating with GPT Models](#integrating-with-gpt-models)
8. [References](#references)

***

## Prerequisites

* Python 3.7+
* An OpenAI API key
* `openai` Python package

Install the SDK with:

```bash theme={null}
pip install openai
```

<Callout icon="lightbulb">
  Store your API key in an environment variable for security:

  ```bash theme={null}
  export OPENAI_API_KEY="your_api_key_here"
  ```
</Callout>

***

## Setup and Helper Function

Import packages, configure your key, and wrap the DALL·E call in a reusable function:

```python theme={null}
import os
import openai
from IPython.display import Image, display
