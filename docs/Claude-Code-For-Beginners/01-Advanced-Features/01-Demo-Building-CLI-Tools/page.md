# Demo Building CLI Tools

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Advanced-Features/Demo-Building-CLI-Tools/page

Shows how to build small CLI tools in Python, Go, and C++ with runnable examples including a project generator, Vue demo, CSV to JSON converter, and a password generator

In this lesson we build several small, focused CLI utilities to show how quickly useful command-line tools can be scaffolded in different languages. The examples alternate between Python, Go, and C++ to demonstrate differences in ergonomics, deployment, and performance. Each example includes a runnable implementation, usage examples, and notes on why you might pick one language over another for a particular task.

Table of contents:

* Python: Project structure generator
* Vue demo: the generated app
* Go: CSV → JSON converter
* C++: Password generator (macOS)
* Why CLI utilities are useful
* Links and references

***

## 1) Python — Project Structure Generator

Goal: create a small Python CLI script, `project_generator.py`, that generates boilerplate project folders in a `dist/` directory. This generator keeps things simple and file-system focused — no external dependencies required.

Supported project types:

* `html` — generates `index.html`, `style.css`, and `scripts.js`
* `vue` — generates a minimal Vue-style app (simple `index.html`, `style.css`, `app.js`)

Example usage:

```bash theme={null}
