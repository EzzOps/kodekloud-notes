# Load API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
```

## 2. Prepare Your Images

You need three files:

1. **Original image** (with the object you want to replace)
2. **Base image** (same image after removing the object)
3. **Mask image** (a transparent PNG that marks the area to edit)

```python theme={null}
display(Image(filename='images/dog_table.png'))        # Original image with dog
display(Image(filename='images/table.png'))            # Image with dog removed
display(Image(filename='images/table-masked.png'))     # Transparent mask placeholder
```

## 3. Perform the Edit

Use the `create_edit` endpoint to fill the masked area based on your prompt:

```python theme={null}
response = openai.Image.create_edit(
    image=open('images/table.png', 'rb'),
    mask=open('images/table-masked.png', 'rb'),
    prompt='A cat sitting on a dining table chair waiting for food',
    n=1,
    size='512x512'
)
edited_url = response['data'][0]['url']
display(Image(url=edited_url))
```

## 4. Generate Multiple Variations

If you’d like several options, increase `n` and iterate through the results:

```python theme={null}
response = openai.Image.create_edit(
    image=open('images/table.png', 'rb'),
    mask=open('images/table-masked.png', 'rb'),
    prompt='A cat sitting on a dining table chair waiting for food',
    n=3,
    size='512x512'
)
for result in response['data']:
    display(Image(url=result['url']))
```

<Callout icon="triangle-alert">
  Requesting a large number of edits or very high resolutions may incur higher usage costs. Monitor your [API usage dashboard](https://platform.openai.com/account/usage).
</Callout>

## 5. Parameter Reference

| Parameter | Type    | Description                                                   |
| --------- | ------- | ------------------------------------------------------------- |
| `image`   | File    | The base image without the masked object (PNG or JPEG).       |
| `mask`    | File    | A transparent PNG marking the area to edit (white = mask).    |
| `prompt`  | String  | Textual description of what should appear in the masked area. |
| `n`       | Integer | Number of edits to generate (1–10).                           |
| `size`    | String  | Output resolution: `256x256`, `512x512`, or `1024x1024`.      |

## 6. Generate Image Variations

Beyond masking, DALL·E 2 can also create variations of a single image without any prompt:

```python theme={null}
response = openai.Image.create_variation(
    image=open('images/table.png', 'rb'),
    n=4,
    size='512x512'
)
for img in response['data']:
    display(Image(url=img['url']))
```

For full details on both endpoints, see the [OpenAI Image API Reference](https://platform.openai.com/docs/api-reference/images).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/ff7f071e-87be-41fd-8f4c-0d3fa959250a" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/mastering-generative-ai-with-openai/module/ad3893f7-fba6-4142-a575-422006496a97/lesson/0dfd8ad8-78ca-4419-9380-653e4f34b845" />
</CardGroup>


# Demo Image Variations

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Generating-Images/Demo-Image-Variations/page

This tutorial teaches how to generate multiple variations of an image using the OpenAI DALL·E API.

In this tutorial, you’ll learn how to generate multiple variations of an existing image using the OpenAI DALL·E API. By the end, you’ll be able to:

* Load and preview a source image
* Call the DALL·E variations endpoint
* Render the generated images

## Prerequisites

* Python 3.6+
* Install the OpenAI Python library:

```bash theme={null}
pip install openai
```

* Set your API key as an environment variable:

```bash theme={null}
export OPENAI_API_KEY="your_api_key_here"
```

## 1. Import Modules and Configure the API Key

Begin by importing the necessary modules and loading your API key:

```python theme={null}
import openai
import os
from IPython.display import Image, display

openai.api_key = os.getenv("OPENAI_API_KEY")
```

## 2. Load and Display the Source Image

Use IPython’s display utilities to preview the original asset:

```python theme={null}
display(Image(filename='./images/lion-cub.png'))
```

This shows a lion and its cub.

## 3. Generate Three Variations

Call the DALL·E variation endpoint, specifying the image file, output size, and number of results:

```python theme={null}
response = openai.Image.create_variation(
    image=open('./images/lion-cub.png', 'rb'),
    size='512x512',
    n=3
)
```

<Callout icon="lightbulb">
  You can modify the `size` or the `n` parameter to control the resolution and the number of variations returned.
</Callout>

## 4. Render the Generated Variations

Display each variation using the URLs returned in the response:

```python theme={null}
