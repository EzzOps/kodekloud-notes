# Example 1: Simple arithmetic in a notebook cell
a = 10
b = 5
print(a + b)
# Output:
# 15
```

```python theme={null}
# Example 2: Iterate over a list of prices and print each
prices = [50000, 60000, 65000, 44000, 127000]
for price in prices:
    print(f'Current price is {price}')
# Output:
# Current price is 50000
# Current price is 60000
# Current price is 65000
# Current price is 44000
# Current price is 127000
```

***

## Visualizations and documentation

A major strength of Jupyter is inline rendering of visualizations. Libraries such as Matplotlib and Seaborn render charts and plots directly into notebook output cells. These visual outputs are preserved in the .ipynb file (unless cleared), which makes notebooks ideal for combining code, visual results, and narrative in one shareable document.

Common visualization types used in data science:

| Visualization                     | Use case                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------- |
| Correlation heatmap               | Understand relationships between numeric features; useful for feature selection |
| Scatter plot                      | Inspect relationships and outliers (e.g., house size vs. price)                 |
| Line charts, histograms, boxplots | Time series, distributions, and data summaries                                  |

<Frame>
  <img alt="A presentation slide titled &#x22;Efficient Results With Jupyter Notebooks&#x22; showing two Jupyter notebook outputs side-by-side: a correlation heatmap of housing features on the left and a scatter plot of house size vs. price on the right. Captions beneath read &#x22;Correlation Heatmap&#x22; and &#x22;House Size vs Price Scatter Plot.&#x22;" />
</Frame>

Benefits of using Jupyter for data science:

* Inline visualizations and instant feedback from code execution.
* Integration with many cloud environments (e.g., Google Colab, AWS SageMaker, Databricks).
* Self-documenting workflows: combine code cells with markdown for clear explanations, hypotheses, and reproducible steps.

<Frame>
  <img alt="A presentation slide titled &#x22;Efficient Results With Jupyter Notebooks&#x22; showing three rounded boxes labeled 01 Inline Visualizations, 02 Cloud Integration, and 03 Self-Documenting. Each box briefly notes benefits like instant feedback, compatibility with Google Colab/AWS/SageMaker/Databricks, and combining code, results, and notes." />
</Frame>

Jupyter is widely used across industry (for example Airbnb, NASA, and Netflix) for exploratory analysis, model development, and collaborative data science projects.

***

## Summary

Key takeaways from this lesson:

* Ways to run Jupyter: locally (pip or Anaconda), in containers, inside IDEs, or as hosted cloud services (e.g., AWS SageMaker).
* The browser is always the user interface for Jupyter; the server executes code and stores outputs.
* Notebook cells can be code or markdown; code cell stdout and visual outputs are captured inline in the .ipynb file.
* JupyterLab is a modern, tabbed interface with extension support; SageMaker Studio builds on JupyterLab to provide a full ML IDE.
* SageMaker supports legacy Notebook Instances and the newer Studio — prefer Studio for new projects.

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; showing four numbered points in a vertical layout. The points summarize Jupyter notebooks and JupyterLab features (local/remote browser access, code/markdown support, multi-notebook extensibility) and note that SageMaker provides a hosted Jupyter/SageMaker Studio." />
</Frame>

A hands-on demo using JupyterLab in AWS SageMaker Studio will be provided later in the course.

## Links and references

* JupyterLab: [https://jupyter.org/](https://jupyter.org/)
* Anaconda distribution: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)
* Docker: [https://www.docker.com/](https://www.docker.com/)
* AWS SageMaker overview and resources: [https://learn.kodekloud.com/user/courses/aws-sagemaker](https://learn.kodekloud.com/user/courses/aws-sagemaker)
* Matplotlib: [https://matplotlib.org/](https://matplotlib.org/)
* Seaborn: [https://seaborn.pydata.org/](https://seaborn.pydata.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-sagemaker/module/8dba4cbc-6eb7-4985-b97a-c5b7e6d23161/lesson/e054507e-0287-40f2-8231-4301df3bbfa7)


# Introduction to Jupyter Notebooks

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-Introduction/Introduction-to-Jupyter-Notebooks/page

Overview of Jupyter Notebooks as interactive, web-based tools for exploratory data analysis, visualization, reproducible experiments, collaboration, and comparisons with REPLs and IDEs

This lesson explains what Jupyter Notebooks solve, why data scientists favor them for experimentation and collaboration, how to run them (hosted services or locally), and their primary benefits.

The dominant language for data science is Python. To develop models and analyze data you need an appropriate Python environment. Several options exist, each with trade-offs depending on whether your goal is quick experimentation, reproducible analysis, or production-quality development.

## Problem: Python REPL (interactive shell)

A minimal starting point is the Python interactive shell (a REPL — Read, Evaluate, Print Loop). If Python is installed locally, running `python` opens a prompt where you can try commands like `print("hello")` and get immediate results. This is great for quick experiments and learning, but it doesn’t scale for multiline, reusable, or version-controlled code. For moderate-length scripts (tens or hundreds of lines) you typically use Python script files and an editor or IDE instead.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Need Python Environment&#x22; showing the Python logo and the label &#x22;Python shell — Read, Evaluation, Print Loop.&#x22; The slide notes the shell runs commands and shows results instantly, is good for quick tests but not for saving code, and recommends Python scripts for reusable code." />
</Frame>

## Alternatives: IDEs

Integrated development environments (IDEs) supply many productivity features that help when building applications:

* Code completion and parameter hints
* Syntax highlighting and linting
* Debugging (breakpoints, step over/into, variable watches)
* AI-assisted suggestions in some editors

Popular IDEs include Visual Studio Code, IDLE, and PyCharm. IDEs are excellent for production applications (Flask, Django) and for advanced debugging, but they do not always match the exploratory, iterative needs of data analysis.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Need Python Environment&#x22; showing logos for VS Code, Python IDLE, and IntelliJ PyCharm. To the right are three points: code assistance, debugging tools, and an efficiency boost for faster development." />
</Frame>

## Why data scientists need something different

Data exploration typically requires multiple tools and rich visualizations to understand feature distributions and correlations. Libraries such as [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/) are commonly used to create charts that drive feature engineering and model design.

REPLs and traditional IDEs can be limiting for reproducibility and collaborative experiments. To let colleagues reproduce your analysis or inspect "how you got that result," you need an environment that preserves code, outputs (including charts), and narrative explanation together.

<Frame>
  <img alt="A presentation slide titled &#x22;Problem: Need Python Environment&#x22; showing three numbered panels that say: data exploration requires multiple Python tools; visualization and annotation help document findings; and REPLs/IDEs are not enough for reproducibility." />
</Frame>

## Solution: Jupyter Notebooks

Jupyter Notebooks are an interactive, web-based environment designed for experimentation and sharing. Key features:

* Code organized into cells so you can run small chunks independently.
* Inline outputs: text, tables, and visualizations display directly below code cells.
* Persistence of inputs and outputs for reproducible experiments.
* Markdown cells let you add narrative, headings, and LaTeX math for clear documentation.

This combination of executable code, visual output, and descriptive text supports scientific-style workflows: state a hypothesis, run experiments, visualize results, iterate, and document findings.

<Frame>
  <img alt="A presentation slide titled &#x22;Solution: Jupyter Notebooks&#x22; showing the Jupyter logo on the left and three brief points on the right: code runs in chunks (&#x22;cells&#x22;), it's interactive/REPL-like with saved inputs/outputs, and a persistent interface that keeps code, results, and experiments." />
</Frame>

## Notebook structure and cells

Notebooks contain two primary cell types:

* Code cells: execute Python and display standard output inline. Visualizations from Matplotlib or Seaborn are rendered directly and saved with the notebook.
* Markdown cells: document steps, reasoning, and include LaTeX-compatible math.

Run cells interactively (for example, Shift+Enter). Each execution yields an execution count (e.g., In \[1], In \[2]) that reflects the order cells were run. Re-run cells as you iterate to update outputs.

<Frame>
  <img alt="A slide titled &#x22;Solution: Jupyter Notebooks&#x22; showing a boxed diagram of stacked colored blocks illustrating the Jupyter Notebook cell execution process. The blocks are labeled Python Code, Standard Console Output, Markdown Code including LaTeX, and Standard Console Output including charts." />
</Frame>

## Example — interactive notebook cells

A short example illustrating two code cells and their outputs. When executed in a notebook the printed results appear inline and are persisted with the .ipynb file.

```python theme={null}
