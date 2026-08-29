# Variation 1
display(Image(url=response['data'][0]['url']))

# Variation 2
display(Image(url=response['data'][1]['url']))

# Variation 3
display(Image(url=response['data'][2]['url']))
```

Each variation offers a unique composition or style. Experiment with different source images or parameters to explore new creative directions.

## Summary of Steps

| Step                  | Description                                 | Example Code                                   |
| --------------------- | ------------------------------------------- | ---------------------------------------------- |
| Import & Authenticate | Load libraries and set API key              | `openai.api_key = os.getenv("OPENAI_API_KEY")` |
| Preview Source Image  | Display the original image                  | `display(Image(...))`                          |
| Request Variations    | Generate `n` new images with specified size | `openai.Image.create_variation(...)`           |
| Render Outputs        | Show each variation using returned URLs     | `display(Image(url=...))`                      |

## Next Steps

Now that you’ve created image variations, consider exploring other OpenAI offerings:

* [OpenAI DALL·E Image API Guide](https://platform.openai.com/docs/guides/images)
* [OpenAI Whisper Speech-to-Text](https://platform.openai.com/docs/guides/speech-to-text)

## References

* [OpenAI Python Library](https://github.com/openai/openai-python)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/0818deaa-36b0-45ad-aa21-aa04378587c7)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/641a7dc4-14a0-4bb9-b755-657b3fca56b6)


# Overview of DALL E 2

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Generating-Images/Overview-of-DALL-E-2/page

DALL-E 2 is OpenAI’s model for generating high-quality images from text and visual prompts, enabling creative image synthesis and manipulation.

DALL-E 2 is OpenAI’s advanced text-to-image foundation model, designed to generate high-quality images from both textual and visual prompts. Unlike large language models such as [GPT-3](https://openai.com/product/gpt-3), DALL-E 2 specializes in creative image synthesis. You can:

1. Provide a **text prompt** describing the scene, style, or concept you want to visualize.
2. Supply an **image prompt** to create variations, overlays, or edits of an existing picture.

The model processes your input and returns one or more fully generated images, offering endless possibilities for design, prototyping, and creative exploration.

![The image is a diagram illustrating the DALL-E 2 Foundation Model, showing input as text and images leading to the model, which then outputs images.](https://kodekloud.com/kk-media/image/upload/v1752881508/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Overview-of-DALL-E-2/dall-e-2-foundation-model-diagram.jpg)

## Key DALL-E 2 APIs

DALL-E 2 provides three core RESTful endpoints for image creation and manipulation:

| API              | Description                                                                                | Typical Use Case                            |
| ---------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------- |
| Image Generation | Generate new images from scratch based on a descriptive text prompt.                       | Concept art, storyboarding, product mockups |
| Image Editing    | Edit or extend an existing image by applying a mask and text prompt to specify changes.    | Photo retouching, add/remove objects        |
| Image Variation  | Produce multiple stylistic variations of a source image without any additional text input. | Branding explorations, style testing        |

![The image outlines three key APIs: Image Generation, Image Editing, and Image Variation, with a brief description of the Image Editing API's functionality.](https://kodekloud.com/kk-media/image/upload/v1752881509/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Overview-of-DALL-E-2/image-generation-editing-variation-apis.jpg)

### 1. Image Generation

Create brand-new visuals by sending a textual description:

```python theme={null}
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    prompt="A futuristic city skyline at sunset, neon-lit skyscrapers reflecting on water",
    n=1,
    size="1024x1024"
)

print(response.data[0].url)
```

### 2. Image Editing

Modify a specific region of an existing image by supplying:

* `image`: the original image file
* `mask`: a black-and-white mask highlighting the edit area
* `prompt`: text describing what to place in the masked region

```python theme={null}
response = client.images.edit(
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="Add a sleek flying car in the sky above the buildings",
    n=1,
    size="512x512"
)

print(response.data[0].url)
```

> **triangle-alert** Ensure your mask file aligns exactly with the dimensions of the source image. Mismatched sizes will result in API errors.

### 3. Image Variation

Generate several stylistic renditions of an existing image:

```python theme={null}
response = client.images.variations(
    image=open("input.png", "rb"),
    n=3,
    size="256x256"
)

for img in response.data:
    print(img.url)
```

> **lightbulb** DALL-E 2 supports three output resolutions: **256×256**, **512×512**, and **1024×1024**. Square images tend to produce the best results, but feel free to experiment with other aspect ratios.

![The image describes three key APIs: Image Generation, Image Editing, and Image Variation, with a note that Image Variation generates multiple variations of the same image in different sizes.](https://kodekloud.com/kk-media/image/upload/v1752881510/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Overview-of-DALL-E-2/image-generation-editing-variation-apis-2.jpg)

Remember, generative image models incorporate a degree of creative randomness. Iterating your prompts—tweaking style descriptors, color palettes, or composition details—will help you achieve the perfect result.

***

## Next Steps: Live Demo

In the following section, we’ll walk through a hands-on demonstration of each DALL-E 2 API, complete with live code execution and real-time image generation.

***

## Links and References

* [OpenAI DALL-E 2 Documentation](https://platform.openai.com/docs/guides/images)
* [GPT-3 Overview](https://openai.com/product/gpt-3)
* [OpenAI Python Client](https://github.com/openai/openai-python)

- [Watch Video](https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/dcf08f43-1a17-4aea-8646-cad4f746c1e2)
