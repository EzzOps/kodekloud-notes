# Understanding DALL E Text to Image Generation

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Vision/Understanding-DALL-E-Text-to-Image-Generation/page

This guide explores how DALL·E transforms text prompts into high-resolution, coherent images using a detailed pipeline.

In this guide, we’ll explore how DALL·E transforms text prompts into high-resolution, coherent images. Built on the transformer architecture, DALL·E’s pipeline involves:

* Tokenizing text
* Mapping tokens to embeddings
* Applying self-attention over text
* Predicting discrete image tokens
* Decoding tokens into pixels
* Assembling and refining image patches

## Pipeline Overview

| Stage                   | Purpose                                                 |
| ----------------------- | ------------------------------------------------------- |
| Tokenization            | Split prompt into subword tokens using BPE              |
| Embedding               | Map each token to a high-dimensional vector             |
| Text Self-Attention     | Capture contextual relationships between tokens         |
| Image Token Generation  | Predict discrete image tokens for structure & style     |
| Image Decoding          | Autoregressively convert tokens into pixel values       |
| Patch Assembly & Render | Stitch patches and refine pixels into a seamless output |

## 1. Tokenization

DALL·E begins by tokenizing your input prompt. Using Byte-Pair Encoding (BPE), the model splits text into subword tokens, ensuring efficient coverage of vocabulary.

<Frame>
  ![The image outlines the process of tokenizing text inputs in three steps: converting text to tokens, using tokens as language building blocks in machine learning, and applying byte-pair encoding (BPE).](../../../../images/kodekloud.com/kk-media/image/upload/v1752879323/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/text-tokenization-process-bpe-diagram.jpg)
</Frame>

Example in Python:

```python theme={null}
text = "a cat wearing sunglasses"
tokens = ["a", " cat", " wear", "ing", " sun", "glass", "es"]
```

These tokens serve as the basis for all subsequent stages.

## 2. Embedding Tokens

Each token is then projected into a continuous embedding space. These dense vectors capture semantic meaning and link text to visual concepts.

<Frame>
  ![The image outlines the process of embedding tokens in four steps, explaining how DALL-E creates embeddings, their mathematical representation, understanding word-visual relationships, and mapping words to image-related feature vectors.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879324/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/embedding-tokens-dall-e-process-diagram.jpg)
</Frame>

For example, the token for “cat” encodes feline features, while “sunglasses” reflects accessory attributes.

## 3. Attention Mechanisms for Text

DALL·E employs self-attention to weigh the importance of each token relative to others. This allows the model to focus on key phrases and capture dependencies between words.

<Frame>
  ![The image outlines three steps of attention mechanisms for understanding text: processing text with self-attention, focusing on different parts of the prompt, and identifying the most important parts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879326/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/attention-mechanisms-text-processing-steps.jpg)
</Frame>

For the prompt “a red apple next to a green banana,” attention disentangles color attributes and models their spatial arrangement.

## 4. Image Token Generation

Once text embeddings are ready, the decoder predicts image tokens. Each token represents discrete visual elements such as shape, color, or texture.

<Frame>
  ![The image shows a step in a process titled "Step 04: Image Token Generation," with the phrase "A CAT WEARING SUNGLASSES" and options labeled Structure, Appearance, Sunglasses, and Background.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879326/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/step-04-image-token-generation-cat-sunglasses.jpg)
</Frame>

In our example, DALL·E generates tokens for structure (cat silhouette), appearance (fur color), accessory (sunglasses), and background.

## 5. Image Decoding

Image tokens are converted into pixel values through autoregressive decoding. Pixels are generated sequentially, ensuring smooth transitions and detailed structure.

<Frame>
  ![The image outlines the process of image decoding in four steps, including pixel value decoding, autoregressive generation, pixel generation for coherent images, and creating high-resolution images based on visual-text relationships.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879327/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/image-decoding-process-four-steps.jpg)
</Frame>

<Callout icon="lightbulb">
  Typical output resolutions are 512×512 or 1024×1024. You can adjust this setting via API parameters.
</Callout>

## 6. Transforming Prompts into Visual Features

DALL·E categorizes tokens into three visual feature types:

| Token Type        | Role                                         |
| ----------------- | -------------------------------------------- |
| Object Tokens     | Main subjects (e.g., “cat,” “cabin”)         |
| Attribute Tokens  | Qualities (e.g., “red,” “cozy,” “snowfall”)  |
| Positional Tokens | Spatial relations (e.g., “next to,” “above”) |

<Frame>
  ![The image is a diagram titled "Converting Text to Visual Features – Examples," showing three categories: Object Tokens, Attribute Tokens, and Positional Tokens, each with examples like "Cat," "Red," and descriptions of their roles.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879328/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/converting-text-visual-features-diagram.jpg)
</Frame>

Self-attention then prioritizes these features for accurate image generation.

<Frame>
  ![The image explains the relationship between input prompts and generated images in DALL-E, highlighting how attention mechanisms help prioritize input parts in the generation process.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879333/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/dall-e-input-prompts-image-relationship.jpg)
</Frame>

*For “a blue bird sitting on a branch,” attention focuses on the bird–branch relationship to ensure correct placement.*

## 7. Image Patch Generation

Finally, DALL·E composes the image patch by patch. Each patch is generated based on the visual feature tokens. After prediction, patches are stitched together and refined at the pixel level.

<Frame>
  ![The image illustrates "Image Patch Generation," showing a table of tokens and a list explaining the process of generating a final image in patches, with each patch representing a portion of the image.](../../../../images/kodekloud.com/kk-media/image/upload/v1752879334/notes-assets/images/Introduction-to-OpenAI-Understanding-DALL-E-Text-to-Image-Generation/image-patch-generation-tokens-table.jpg)
</Frame>

<Callout icon="triangle-alert">
  If post-processing is skipped, patch seams may become visible. Always apply smoothing or filtering for production-ready images.
</Callout>

## Links and References

* [OpenAI DALL·E 2](https://openai.com/product/dall-e-2)
* [Transformer Architecture (Vaswani et al.)](https://arxiv.org/abs/1706.03762)
* [Byte-Pair Encoding (BPE) Explained](https://huggingface.co/learn/nlp-course/chapter7/7)
* [Self-Attention Mechanism Overview](https://www.tensorflow.org/text/guide/transformer)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/introduction-to-openai/module/d76ba88f-ebc6-4d12-8aa5-9359bc23be72/lesson/d8bfcd6c-7fb2-4377-a306-10430f72e272" />
</CardGroup>
