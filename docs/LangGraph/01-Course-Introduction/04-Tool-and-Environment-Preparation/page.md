# Tool and Environment Preparation

Source: https://notes.kodekloud.com/docs/LangGraph/Course-Introduction/Tool-and-Environment-Preparation/page

Guide to preparing a Python development environment for LangGraph, installing dependencies, configuring virtual environments and API keys, and running a quick OpenAI integration test.

Before diving into LangGraph, confirm your local environment is ready. This guide keeps things lightweight and beginner-friendly while ensuring reproducible setups for development and experimentation.

Minimum requirements

* Python 3.10 or later
* A code editor or Jupyter notebook (Jupyter is excellent for inline experimentation)
* A virtual environment (venv or Conda) to isolate dependencies
* A few Python packages (listed below)

We recommend Jupyter Notebook for interactive experimentation and Visual Studio Code for larger projects. Always use a virtual environment to avoid dependency conflicts.

<Frame>
  <img alt="The image shows a terminal interface with options to launch Python 3.10+, Jupyter Notebook, and VSCode, along with &#x22;venv&#x22; and &#x22;conda&#x22; highlighted below." />
</Frame>

## Install system prerequisites and pip

First, check whether `pip` is available:

```bash theme={null}
pip --version
```

If `pip` is missing, install it using your distribution's package manager. Use the appropriate command for your platform:

|                     Platform | Install pip                                              |
| ---------------------------: | -------------------------------------------------------- |
|              Ubuntu / Debian | `sudo apt update`<br />`sudo apt install -y python3-pip` |
| RHEL / CentOS / Rocky / Alma | `sudo dnf install -y python3-pip`                        |
|                   Arch Linux | `sudo pacman -S python-pip`                              |

Once `pip` is available, proceed to install the Python packages.

## Install core Python packages

Install the minimal required packages and a few recommended utilities. The table below summarizes purpose and installation.

| Package(s)                         | Purpose                                                             |
| ---------------------------------- | ------------------------------------------------------------------- |
| `langgraph`, `langchain`, `openai` | Core libraries for building LLM workflows and calling OpenAI models |
| `tqdm`                             | Progress bars for long-running loops                                |
| `rich`                             | Pretty console output for better CLI readability                    |
| `langsmith`                        | Observability and tracing for LangChain/LangGraph workflows         |
| `python-dotenv`                    | Load local `.env` files during development                          |

Install the packages:

```bash theme={null}
