# Flask routes (skeleton)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/metar', methods=['POST'])
def metar():
    station = request.form.get('station', '').strip().upper()
    if not station:
        return render_template('result.html', error="Please provide a station code.")
    # Fetch METAR from aviationweather.gov (simple example URL)
    url = (
        "https://aviationweather.gov/adds/dataserver_current/httpparam?"
        f"dataSource=metars&requestType=retrieve&format=xml&stationString={station}&hoursBeforeNow=1"
    )
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        return render_template('result.html', error="Failed to fetch METAR data.")
    # For this example, assume we retrieved a METAR string
    # In a production app parse XML and extract the raw_text field
    raw_metar = "KHPN 051953Z 36008KT 10SM CLR 21/M01 A3012"
    decoder = METARDecoder()
    result = decoder.decode_metar(raw_metar)
    return render_template('result.html', metar=raw_metar, summary=result['summary'])
```

## Quick smoke test from the command line

A simple one-liner can sanity-check the METARDecoder without running the Flask app.

```bash theme={null}
# Activate your venv and run a quick python one-liner to sanity-check the decoder
source venv/bin/activate && python - <<'PY'
from app import METARDecoder
decoder = METARDecoder()
test_metar = 'KHPN 051953Z 36008KT 10SM CLR 21/M01 A3012'
result = decoder.decode_metar(test_metar)
print("METAR decoding test passed")
print("Summary:", result['summary'])
PY
```

## Committing and commit message guidance

Stage your files:

```bash theme={null}
git add app.py requirements.txt static/ templates/ README.md
```

A concise, descriptive commit message for the initial release:

```bash theme={null}
git commit -m "Add Flask METAR Reader web application

- Fetches METAR data and decodes to human-readable summaries
- Includes temperature conversion, wind direction mapping, visibility and cloud decoding
- Add initial templates and styles, and README with installation instructions"
```

<Callout icon="lightbulb">
  When using AI tools to generate or assist with commits, review commit authorship and the content of commit messages. You may choose whether to keep an explicit "Co-Authored-By" line for transparency.
</Callout>

Push to GitHub when ready:

```bash theme={null}
git push origin main
```

After pushing, verify the repository page on GitHub and add screenshots, badges, or additional docs (CONTRIBUTING.md, CODE\_OF\_CONDUCT.md) to encourage contributors.

<Frame>
  <img alt="A screenshot of a dark-themed desktop showing a browser open to a GitHub repository README for a &#x22;METAR Reader&#x22; web app, with the file list and project description visible. A code editor/IDE is open in the background." />
</Frame>

## Repository structure (example)

| Path             | Purpose                                   |
| ---------------- | ----------------------------------------- |
| app.py           | Main Flask application with METAR decoder |
| requirements.txt | Python dependencies                       |
| templates/       | HTML templates (index.html, result.html)  |
| static/          | Static assets (style.css, images)         |
| README.md        | Project overview, installation, usage     |

## Installation and quick start

```bash theme={null}
git clone https://github.com/yourusername/KodeKloud-METAR-Reader.git
cd KodeKloud-METAR-Reader

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=app.py
flask run
# Open http://127.0.0.1:5000
```

If you want to show a table of example airports, usage notes, or screenshots, add them to README.md. You can also provide a CONTRIBUTING.md to guide other developers.

<Frame>
  <img alt="A dark-mode screenshot of a GitHub README for a METAR reader, showing a table of airports and codes at the top and a &#x22;How It Works&#x22; section explaining the METAR decoding process." />
</Frame>

## Useful METAR token mappings (quick reference)

| Token           | Meaning                    | Example                      |
| --------------- | -------------------------- | ---------------------------- |
| RA              | Rain                       | `-RA` light rain             |
| SN              | Snow                       | `+SN` heavy snow             |
| FG              | Fog                        | `FG` fog present             |
| BR              | Mist                       | `BR` mist                    |
| TS              | Thunderstorm               | `TS` thunderstorms           |
| FEW/SCT/BKN/OVC | Cloud coverage             | `BKN100` broken at 10,000 ft |
| SM              | Statute miles (visibility) | `10SM` -> 10 miles           |
| Axxxx           | Altimeter (inHg)           | `A3012` -> 30.12 inHg        |
| M prefix        | Negative temperatures      | `M01` = -1°C                 |

## Final checklist before public release

* [ ] Update .gitignore to exclude venv, editor files, and secrets
* [ ] Add LICENSE (e.g., MIT)
* [ ] Ensure README contains install, usage, and contribution instructions
* [ ] Add basic tests or a smoke test for the decoder
* [ ] Remove any hard-coded API keys or secrets from the repo
* [ ] Verify commit messages and authorship are as you intend

With these steps the Flask METAR Reader is documented, tested at a basic level, and ready for a GitHub release so users and contributors can easily install, run, and extend the project.

## Links and references

* [Kubernetes Documentation](https://kubernetes.io/docs/) (general resource)
* [Docker Hub](https://hub.docker.com/) (container images)
* [Aviation Weather Center — METAR docs](https://www.aviationweather.gov/adds/metars) (data source and format reference)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/e36fd287-dee2-4916-a919-953391788143/lesson/020d9e6a-6b3f-4e82-84e2-e37a2a5aae6c" />
</CardGroup>


# Course Introduction

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Introduction/Course-Introduction/page

Hands-on Cloud Code course teaching project scaffolding, automated audits, testing, autonomous agents, security remediation, and CI CD workflows to accelerate secure software delivery.

Hi — I’m Jeremy Morgan. Welcome to the Cloud Code course.

Imagine coding with an AI assistant that can summarize, audit, and even help design your entire project in seconds. Since its launch, Cloud Code has helped thousands of engineers ship faster and more securely — over 80% report fewer bugs and more efficient code reviews. Throughout this course you’ll learn to harness Cloud Code for faster development, stronger security posture, and better team collaboration.

What you’ll gain:

* Rapid project scaffolding and generator scripts
* Automated audits and prioritized remediation todos
* Guided unit testing and test-driven development
* Autonomous agents for repetitive tasks and CI/CD automation
* Practical labs to replicate real-world engineering workflows

Whether your goal is to speed up development, harden security, or improve developer experience, this course will show you how to use Cloud Code to accomplish it.

## Course goals and outcomes

* Scaffold a new project and prepare it for public release
* Add reliable unit tests and run audits automatically
* Delegate tasks to Cloud agents for autonomous completion
* Manage reproducible environments for consistency and security
* Master multi-file project navigation, extended sessions, and prompt design

<Callout icon="lightbulb">
  Work through the hands-on labs to apply each concept immediately. These labs mirror real production tasks and are optimized for practical learning.
</Callout>

In this lesson we build a project from scratch: scaffold a codebase, prepare for release, add tests, run security and quality audits, and generate patch files and remediation plans.

Below are representative interactive outputs, audit samples, and example sessions you’ll see while working through the course.

## Example: Test failures and stack traces

This shows typical unit test failures you may encounter during development and CI runs:

```text theme={null}
