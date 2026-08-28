# Example test failures and stack traces (console output)
effect = self.side_effect
if effect is not None:
    if _is_exception(effect):
        raise effect
E   Exception: HTTP 404

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/unittest/mock.py:1196: Exception
    TestEdgeCases.test_extreme_wind_directions

self = <test_app.TestEdgeCases object at 0x1148e3d10>

def test_extreme_wind_directions(self):
    """Test edge cases for wind direction conversion."""
    # Test boundary conditions
    assert self.decoder.get_wind_direction_text(361) == 'north'  # Should wrap around
    assert self.decoder.get_wind_direction_text(-1) == 'north-northwest'  # Negative wrapping
E   AssertionError: assert 'north' == 'north-northwest'
E     - north-northwest
E     + north

test_app.py:278: AssertionError

FAILED test_app.py::TestMETARDecoder::test_decode_weather_phenomena - AssertionError: assert 'rain, thunderstorm' == 'thunderstorm, rain'
FAILED test_app.py::TestMETARDecodingIntegration::test_decode_metar_with_weather - AssertionError: assert 'scattered clouds at 800 feet' in 'overcast at 2500 feet'
FAILED test_app.py::TestMETARDecodingIntegration::test_decode_multiple_weather_phenomena - AssertionError: assert 'heavy thunderstorm, heavy rain' in 'heavy rain, heavy thunderstorm'
FAILED test_app.py::TestFetchMETAR::test_fetch_metar_network_error - Exception: Network error
FAILED test_app.py::TestFetchMETAR::test_fetch_metar_http_error - Exception: HTTP 404
FAILED test_app.py::TestEdgeCases::test_extreme_wind_directions - AssertionError: assert 'north' == 'north-northwest'
```

## Example: Interactive terminal and guided prompts

During labs you’ll see interactive terminal sessions that guide edits, audits, and commits:

```bash theme={null}
Welcome to the KodeKloud Hands-On lab

KODEKLOUD

All rights reserved

root@controlplane ~ via v3.12.3 ➜
```

These prompts help you iterate quickly: modify files, re-run tests, and accept suggested fixes.

## What Cloud Code audits look like

Cloud Code provides structured audit outputs and writes files for reviewers and stakeholders:

```text theme={null}
● Write(audits/ERROR_HANDLING_COMPREHENSIVE_REVIEW.md)
└─ Wrote 596 lines to audits/ERROR_HANDLING_COMPREHENSIVE_REVIEW.md
# Error Handling Comprehensive Review
## Executive Summary
**Status:** ❌ **CRITICAL DEFICIENCIES IDENTIFIED**
**Overall Score:** 3.5/10
The Express Login Demo exhibits severe error handling vulnerabilities that create significant security risks and operational issues. The application lacks centralized error management, exposes sensitive information through verbose error messages, and has inconsistent handling across routes.
## Critical Findings Overview
+586 lines (ctrl+r to expand)
* Whirlpooling... (esc to interrupt)
```

Cloud Code can also generate remediation todos, patch files, or full security reports you can review and apply from within your editor.

## Example: File structure and architecture summary

Cloud Code generates concise summaries that help you understand architecture and hotspots quickly:

```text theme={null}
- config/database.js - PostgreSQL database connection pool
- routes/auth.js - Authentication routes (currently only login)
- schema.sql - Database schema definition

Route-Controller Architecture:

Routes are directly connected using Express Router patterns:
- Main server mounts auth routes at /api/auth (server.js:11)
- Auth router handles /login endpoint with inline controller logic (routes/auth.js:9-96)
- No separate controller layer - business logic is embedded in route handlers

Database:

PostgreSQL with:
- Connection via pg library with connection pooling (config/database.js:3-9)
- Single users table with id, email, name, password, timestamps (schema.sql:8-15)
- Email index for performance (schema.sql:18)
- Uses bcrypt for password hashing and JWT for authentication tokens
```

## Example: Secrets & logging scan

Cloud Code helps find risky console logging or secrets left in files:

```bash theme={null}
$ grep -r "console\.log\|console\.error" /Users/jeremy/Repos/Claude\ Code\ Course/Express-login-demo/ --include="*.js" --exclude-dir=node_modules
/Users/jeremy/Repos/Claude Code Course/Express-login-demo/config/database.js: console.log('Connected to PostgreSQL database');
/Users/jeremy/Repos/Claude Code Course/Express-login-demo/config/database.js: console.error('Database connection error:', err);
 /Users/jeremy/Repos/Claude Code Course/Express-login-demo/server.js: console.log(`Server running on port ${PORT}`)

$ grep -r "password\|secret\|token\|key" /Users/jeremy/Repos/Claude\ Code\ Course/Express-login-demo/.env
/Users/jeremy/Repos/Claude Code Course/Express-login-demo/.env:JWT_SECRET=your_jwt_secret_key_here
/Users/jeremy/Repos/Claude Code Course/Express-login-demo/.env:DB_PASSWORD=your_db_password
```

<Frame>
  <img alt="A split-screen slide titled &#x22;Claude Code&#x22; with bullet points (Getting Started, Working, Code Review, Security Auditing, Advanced Features) on the left. On the right, a bearded man wearing glasses and a KodeKloud T‑shirt speaks toward the camera." />
</Frame>

## Prioritized remediation: TODO list example

After an audit, Cloud Code creates prioritized tasks to fix vulnerabilities and technical debt:

```text theme={null}
Update Todos
- Examine codebase structure and identify database files
- Analyze database schema and configuration
- Review all database queries for SQL injection vulnerabilities
- Check connection string and credential security
- Verify parameterized queries and ORM usage
- Assess database permissions and access controls
- Review sensitive data handling and encryption
- Check transaction handling and error management
- Analyze logging and audit capabilities
- Generate comprehensive security report

Write(audits/DATABASE_SECURITY_AUDIT_REPORT.md)

Opened changes in Visual Studio Code ✎
Save file to continue...

Do you want to make this edit to DATABASE_SECURITY_AUDIT_REPORT.md?
1. Yes
2. Yes, for this session only (shift+tab)
3. No, and tell Cloud what to do differently (esc)
```

## Advanced features & automation

In advanced modules you’ll learn to:

* Use Cloud agents for autonomous tasks
* Implement test-driven development (TDD)
* Design database migrations and schema changes
* Automate CLI tools and create Kubernetes clusters
* Configure CI/CD pipelines for release automation

Example starter script Cloud Code can help create:

```python theme={null}
#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

class ProjectGenerator:
    def __init__(self):
        self.dist_dir = Path("dist")
        self.templates = {
            # ... template definitions ...
        }

    def generate(self, project_type: str, name: str):
        # Implementation that writes project files to dist/
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate starter projects.")
    parser.add_argument("type", help="Type of project to generate")
    parser.add_argument("name", help="Name of the project")
    args = parser.parse_args()

    gen = ProjectGenerator()
    gen.generate(args.type, args.name)
# (Output truncated — generator wrote many files)
```

Create the distribution directory:

```bash theme={null}
$ mkdir -p dist
```

## Course modules at a glance

| Module                          | Focus                               | Outcomes                                    |
| ------------------------------- | ----------------------------------- | ------------------------------------------- |
| Getting Started                 | Environment setup and first session | Scaffold a project and run your first audit |
| Working with Cloud Code         | Day-to-day workflows                | Run tests, fix issues, manage sessions      |
| Code Review & Security Auditing | Automated audits and fixes          | Generate audits, TODOs, and patch files     |
| Advanced Features               | Automation and scaling              | Agents, CI/CD, Kubernetes, TDD              |

## Community and continued learning

KodeKloud emphasizes community learning. Join the forums to ask questions, share solutions, and learn from peers.

<Frame>
  <img alt="A screenshot of the KodeKloud community/forum interface showing a left-hand category list and a central/right column of forum topics and latest posts. A circular picture-in-picture video of a man speaking appears in the bottom-right corner." />
</Frame>

<Callout icon="warning">
  Never commit secrets, API keys, or plaintext credentials to your repository. Use environment variables, vaults, or secrets managers and run scans regularly.
</Callout>

## Links and references

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)
* [Node.js (Express) documentation](https://expressjs.com/)
* [Python argparse documentation](https://docs.python.org/3/library/argparse.html)

So — let’s get started. Dive into the labs, apply audits, and use Cloud Code to accelerate secure, maintainable software delivery.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/0bd6d2b4-0fbf-4c4d-a348-af6c3321121c/lesson/eb50d87a-451c-42f9-b2bc-b8e8093ac4ca" />
</CardGroup>


# Demo Installing Claude on Ubuntu Virtual Machines

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Introduction/Demo-Installing-Claude-on-Ubuntu-Virtual-Machines/page

Guide to installing Claude Code on Ubuntu VMs, avoiding npm permission errors and using the native installer with tips for PATH, Node alternatives, and VM sizing

This guide explains a common issue when installing Claude Code on typical Ubuntu virtual machines (EC2, Lightsail, etc.) and provides a safe, recommended workaround using the native installer. It preserves the original troubleshooting steps and shows how to avoid permission problems that occur with global npm installs.

## 1 — Update and upgrade the system

Always start by updating package lists and upgrading installed packages:

```bash theme={null}
sudo apt update
sudo apt upgrade -y
```

If a kernel was upgraded, apt may report a pending kernel upgrade and suggest a reboot. Example output:

```text theme={null}
Pending kernel upgrade!
Running kernel version:
 6.14.0-1010-aws
Diagnostics:
 The currently running kernel version is not the expected kernel version 6.14.0-1012-aws.

Restarting the system to load the new kernel will not be handled automatically, so you should consider rebooting.
```

<Callout icon="warning">
  If the system indicates a pending kernel upgrade, plan a reboot. Some kernel upgrades require a restart before the VM behaves as expected — especially on cloud images that use kernel packages from the provider (e.g., `*-aws` kernels).
</Callout>

## 2 — Node.js / npm and a common permissions error

Many older guides instruct installing Claude Code via a global npm package:

```bash theme={null}
sudo apt install -y nodejs npm
```

Then attempting:

```bash theme={null}
npm install -g @anthropic-ai/claude-code
```

may fail with permission errors when npm tries to write to `/usr/local/lib/node_modules`. Example failure:

```text theme={null}
npm ERR! code EACCES
npm ERR! syscall mkdir
npm ERR! path /usr/local/lib/node_modules
npm ERR! errno -13
npm ERR! Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules'
...
The operation was rejected by your operating system.
It is likely you do not have the permissions to access this file as the current user

A complete log of this run can be found in:
 /home/ubuntu/.npm/_logs/<timestamp>-debug-0.log
```

<Callout icon="lightbulb">
  Anthropic explicitly recommends not using `sudo` with `npm install -g` because it can create permission and ownership issues. Prefer user-local installations (see npm 'prefix': [https://docs.npmjs.com/cli/v9/using-npm/config#prefix](https://docs.npmjs.com/cli/v9/using-npm/config#prefix)), [nvm](https://github.com/nvm-sh/nvm), or the native installer instead.
</Callout>

## 3 — Options to resolve npm permission issues

Choose one of these approaches to avoid global permission errors and maintain a safe system configuration:

| Resource / Approach            |                                                           Use Case | Links / Notes                                                                                                  |
| ------------------------------ | -----------------------------------------------------------------: | -------------------------------------------------------------------------------------------------------------- |
| nvm (Node Version Manager)     |        Install Node for your user and use per-user global packages | [https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm)                                                 |
| npm prefix (user-local global) | Reconfigure npm global install directory under your home directory | [https://docs.npmjs.com/cli/v9/using-npm/config#prefix](https://docs.npmjs.com/cli/v9/using-npm/config#prefix) |
| Native installer (recommended) |           Quick, VM-friendly install without npm permission issues | See installer steps below                                                                                      |

## 4 — Recommended: Use the native Claude Code installer (quick and simple)

On a freshly provisioned VM, install curl and git (if not already installed), then run Anthropic’s installer script:

```bash theme={null}
sudo apt install -y curl git
curl -fsSL https://claude.ai/install.sh | bash
```

The installer typically places the `claude` binary under `~/.local/bin` and may prompt that this directory is not in your PATH. Example installer output:

```text theme={null}
Setting up Claude Code...

⚠ Setup notes:
• ~/.local/bin is not in your PATH
• Add it by running: export PATH="$HOME/.local/bin:$PATH"

✓ Claude Code successfully installed!

Version: 1.0.98
Location: ~/.local/bin/claude

Next: Run claude --help to get started

✅ Installation complete!
```

If `~/.local/bin` is not in your PATH, add it permanently to your shell startup file or re-login:

```bash theme={null}
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
source ~/.profile
```

Now verify the installation:

```bash theme={null}
claude --help
```

You should see the command help and available subcommands, confirming a successful installation.

## 5 — Instance sizing and system requirements

When provisioning a VM for Claude Code, ensure the instance meets Anthropic’s recommended system requirements — in particular, at least 4 GB RAM. Choose an instance size with adequate memory and CPU.

<Frame>
  <img alt="A screenshot of a browser displaying Anthropic's &#x22;Set up Claude Code&#x22; documentation page listing system requirements and additional dependencies. The window is shown over an Amazon Lightsail interface, with a left navigation menu and a right-side table of contents visible." />
</Frame>

For example, Lightsail and many cloud providers expose a grid of plans. Pick an instance with 4 GB RAM or more:

<Frame>
  <img alt="A screenshot of the Amazon Lightsail instance selection page showing network type options and a grid of pricing cards. Each card lists monthly plans and specs (memory, vCPUs, SSD storage, transfer) with prices from 5 to 384." />
</Frame>

## 6 — Summary and best practices

* Prefer the native installer to avoid global npm permission issues on VMs.
* If you must use Node/npm, use nvm or configure npm's `prefix` so global packages install under your home directory.
* Reboot the VM after kernel upgrades if apt reports a pending kernel; this avoids inconsistent behavior.
* Pick an instance size with at least 4 GB RAM for reliable performance.

Useful links and references:

* [Node.js](https://nodejs.org/)
* [nvm — Node Version Manager](https://github.com/nvm-sh/nvm)
* [npm config 'prefix'](https://docs.npmjs.com/cli/v9/using-npm/config#prefix)
* Anthropic installer: [https://claude.ai/install.sh](https://claude.ai/install.sh)

Example small diff shown in the original notes:

```diff theme={null}
1 function greet() {
2 -  console.log("Hello, World!");
3 +  console.log("Hello, Claude!");
4 }
```

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/0bd6d2b4-0fbf-4c4d-a348-af6c3321121c/lesson/22a9bd77-22f3-448c-bb91-ff2fb9baebae" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/0bd6d2b4-0fbf-4c4d-a348-af6c3321121c/lesson/692f57ec-6c8f-4294-9383-62f4fff426cc" />
</CardGroup>
