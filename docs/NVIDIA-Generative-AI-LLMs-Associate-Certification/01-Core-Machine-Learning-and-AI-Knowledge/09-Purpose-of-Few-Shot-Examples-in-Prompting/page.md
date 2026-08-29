# Purpose of Few Shot Examples in Prompting

Source: https://notes.kodekloud.com/docs/NVIDIA-Generative-AI-LLMs-Associate-Certification/Core-Machine-Learning-and-AI-Knowledge/Purpose-of-Few-Shot-Examples-in-Prompting/page

Explains that few-shot examples in prompts steer LLMs’ output format, tone, and behavior via in-context learning without changing model weights or reducing inference cost.

Question 6.

In prompt engineering for LLMs, what is the primary purpose of using few-shot examples?

* To increase the model's vocabulary?
* To guide the model's response format and style?
* To reduce the computational cost of inference?
* Or to fine-tune the model weights in real time?

Answer: Few-shot — To guide the model's response format and style.

Few-shot examples supply in-context demonstrations that steer the LLM toward the expected format, tone, and approach for a task. They do not alter the model's internal weights or vocabulary and do not reduce inference cost. Instead, they provide examples that the model uses at inference time to infer the desired mapping from inputs to outputs.

<Frame>
  <img alt="The image contains a question and answer about the primary purpose of using &#x22;few-shot&#x22; examples in prompt engineering for LLMs, citing guiding the model's response format and style as the purpose." />
</Frame>

Example

The following few-shot prompt gives the model three demonstration pairs that map plain-English instructions to shell commands. The fourth entry is the new instruction (the query). The model should follow the demonstrated pattern and produce the corresponding command:

```bash theme={null}
