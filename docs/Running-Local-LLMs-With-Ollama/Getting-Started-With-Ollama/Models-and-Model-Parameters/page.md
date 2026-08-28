# Models and Model Parameters

Source: https://notes.kodekloud.com/docs/Running-Local-LLMs-With-Ollama/Getting-Started-With-Ollama/Models-and-Model-Parameters/page

This guide explores Ollamas supported models, their specifications, and how to choose the right one for your project.

We’ve installed **Ollama** locally and launched our first large language model (LLM). In this guide, we’ll explore the full catalog of models that Ollama supports and learn how to interpret their technical specifications. Whether you’re a beginner or an experienced developer, you don’t need deep AI knowledge to get started—our analogies and examples will clarify each concept.

To browse all available models, visit [ollama.com/search](https://ollama.com/search). Below, we’ll show you how to search for models, inspect their details, and choose the right one for your project.

Consider **Jane**, a developer building a local AI assistant. When deciding on a model, she balances:

* Output quality (accuracy, coherence)
* Computational requirements (RAM, CPU/GPU)
* Hardware availability (laptop vs. server)

Ollama’s catalog includes families like Meta’s LLaMA, QWQ, Mistral, and more. You’ll see multiple versions—for example, LLaMA 3.3, 3.2, and 3.1. What do those numbers mean? Let’s dive in.

If you click a model on the website, you’ll see a detailed info page. For instance, on **LLaMA 3.2**, the specifications include its architecture, parameter count, and quantization format. You can also retrieve this info locally:

```bash theme={null}
ollama run llama-3.2
