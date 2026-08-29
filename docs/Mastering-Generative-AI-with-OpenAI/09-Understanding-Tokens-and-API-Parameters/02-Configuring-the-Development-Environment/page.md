# Configuring the Development Environment

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Understanding-Tokens-and-API-Parameters/Configuring-the-Development-Environment/page

Prepare your local machine to experiment with the OpenAI API by installing Python, setting up a virtual environment, and verifying the setup.

Prepare your local machine to experiment with the OpenAI API. We’ll cover installing Python, setting up a virtual environment, installing required packages, obtaining your API key, exporting it as an environment variable, and verifying everything with `curl` and Jupyter Notebook.

**Workflow Overview**

1. Install Python & pip
2. Create and activate a Python virtual environment
3. Install the OpenAI and Jupyter packages
4. Obtain your OpenAI API key
5. Export `OPENAI_API_KEY`
6. Verify with `curl` and in Jupyter

![The image outlines six steps for setting up a Python environment with OpenAI and Jupyter, including installing Python, creating a virtual environment, installing modules, obtaining an API key, setting an environment variable, and testing the setup.](https://kodekloud.com/kk-media/image/upload/v1752881563/notes-assets/images/Mastering-Generative-AI-with-OpenAI-Configuring-the-Development-Environment/python-environment-setup-openai-jupyter.jpg)

***

## 1. Install Python

Download and install Python 3.10+ for your operating system from [python.org/downloads](https://python.org/downloads). After installation, verify your setup:

```bash theme={null}
python -V
