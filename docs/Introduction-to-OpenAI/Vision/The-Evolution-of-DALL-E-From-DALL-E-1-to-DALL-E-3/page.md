# Initialize the client with your API key
client = OpenAI(api_key="sk-your-api-key-here")
```

<Callout icon="lightbulb">
  You can find the latest OpenAI Python SDK and examples in the [openai-python GitHub repo](https://github.com/openai/openai-python).
</Callout>

***

## Define the Image URL

Specify the publicly accessible image URL you want to caption:

```python theme={null}
# Image URL to caption
image_url = "https://assets-prd.ignimgs.com/2022/06/10/netflix-one-piece-1654901410673.jpg"
```

***

## Generate Captions Function

Create a helper function that sends a chat completion request to GPT-4, including both a text prompt and the image URL. We’ll cap the response at 125 tokens to keep captions concise.

```python theme={null}
from typing import Dict

def generate_captions(image_url: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is this image?"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=125
    )
    # Extract the generated caption
    return response.choices[0].message.content
```

***

## Run the Script

Use the function and print the returned caption:

```python theme={null}
if __name__ == "__main__":
    caption = generate_captions(image_url)
    print(caption)
```

***

## Sample Output

```plaintext theme={null}
This image features characters from the anime and manga "One Piece." In the center is Monkey D. Luffy wearing his trademark straw hat. To his left stands Sanji with blond hair, and to his right is Nami, recognizable by her orange hair. They are members of the Straw Hat Pirates.
```

***

## References

* [OpenAI Python Client](https://github.com/openai/openai-python)
* [GPT-4 Vision](https://openai.com/product/gpt-4-vision)
* [OpenAI API Reference: Chat Completions](https://platform.openai.com/docs/api-reference/chat)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/d76ba88f-ebc6-4d12-8aa5-9359bc23be72/lesson/c5fed0f6-e493-4bd2-a2b8-2bbc201e53fc" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/d76ba88f-ebc6-4d12-8aa5-9359bc23be72/lesson/c7d10d6d-5077-45cd-acc1-a865d54a9f63" />
</CardGroup>


# The Evolution of DALL E From DALL E 1 to DALL E 3

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Vision/The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/page

This article explores the advancements of OpenAIs DALL·E from its first version to the latest, highlighting improvements in image quality and creative capabilities.

Discover how OpenAI’s text-to-image AI tool has advanced since 2021—boosting resolution, improving prompt fidelity, and unlocking new creative workflows. Starting with the original DALL·E, we’ll trace its major upgrades, community-driven variants, and the latest innovations shaping the future of AI-generated imagery.

<Frame>
  ![The image is an agenda slide with three points: "DALL-E – The first version," "Enhancements and new capabilities," and "DALL-E Mini and other variants."](https://kodekloud.com/kk-media/image/upload/v1752879318/notes-assets/images/Introduction-to-OpenAI-The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/dall-e-agenda-enhancements-variants.jpg)
</Frame>

***

## 1. DALL·E 1: The Pioneer of Text-to-Image Synthesis

Debuting in January 2021, DALL·E 1 introduced a transformer-based model trained on millions of text–image pairs. It set the stage for AI-driven creative composition by translating natural language prompts into original visuals.

### Key Features

* Text-to-Image Mapping: Converts detailed prompts into coherent images
* Concept Blending: Merges unrelated ideas (e.g., “an avocado-shaped chair”) into a single scene

### Limitations

* Low Resolution: Outputs were often under 256×256 pixels and lacked fine detail
* Artifact Risks: Complex prompts could produce visual glitches or inconsistent elements

<Frame>
  ![The image is an infographic about DALL-E's first version, highlighting its features like natural language blending and text-to-image mapping, along with limitations such as lower resolution and limited practical use.](https://kodekloud.com/kk-media/image/upload/v1752879319/notes-assets/images/Introduction-to-OpenAI-The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/dall-e-v1-infographic-features-limitations.jpg)
</Frame>

***

## 2. DALL·E 2: Dramatically Higher Fidelity and Precision

Launched in 2022, DALL·E 2 marked a substantial leap in image quality, enabling designers and marketers to create production-ready visuals from text prompts.

* Higher Resolution & Detail: Supports up to 1024×1024px with richer textures and lighting
* Improved Compositional Accuracy: Enhanced spatial reasoning—objects relate correctly in 3D space
* Inpainting & Variations: Edit specific regions or generate alternative renditions of an existing image
* Enhanced Prompt Alignment: Follows nuanced instructions more faithfully, reducing trial-and-error

<Frame>
  ![The image lists enhancements and new capabilities of DALL-E 2, including improved image generation, higher resolution, inpainting, and better compositional accuracy.](https://kodekloud.com/kk-media/image/upload/v1752879320/notes-assets/images/Introduction-to-OpenAI-The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/dall-e-2-enhancements-new-capabilities.jpg)
</Frame>

***

## 3. Community-Driven Variants: DALL·E Mini and Beyond

To democratize AI art, open-source projects like DALL·E Mini (now Craiyon) emerged, replicating core functionality on limited hardware.

* Accessibility: Runs on standard CPUs or small GPUs—great for hobbyists
* Rapid Prototyping: Enables quick experimentation without cloud costs
* Open Ecosystem: Researchers can fine-tune models or integrate with other AI pipelines

<Frame>
  ![The image describes DALL-E Mini and other variants as being less computationally intensive, more accessible to developers and researchers, and functioning as open-source models on a smaller scale.](https://kodekloud.com/kk-media/image/upload/v1752879320/notes-assets/images/Introduction-to-OpenAI-The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/dall-e-mini-open-source-models.jpg)
</Frame>

<Callout icon="lightbulb">
  Use descriptive adjectives, specify styles (e.g., “oil painting,” “isometric”), and define color palettes to guide the model toward your vision. Experiment with step-by-step instructions for complex scenes.
</Callout>

***

## 4. DALL·E 3: State-of-the-Art Imagery and Interactive Editing

The latest iteration elevates AI-generated visuals with print-quality resolution, interactive tools, and fine-grained control.

* Ultra-High Resolution: Delivers up to 2048×2048px—suitable for large-format prints
* Interactive Inpainting: Iteratively refine subregions with follow-up prompts
* Precise Prompt Control: Constrain style, mood, and composition using advanced conditioning
* Faster Inference & Cost Efficiency: Optimized for real-time workflows and reduced compute costs

**Expanded Use Cases**

* Film & Animation: Generate storyboard frames and concept art directly from scripts
* E-Commerce: Produce hyper-realistic product renders for marketing and prototyping

<Frame>
  ![The image outlines key enhancements of DALL-E 3, highlighting features like new capabilities, higher resolution, interactive editing, and expanded use cases in film, animation, and e-commerce.](https://kodekloud.com/kk-media/image/upload/v1752879321/notes-assets/images/Introduction-to-OpenAI-The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/dall-e-3-enhancements-features-overview.jpg)
</Frame>

***

## 5. Future Directions in AI Image and Video Generation

Emerging research points toward:

* 3D Asset Creation: From flat images to fully modeled objects for VR/AR and gaming
* Text-to-Video Synthesis: Dynamic scene generation for ads, short films, and interactive media
* Multimodal Integration: Seamless fusion of text, image, and audio generation for immersive storytelling

<Frame>
  ![The image outlines future directions in technology, focusing on 3D image generation for VR and gaming, video generation for various industries, and enhanced multimodal capabilities for seamless transitions between text, image, and audio.](https://kodekloud.com/kk-media/image/upload/v1752879322/notes-assets/images/Introduction-to-OpenAI-The-Evolution-of-DALL-E-From-DALL-E-1-to-DALL-E-3/future-tech-directions-3d-video-multimodal.jpg)
</Frame>

***

## Comparison of DALL·E Versions

| Feature            | DALL·E 1        | DALL·E 2           | DALL·E 3               |
| ------------------ | --------------- | ------------------ | ---------------------- |
| Resolution         | ≤256×256        | Up to 1024×1024    | Up to 2048×2048        |
| Prompt Fidelity    | Basic alignment | Enhanced alignment | Fine-grained control   |
| Editing Tools      | None            | Inpainting & masks | Interactive inpainting |
| Speed & Efficiency | Slower          | Faster             | Real-time optimized    |
| API & Integration  | Limited Access  | Public API         | Expanded ecosystem     |

***

## References and Further Reading

* [OpenAI DALL·E Blog Posts](https://openai.com/research/dall-e)
* [Text-to-Image Synthesis Techniques](https://arxiv.org/abs/2102.12092)
* [Craiyon (formerly DALL·E Mini)](https://www.craiyon.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/d76ba88f-ebc6-4d12-8aa5-9359bc23be72/lesson/678a9ff8-b8de-423e-932f-01f46ec25076" />
</CardGroup>
