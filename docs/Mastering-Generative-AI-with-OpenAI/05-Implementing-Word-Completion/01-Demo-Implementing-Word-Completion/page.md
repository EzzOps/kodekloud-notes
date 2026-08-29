# Demo Implementing Word Completion

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Implementing-Word-Completion/Demo-Implementing-Word-Completion/page

This article teaches how to use the OpenAI ChatCompletion API in Jupyter Notebook for generating product descriptions and HTML snippets.

In this hands-on tutorial, you'll learn how to leverage the OpenAI ChatCompletion API inside a Jupyter Notebook to generate product descriptions, concise summaries, and HTML snippets. By the end, you'll have a reusable Python helper function and three prompt patterns for marketing automation.

## Prerequisites

* Python 3.x
* [openai Python package](https://pypi.org/project/openai/)
* [Jupyter Notebook](https://jupyter.org/)
* An OpenAI API key

***

## 1. Setup: Import Modules & Configure API Key

Begin by importing the required libraries and setting your API key as an environment variable.

```python theme={null}
import os
import openai
