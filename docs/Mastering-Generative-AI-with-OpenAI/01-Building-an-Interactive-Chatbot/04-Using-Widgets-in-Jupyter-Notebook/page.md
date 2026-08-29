# Using Widgets in Jupyter Notebook

Source: https://notes.kodekloud.com/docs/Mastering-Generative-AI-with-OpenAI/Building-an-Interactive-Chatbot/Using-Widgets-in-Jupyter-Notebook/page

Enhance Jupyter Notebook with interactive widgets and layouts using Panel for dynamic interfaces and explorations.

Enhance your Jupyter Notebook with interactive widgets and layouts using [Panel](https://panel.holoviz.org/). Panel makes it easy to build dynamic interfaces directly in your notebook, turning static analyses into interactive explorations.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Step 1: Install and Enable Panel](#step-1-install-and-enable-panel)
* [Step 2: Import Panel and Define Widgets](#step-2-import-panel-and-define-widgets)
* [Step 3: Create an Event Handler](#step-3-create-an-event-handler)
* [Step 4: Display Widgets in a Layout](#step-4-display-widgets-in-a-layout)
* [Widget Reference Table](#widget-reference-table)
* [Additional Resources](#additional-resources)

## Prerequisites

* Jupyter Notebook (or [JupyterLab](https://jupyterlab.readthedocs.io/))
* Python 3.7+
* Panel library

<Callout icon="lightbulb">
  If you haven’t installed Panel yet, run:

  ```bash theme={null}
  pip install panel
  ```
</Callout>

## Step 1: Install and Enable Panel

Start your notebook and enable Panel’s extension:

```python theme={null}
import panel as pn
