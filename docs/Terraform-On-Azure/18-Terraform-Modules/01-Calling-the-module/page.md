# Calling the module

Source: https://notes.kodekloud.com/docs/Terraform-On-Azure/Terraform-Modules/Calling-the-module/page

Explains how to call and reuse Terraform modules from a root configuration, with Azure examples showing module sources, inputs, outputs, initialization, planning, and reuse.

Now that you understand how a module is structured internally, the next step is learning how to call and reuse it from a calling configuration (typically the root module). A module sitting in a folder does nothing by itself — Terraform only evaluates a module when a configuration references it with a `module` block.

This guide walks through a concise, practical example of calling a local module, explains the execution flow, and shows how to pass inputs and expose outputs so different modules can interoperate.

## Basic example: create a module instance

A simple module call from the root module looks like this:

```hcl theme={null}
