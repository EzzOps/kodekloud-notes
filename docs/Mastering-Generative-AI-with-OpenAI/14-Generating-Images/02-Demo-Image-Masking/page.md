# Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
# Alternatively, set directly (not recommended for production)
def generate_image(prompt: str, size: str = "512x512", n: int = 1, response_format: str = "url"):
    """
    Generate `n` images for a given text prompt.

    Args:
      prompt: Text description to guide image creation.
      size:  Resolution, choose from our supported list.
      n:      Number of images to generate.
      response_format: "url" or "b64_json".

    Returns:
      A list of dicts containing the image data (URL or base64 JSON).
    """
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size,
        response_format=response_format
    )
    return response["data"]
```

***

## Supported Image Sizes

Choose the resolution that matches your use case:

| Size   | Pixel Dimensions | Use Case                       |
| ------ | ---------------- | ------------------------------ |
| Small  | 256×256          | Thumbnails, icons              |
| Medium | 512×512          | Social posts, blog headers     |
| High   | 1024×1024        | Print, high-resolution display |

***

## Generate and Display a Single Image

Create a 512×512 image of a “cozy coffee-shop corner” and render it in Jupyter:

```python theme={null}
# Generate one image
images = generate_image(
    prompt="Interior photography of a cozy corner in a coffee shop, using natural light.",
    size="512x512",
    n=1
)

# Display the first result
image_url = images[0]["url"]
Image(url=image_url, width=512)
```

Each execution produces a new, unique image.

***

## Generate Multiple Images

Request several variations at once by increasing `n` and iterating over the response:

```python theme={null}
# Generate three variations
images = generate_image(
    prompt="Interior photography of a cozy corner in a coffee shop, using natural light.",
    size="512x512",
    n=3
)

# Display all generated images side by side
for img in images:
    display(Image(url=img["url"], width=256))
```

***

## Base64-Encoded Output

If you prefer embedding images directly (e.g., in HTML or JSON), request `b64_json`:

```python theme={null}
# Generate one base64 image
b64_data = generate_image(
    prompt="A futuristic city skyline at dusk, cinematic lighting",
    size="1024x1024",
    n=1,
    response_format="b64_json"
)

# Access the base64 string
encoded_str = b64_data[0]["b64_json"]
```

> **triangle-alert** Large base64 payloads can impact performance. Use `b64_json` sparingly.

***

## Integrating with GPT Models

You can automate end-to-end content creation by combining DALL·E with GPT:

1. **Text-to-Image Workflow**
   * Use [GPT-3.5 Turbo](https://platform.openai.com/docs/models/gpt-35-turbo) to draft descriptive prompts.
   * Feed them into DALL·E for image generation.

2. **Prompt Engineering**
   * Send long-form descriptions to GPT-4 to refine or expand for DALL·E.
   * Obtain optimized prompts that yield better visual results.

This approach can power dynamic blog posts, marketing assets, or social media content.

***

## References

* [OpenAI Image API Reference](https://platform.openai.com/docs/api-reference/images)
* [DALL·E Model Overview](https://platform.openai.com/docs/models/dall-e)
* [GPT-3.5 Turbo Documentation](https://platform.openai.com/docs/models/gpt-35-turbo)
* [GPT-4 Documentation](https://platform.openai.com/docs/models/gpt-4)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/d7856e5a-7ed4-453c-a115-e6e70641c3d5)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/1779c5fe-946f-4465-bae3-8c0dca40d546)


# Demo Image Masking

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Generating-Images/Demo-Image-Masking/page

This tutorial teaches how to use DALL·E 2’s image masking feature for editing pictures by defining masked regions and providing text prompts.

In this tutorial, you’ll learn how to use DALL·E 2’s image masking feature to edit an existing picture by defining a masked region and supplying a text prompt. This approach is perfect for seamlessly replacing objects, changing backgrounds, or adding new elements to your images.

## Prerequisites

* Python 3.7+
* The `openai` Python package (`pip install openai`)
* An OpenAI API key

> **lightbulb** Make sure you’ve exported your API key as an environment variable:

  ```bash theme={null}
  export OPENAI_API_KEY="your_api_key_here"
  ```

## 1. Install and Authenticate

Begin by installing the client library and initializing your API key in Python:

```python theme={null}
import openai
import os
from IPython.display import Image
