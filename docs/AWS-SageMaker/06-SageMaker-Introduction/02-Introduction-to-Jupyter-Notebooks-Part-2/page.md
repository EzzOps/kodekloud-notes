# Try invoking python3
ubuntu@ip-172-31-1-136:~$ python3
Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
>>> a = 3
>>> b = 4
>>> print(a + b)
7
>>> exit()
```

## 2. Install pip and create a virtual environment (recommended)

On Ubuntu 24.04+ you may need to install pip and the venv helper:

```bash theme={null}
sudo apt update
sudo apt install -y python3-pip python3-venv
```

Verify pip:

```bash theme={null}
ubuntu@ip-172-31-1-136:~$ pip --version
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```

Create and activate an isolated virtual environment to avoid global package conflicts:

```bash theme={null}
python3 -m venv jupyter_env
source jupyter_env/bin/activate
# Prompt will show (jupyter_env) when active
```

<Callout icon="lightbulb">
  Use virtual environments to isolate project dependencies. This keeps system packages clean and prevents conflicting versions across projects.
</Callout>

## 3. Install and run the classic Jupyter Notebook server

Install Jupyter Notebook inside the virtual environment:

```bash theme={null}
pip install jupyter
```

Start the notebook server, binding to all interfaces so you can connect remotely. Disable the automatic browser on the remote server:

```bash theme={null}
jupyter notebook --ip=0.0.0.0 --no-browser
```

The server prints informational lines and one or more access URLs with an authentication token. Example output:

```text theme={null}
[I 2025-03-27 16:12:42.612 ServerApp] Serving notebooks from local directory: /home/ubuntu
[I 2025-03-27 16:12:42.612 ServerApp] Jupyter Server 2.15.0 is running at:
[I 2025-03-27 16:12:42.612 ServerApp] http://ip-172-31-1-136:8888/tree?token=7fa9...f265d487
[I 2025-03-27 16:12:42.616 ServerApp] Use Control-C to stop this server and shut down all kernels.
```

Important: the hostname in the printed URL may show the instance’s private IP or private DNS (not accessible from your laptop). Replace that hostname with the instance’s *public IP* shown in the EC2 console, or use an SSH tunnel to bind the port locally.

<Callout icon="warning">
  Do not expose a Jupyter server directly to the public internet without proper authentication and TLS. Prefer SSH tunneling, a VPN, or secure application endpoints to protect access.
</Callout>

## 4. Connect from a browser, create a notebook, and run cells

Open the corrected URL in your browser (public IP or a tunneled localhost URL). The classic Jupyter file view appears. Create a new Python 3 notebook and try code and markdown cells.

Example code cells and outputs:

```python theme={null}
# Cell 1
a = 6
b = 4
print(a + b)
# Output: 10
```

```python theme={null}
# Cell 2
c = 8
print(c + a)
# Output: 14
```

Switch a cell to Markdown to add narrative:

```markdown theme={null}
# Feature Engineering Code Next
- Prepare features
- Scale and transform
```

Keyboard shortcuts:

* Shift+Enter — run cell and advance.
* Ctrl+Enter — run cell in place.
* Execution order appears as bracket numbers \[1], \[2].

When finished with the server, stop it in the terminal with Ctrl+C and confirm.

## 5. Install and use JupyterLab (modern UI)

JupyterLab is a more integrated, IDE-like interface that combines notebooks, terminals, file browser, and extensions.

Install and launch JupyterLab:

```bash theme={null}
pip install jupyterlab
jupyter lab --ip=0.0.0.0 --no-browser
```

Open the Lab URL (replace private hostname with public IP or use SSH tunneling). JupyterLab highlights:

* Launcher for notebooks, consoles, and terminals.
* Split panes and tabbed layout for working on multiple files concurrently.
* Integrated terminal to run shell commands and pip inside the environment.
* Extension support (e.g., Git integration, code formatters, plot viewers).

Inside a JupyterLab terminal you might see installed packages:

```bash theme={null}
# Example output from `pip list` (truncated)
nbformat        5.10.4
notebook        7.3.3
numpy           2.2.4
pip             24.0
pyzmq           26.3.0
jupyterlab      4.3.6
```

You can install JupyterLab extensions to add Git, file diffing, and other developer tools.

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Demo Steps&#x22; showing eight numbered steps for setting up and using Jupyter Notebook, from checking Python and installing Jupyter to adding cells, running code, and discussing shortcuts." />
</Frame>

## 6. Quick reference — commands and tips

|                     Task | Command / Tip                                | Notes                                          |
| -----------------------: | -------------------------------------------- | ---------------------------------------------- |
|      Install system deps | sudo apt install -y python3-pip python3-venv | Ubuntu 24.04+                                  |
|              Create venv | python3 -m venv jupyter\_env                 | Activate with source jupyter\_env/bin/activate |
| Install classic notebook | pip install jupyter                          | Starts with jupyter notebook                   |
|       Install JupyterLab | pip install jupyterlab                       | Starts with jupyter lab                        |
|               Run server | jupyter notebook --ip=0.0.0.0 --no-browser   | Replace private IP with public, or tunnel      |
|            Secure access | Use SSH tunnel or VPN                        | Do not leave ports open publicly               |

## 7. Recap — what we covered

| Step | Summary                                                                                                  |
| ---- | -------------------------------------------------------------------------------------------------------- |
| 1    | Verified Python is available (use python3 on modern Ubuntu).                                             |
| 2    | Installed pip and python3-venv; created and activated a virtual environment.                             |
| 3    | Installed Jupyter (classic) and launched it for remote access.                                           |
| 4    | Created notebooks, added code and markdown cells, executed cells, and inspected outputs.                 |
| 5    | Installed and launched JupyterLab to use an IDE-like interface with terminals and extensions.            |
| 6    | Emphasized security: replace private IPs with public IPs or use SSH tunneling and avoid public exposure. |

<Frame>
  <img alt="A presentation slide titled &#x22;Summary&#x22; that lists five numbered points about Jupyter notebooks. The points cover installing a Jupyter server, creating and using notebooks locally or in hosted environments, SageMaker integration, code vs. markdown cells, and collaboration for ML projects." />
</Frame>

Jupyter Notebook and JupyterLab provide a flexible environment to mix code, results, and narrative documentation — making them core tools for data science, machine learning, and exploratory analysis. If you prefer a managed environment, consider using [AWS SageMaker](https://learn.kodekloud.com/user/courses/aws-sagemaker) or other hosted notebook services that include security, scaling, and pre-configured tools.

Further reading and references:

* [Jupyter Documentation](https://jupyter.org/documentation)
* SSH tunneling and port forwarding (search “ssh local port forwarding” for tutorials)
* [AWS SageMaker course — KodeKloud](https://learn.kodekloud.com/user/courses/aws-sagemaker)

Next up: try a hands-on lab to practice creating notebooks, running experiments, and using JupyterLab extensions.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/8dba4cbc-6eb7-4985-b97a-c5b7e6d23161/lesson/dc2f834c-f4a3-4af5-b1c1-f6c3e1802851" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/aws-sagemaker/module/8dba4cbc-6eb7-4985-b97a-c5b7e6d23161/lesson/58a58ea4-4848-403c-aa19-229ad1445e52" />
</CardGroup>


# Introduction to Jupyter Notebooks Part 2

Source: https://notes.kodekloud.com/docs/AWS-SageMaker/SageMaker-Introduction/Introduction-to-Jupyter-Notebooks-Part-2/page

Overview of running Jupyter notebooks locally, in containers, IDEs, and AWS SageMaker, covering server architecture, instance sizing, examples, visualizations, and workflow benefits

This article explains the common ways to run Jupyter notebooks, how the Jupyter server and browser interface interact, and highlights Jupyter in AWS SageMaker. It also covers instance sizing, simple notebook examples, and visualization capabilities you’ll use in data science workflows.

## Ways to run Jupyter

You can run Jupyter in several environments depending on your workflow, collaboration needs, and infrastructure:

| Method               | When to use                                           | Examples / Notes                                            |
| -------------------- | ----------------------------------------------------- | ----------------------------------------------------------- |
| Local installation   | Development, quick experimentation, or offline work   | Install with pip or use the Anaconda distribution           |
| Containerized        | Isolated, reproducible environments; consistent CI/CD | Run Jupyter inside Docker images from Docker Hub or quay.io |
| Inside an IDE        | Tight editor integration and local debugging          | VS Code supports .ipynb files natively                      |
| Hosted cloud service | Scalable, managed compute and collaboration           | AWS SageMaker, Google Colab, Databricks                     |

* Local setup
  * If Python is installed, use pip:
    ```bash theme={null}
    pip install notebook          # classic Jupyter Notebook server
    pip install jupyterlab        # modern JupyterLab interface
    ```
  * Or install the Anaconda distribution, which bundles Python, Jupyter, common data science libraries, and the conda package manager: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

* Containerized
  * Use Docker or another container runtime to pull ready-made Jupyter images. Containers isolate the notebook server and dependencies from the host OS while providing the same browser-based UI.

* Inside an IDE
  * Some IDEs (for example Visual Studio Code) open .ipynb files natively and provide notebook-like experiences directly inside the editor. IDE support varies; for many data-science tasks the full Jupyter UI is preferred.

* Hosted cloud service
  * Managed services run Jupyter servers in the cloud and give you a remote URL to access via your browser. AWS SageMaker is a common option that integrates Jupyter/JupyterLab with AWS services and storage.

<Frame>
  <img alt="A slide titled &#x22;Workflow: Ways to Run Jupyter&#x22; listing four methods: Local Setup (install via pip or Anaconda), Containerized Setup (use Docker images from quay.io), IDE Support (.ipynb support), and Cloud-Based (SageMaker on AWS) for team collaboration." />
</Frame>

When you run Jupyter locally or in a container, the Jupyter server exposes a web interface you open in a browser (for example [http://localhost:8888](http://localhost:8888)). With a hosted cloud service such as AWS SageMaker, your browser points to a cloud URL instead — the UI (classic Notebook or JupyterLab) looks the same but runs on managed infrastructure.

<Callout icon="lightbulb">
  Jupyter is always accessed via a web browser. The server (local, container, or cloud) runs the code and hosts the notebook application; your browser is the client.
</Callout>

***

## Jupyter in AWS SageMaker

AWS SageMaker has supported hosted Jupyter environments since its initial release. Over time AWS added:

* Classic Notebook Instances — managed EC2 instances preconfigured to run a Jupyter server.
* JupyterLab support — a multi-tabbed interface with extension support.
* SageMaker Studio — a full ML-focused IDE built on JupyterLab that integrates many additional tools and workflows for data scientists and MLOps engineers.

Most new projects use SageMaker Studio because it provides a richer integrated environment beyond basic JupyterLab. SageMaker still supports legacy Notebook Instances for backward compatibility, but Studio is the recommended choice for new work.

<Frame>
  <img alt="A presentation slide titled &#x22;Workflow: Jupyter in SageMaker&#x22; showing two options: &#x22;Notebook Instances&#x22; and &#x22;SageMaker Studio.&#x22; The left box notes Jupyter Notebook (basic, standalone) and JupyterLab (more flexible, multi-tab); the right box describes SageMaker Studio as a JupyterLab-integrated ML IDE." />
</Frame>

<Callout icon="warning">
  Notebook Instances in AWS SageMaker are supported but considered legacy. For new projects, prefer SageMaker Studio for a modern, integrated JupyterLab-based experience.
</Callout>

***

## Hosting resources and instance sizing

When creating a hosted Jupyter server (Notebook Instance or a Studio kernel/compute), you choose a compute profile. SageMaker uses instance families and sizes similar to EC2 naming:

|      Component | Meaning                                                                                  |
| -------------: | ---------------------------------------------------------------------------------------- |
|         Family | Workload type (M = general purpose, C = compute-optimized, P = GPU/accelerated)          |
|     Generation | Newer generations (e.g., M6) use more recent CPU/GPU hardware than older ones (M5, etc.) |
| Size (t-shirt) | CPU / memory / GPU capacity (large, xlarge, 2xlarge, etc.)                               |

Choose an instance type that matches your workloads: data preprocessing, model training, or GPU-accelerated deep learning. You can provision multiple hosted environments with different sizes for different projects.

When you run cells inside a notebook, code executes on the server. Notebook cells capture stdout and visual outputs inline and save them into the .ipynb document.

Example notebook cells:

```python theme={null}
