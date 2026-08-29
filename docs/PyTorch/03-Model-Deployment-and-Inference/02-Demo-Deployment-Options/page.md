# Demo Deployment Options

Source: https://notes.kodekloud.com/docs/PyTorch/Model-Deployment-and-Inference/Demo-Deployment-Options/page

This demonstration covers the process of deploying ONNX models, including installation, model modification, export, inference, and output mapping.

Welcome to the first demonstration in our deployment series. In this guide, we provide a comprehensive overview of working with ONNX and the ONNX Runtime. This demonstration will walk you through installing the necessary modules, modifying a pretrained model, exporting it to ONNX format, preparing input for inference, running the inference, and finally mapping the output to a human-readable label.

<Callout icon="lightbulb">
  ONNX is an open standard format that allows interoperability of models across different platforms. With ONNX Runtime, you can execute these models efficiently in various deployment scenarios.
</Callout>

***

## Installing ONNX and ONNX Runtime

Begin by installing both ONNX and the ONNX Runtime. For this demo, we assume that the required modules are already installed. If you encounter any issues, install the modules using pip and restart your notebook.

```python theme={null}
