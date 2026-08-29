# Demo Building Dynamic Context with Custom Data Part 1

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Using-Word-Embeddings-For-Dynamic-Context/Demo-Building-Dynamic-Context-with-Custom-Data-Part-1/page

This tutorial creates a dynamic context for a chatbot using custom data from the Oscar Awards dataset.

In this tutorial, we’ll create a **dynamic context** for a chatbot by enriching prompts with custom data. We’re using the [“Oscar Award, 1927 – 2023” dataset from Kaggle][Kaggle Dataset], which includes every nominee and winner by year, ceremony number, category, nominee name, film, and winner status.

![The image shows a Kaggle dataset page titled "The Oscar Award, 1927 - 2023," displaying a CSV file with columns for year, ceremony, category, name, film, and winner status.](https://kodekloud.com/kk-media/image/upload/v1752881577/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Demo-Building-Dynamic-Context-with-Custom-Data-Part-1/oscar-award-dataset-1927-2023.jpg)

## 1. Environment Setup

First, install dependencies and configure your API key.

```bash theme={null}
pip install pandas numpy openai
```

> **lightbulb** Make sure your `OPENAI_API_KEY` is set in the environment:

  ```bash theme={null}
  export OPENAI_API_KEY="your_api_key_here"
  ```

Then, load the Python modules and define helper functions:

```python theme={null}
import os
import pandas as pd
import numpy as np
import openai
