# task_1_zero_shot.py
def main(llm):
    vague_prompt = "Write a privacy policy."
    vague_response = llm.invoke(vague_prompt)
    print(f"\nVague response preview: {vague_response.content[:100]}...")
    print("Problem: Too generic, not useful for our company!")

    print("\n✅ Specific Zero-Shot Prompting")
    specific_prompt = (
        "Write a 200-word data privacy policy for European customers "
        "in compliance with the [General Data Protection Regulation (GDPR)](https://gdpr.eu/). "
        "Include retention (30 days), data subject rights, and data transfer rules."
    )
    specific_response = llm.invoke(specific_prompt)
    print(f"\nSpecific response preview: {specific_response.content[:200]}...")
    print("Success: Clear, actionable, company-specific!")

    print("\n📊 Comparison Results:")
    print(f"Vague response length: {len(vague_response.content)} characters")
    print(f"Specific response length: {len(specific_response.content)} characters")
```

Example console output (trimmed):

```text theme={null}
Vague response preview: We are committed to protecting your privacy...
Problem: Too generic, not useful for our company!

✅ Specific Zero-Shot Prompting

Specific response preview: We are committed to protecting the privacy of our European customers in accordance with the GDPR. This policy covers...
Success: Clear, actionable, company-specific!

📊 Comparison Results:
Vague response length: 263 characters
Specific response length: 1369 characters
```

Zero-shot best practices:

* State the exact task and desired length.
* Define context (jurisdiction, audience, domain).
* List required sections or bullet points the output must include.
* Constrain format where necessary (e.g., JSON, Markdown, or numbered sections).

***

## Task 2 — One-Shot Prompting

One-shot prompting supplies a single example that demonstrates the desired format, tone, or structure. It’s useful when you want the model to reproduce a template or layout across many inputs.

Example: Provide a refund policy template as the one-shot example and ask the model to produce a remote work policy using the same structure.

One-shot example (refund policy template):

```text theme={null}
1. Eligibility: Within 30 days of purchase
2. Conditions: Product unused and in original packaging
3. Process: Submit request via support@company.com
4. Timeline: Refund processed within 5-7 business days
5. Exceptions: Digital products and custom orders non-refundable
```

Then ask the model:

```text theme={null}
🧪 Using the template above, create a REMOTE WORK POLICY for our company with the same five-section format.
```

Generated result (example):

```text theme={null}
REMOTE WORK POLICY
1. Eligibility: Employees approved by management for remote work
2. Conditions: Maintain a dedicated workspace and reliable internet connection
3. Process: Submit remote work request to HR at hr@company.com
4. Timeline: Approval communicated within 3 business days
5. Exceptions: Positions requiring on-site presence and confidential projects not eligible for remote work
```

One-shot benefits:

* Enforces a single-template formatting.
* Fast to set up for repetitive, structured documents.
* Good when you want to preserve a strict layout without many examples.

***

## Task 3 — Few-Shot Prompting

Few-shot prompting gives the model several diverse examples so it can learn format, tone, and response patterns. This technique is ideal for customer support, marketing copy, or any content that requires consistent voice across variations.

<Frame>
  <img alt="A dark-themed screen showing a presentation card titled &#x22;Task 3: Few-Shot Prompting (3 minutes)&#x22; with a definition and bullet points explaining why multiple examples matter. On the right is a file/sidebar list with Python files like task_2_one_shot.py and task_3_few_shot.py." />
</Frame>

Example few-shot training set (customer support style examples):

```text theme={null}
Customer Issue: The product arrived damaged.
Support Response: I'm so sorry to hear that. Please send a photo to support@company.com so we can open a replacement or refund immediately. We'll respond within 2 business days.

Customer Issue: I haven't received my order.
Support Response: I apologize for the delay. Please share your order number and I'll check the shipping status. Expect an update within 24 hours.

Customer Issue: I need to change my billing address.
Support Response: Thanks for letting us know. Please confirm the new billing address and we'll update it for future invoices. This change will reflect within 1 business day.
```

New prompt and model output:

```text theme={null}
🧾 New customer issue:
Product not working

🤖 AI Response:
I'm sorry to hear the product isn't working as expected. Could you please provide a brief description of the issue and any error messages? Meanwhile, I'll check if there are known troubleshooting steps or recalls related to your product.
```

Quick response analysis example:

```text theme={null}
✓ Shows empathy: True
✓ Takes action (asks for next steps): True
✓ Provides timeline: False
Quality Score: 2/3
```

Few-shot advantages:

* Learns subtleties of tone and phrasing across examples.
* Keeps responses consistent across agents or channels.
* Reduces need for labeled fine-tuning for many use-cases.

***

## Task 4 — Chain-of-Thought (CoT) Prompting

Chain-of-Thought prompting encourages the model to expose intermediate reasoning steps. This produces more accurate and defensible answers for complex or multi-step tasks.

Use CoT when you need the model to enumerate assumptions, weigh options, or provide a stepwise troubleshooting path.

Example LangChain prompt templates (fixed and syntactically correct):

```python theme={null}
# task_4_chain_of_thought.py
from langchain.prompts import PromptTemplate, FewShotPromptTemplate

# Example list of examples (each is a dict with 'input' and 'output')
examples = [
    {"input": "User cannot connect to WiFi", "output": "Step 1: Ask for error details. Step 2: Confirm SSID and password. Step 3: Suggest restart and driver update."},
    {"input": "App crashes on startup", "output": "Step 1: Ask for device and OS. Step 2: Ask for app version and logs. Step 3: Suggest clearing cache or reinstalling."},
    {"input": "Invoice not received", "output": "Step 1: Verify order number. Step 2: Confirm billing email. Step 3: Resend invoice and confirm delivery."}
]

# Create the example template
example_prompt = PromptTemplate(
    template="Customer Issue: {input}\nSupport Response: {output}",
    input_variables=["input", "output"]
)

# Create the few-shot prompt template
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="You are a helpful customer support agent. Here are examples of how to break problems down step-by-step:\n\n",
    suffix="Customer Issue: {input}\nSupport Response:",
    input_variables=["input"]
)

def generate_support_response(llm, user_issue):
    prompt = few_shot_prompt.format(input=user_issue)
    response = llm.invoke(prompt)
    return response.content
```

Simple CoT instruction pattern:

```text theme={null}
When solving the problem, think through it step-by-step:
1. Identify the main issue.
2. List possible causes.
3. Propose troubleshooting steps in order of likelihood.
4. Provide a recommended next action.
```

CoT best practices:

* Provide worked examples that demonstrate intermediate steps.
* Ask the model to enumerate assumptions and order steps by likelihood.
* Use models/configurations that support longer contexts for full reasoning chains.
* Prefer CoT when correctness and traceability matter.

***

## Task 5 — Technique Showdown (Comparison)

Compare the techniques by running the same task through each style and evaluating differences in structure, tone, and completeness.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Task 5: Technique Showdown&#x22; listing and briefly describing four prompting techniques (Zero-Shot, One-Shot, Few-Shot, Chain-of-Thought) with a highlighted key insight box; a colorful cursor points at &#x22;Chain-of-Thought.&#x22; A file sidebar with task filenames is visible along the right edge of the screen." />
</Frame>

Example Python script comparing all four techniques:

```python theme={null}
# task_5_comparison.py
def main(llm):
    test_problem = "Create an employee remote work policy"
    print(f"🧪 Test Problem: {test_problem}\nTesting all 4 prompting techniques...\n")

    results = {}

    # 1. ZERO-SHOT PROMPTING
    print("1️⃣ Zero-Shot Prompting")
    zero_shot_result = llm.invoke(test_problem)
    results["zero_shot"] = zero_shot_result.content
    print(f"Response length: {len(zero_shot_result.content)} characters")
    print(f"Preview: {zero_shot_result.content[:100]}...\n")

    # 2. ONE-SHOT PROMPTING
    print("2️⃣ One-Shot Prompting")
    one_shot_example = (
        "REMOTE WORK POLICY\n"
        "1. Eligibility: ...\n"
        "2. Conditions: ...\n"
        "3. Process: ...\n"
        "4. Timeline: ...\n"
        "5. Exceptions: ..."
    )
    one_shot_prompt = one_shot_example + "\n\nPlease create a remote work policy in the same format for our company."
    one_shot_result = llm.invoke(one_shot_prompt)
    results["one_shot"] = one_shot_result.content
    print(f"Response length: {len(one_shot_result.content)} characters\n")

    # 3. FEW-SHOT PROMPTING
    print("3️⃣ Few-Shot Prompting")
    few_shot_prompt = "Examples:\n" + one_shot_example + "\n\n[additional examples]\n\nNow create a remote work policy:"
    few_shot_result = llm.invoke(few_shot_prompt)
    results["few_shot"] = few_shot_result.content
    print(f"Response length: {len(few_shot_result.content)} characters\n")

    # 4. CHAIN-OF-THOUGHT PROMPTING
    print("4️⃣ Chain-of-Thought Prompting")
    cot_prompt = (
        "You are an expert HR advisor. When drafting the policy, think through it step-by-step:\n"
        "1. Identify objectives.\n2. Define eligibility and conditions.\n3. Describe the process and timelines.\n4. Note exceptions and compliance.\n\n"
        "Now create an employee remote work policy based on that reasoning."
    )
    cot_result = llm.invoke(cot_prompt)
    results["chain_of_thought"] = cot_result.content
    print(f"Response length: {len(cot_result.content)} characters\n")

    # Comparative summary
    for k, v in results.items():
        print(f"{k}: {len(v)} characters")
```

Typical comparative observations:

* Zero-Shot: fastest but may miss company specifics or required sections.
* One-Shot: enforces a strict format from a single template.
* Few-Shot: matches tone and variations across multiple examples.
* Chain-of-Thought: produces longer, structured reasoning and more comprehensive policies.

Comparison table (quick reference):

| Technique        | Primary Strength     | When to Use                            | Example Outcome                        |
| ---------------- | -------------------- | -------------------------------------- | -------------------------------------- |
| Zero-Shot        | Fast, minimal setup  | Quick answers, prototypes              | Short, generic policy                  |
| One-Shot         | Template enforcement | When strict format matters             | Policy that matches template exactly   |
| Few-Shot         | Tone + consistency   | Customer support, brand voice          | Consistent, styled responses           |
| Chain-of-Thought | Detailed reasoning   | Complex troubleshooting, policy design | Multi-step, defensible recommendations |

<Frame>
  <img alt="A screenshot of a coding tutorial popup titled &#x22;Congratulations!&#x22; listing mastered prompting techniques (zero-shot, one-shot, few-shot, chain-of-thought) and a key takeaway. To the right is a code editor/file explorer showing Python files such as task_5_comparison.py." />
</Frame>

***

## Wrap-up and Practical Tips

By completing these exercises you should now be able to:

* Choose the right prompting technique based on goals (speed, format, tone, or reasoning).
* Design explicit constraints (format, length, audience) to get predictable outputs.
* Use One-Shot and Few-Shot prompts to enforce structure and brand voice.
* Use Chain-of-Thought when you need traceable, stepwise reasoning.

Quick checklist before running experiments:

* Provide role/context to the model (e.g., "You are an expert HR advisor").
* Include required sections and constraints.
* Use examples to teach format or tone when needed.
* Keep a simple evaluation rubric (empathy, actionability, timeline) to compare outputs.

Links and References

* [LangChain — Learn with KodeKloud](https://learn.kodekloud.com/user/courses/langchain)
* [General Data Protection Regulation (GDPR)](https://gdpr.eu/)
* [OpenAI API Documentation](https://platform.openai.com/docs)

Recommended next steps:

* Run the provided tasks in your environment and compare outputs across multiple model sizes.
* Iterate on prompts and evaluate with a small rubric (correctness, format, tone).
* Automate comparisons with simple scripts (as shown in task\_5\_comparison.py) to measure improvements over prompt versions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/fc768b46-c135-4b58-8e50-d67119a89254" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/ai-agents-fundamentals/module/dd5e8998-51f1-4352-82a5-3414cdc3299c/lesson/fe1ff954-9097-4b13-90d4-e17d0cc3ab62" />
</CardGroup>


# Practice Labs Your First AI API Call

Source: https://notes.kodekloud.com/docs/AI-Agents-Fundamentals/AI-Agents-Part-1/Practice-Labs-Your-First-AI-API-Call/page

Tutorial guiding users through setting up the OpenAI Python client, making chat API calls, extracting responses, and estimating token usage and costs

Let's start with the lab files you'll work through:

```text theme={null}
README.md
task_1_import_setup.py
task_2_client_initialization.py
task_3_api_call_explained.py
task_4_extract_response.py
task_5_tokens_and_costs.py
verify_environment.py

root@controlplane ~/code via ⬢ v3.12.3 ❯
```

In this lesson you'll learn how to make your first AI API calls with the OpenAI Python client. The goal is practical: verify your environment, connect to the API, make a chat completion request, extract the assistant's reply, and inspect token usage and cost — all in progressive steps.

<Frame>
  <img alt="A tutorial screen titled &#x22;Mission: Your First AI API Calls&#x22; showing a &#x22;Welcome, Beginner!&#x22; message and a list of six progressive steps for making AI API calls. A dark sidebar on the right displays filenames for related Python tasks." />
</Frame>

## 1 — Verify the environment

Before writing code, verify that your runtime is ready: activate the virtual environment, confirm Python is available, ensure the OpenAI package is installed, and verify your API keys are present. Run these commands in the lab VM:

```bash theme={null}
source /root/venv/bin/activate
python3 /root/code/verify_environment.py
```

If verification succeeds, the script prints readiness checks and exits. If something fails, re-check your virtual environment and that packages (like the OpenAI Python package) are installed.

Environment variables commonly used in these examples:

| Environment Variable | Purpose                                                        |
| -------------------- | -------------------------------------------------------------- |
| OPENAI\_API\_KEY     | Your secret API key (keep it private)                          |
| OPENAI\_API\_BASE    | Optional API base URL (use when pointing to a custom endpoint) |

## What is OpenAI?

[OpenAI](https://openai.com) builds ChatGPT and families of large language models (e.g., GPT-4, GPT-4.1 Mini, GPT-3.5). The OpenAI Python client is the bridge between your Python code and the API.

<Frame>
  <img alt="A dark-themed screenshot of a tutorial titled &#x22;What is OpenAI?&#x22; listing OpenAI models (GPT-4, GPT-4.1‑mini, GPT-3.5) and describing the OpenAI Python library. A file sidebar with example Python task filenames is visible on the right." />
</Frame>

## Task 1 — Import required libraries

Open `task_1_import_setup.py`. You need to import the OpenAI client library and the `os` module to read environment variables. The following file shows the required imports and writes a completion marker for the lab system.

```python theme={null}
#!/usr/bin/env python3
"""
Task 1: Import Required Libraries
Learn what libraries we need for AI API calls.
"""
