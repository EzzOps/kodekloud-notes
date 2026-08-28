# app.py
import os
import uuid
import tempfile
import atexit
import traceback
from datetime import datetime, timedelta
from threading import Lock
from flask import Flask, request, render_template, jsonify, send_file, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image, ImageFilter, ImageOps
import cv2  # kept available for future features
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25 MB
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# Rate limiting: 30 requests per minute per IP
limiter = Limiter(app, key_func=get_remote_address, default_limits=["30 per minute"])

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
TEMP_FILES = set()
TEMP_FILES_LOCK = Lock()

def allowed_file(filename: str) -> bool:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return ext in ALLOWED_EXTENSIONS

def register_temp_file(path: str):
    with TEMP_FILES_LOCK:
        TEMP_FILES.add(path)

def cleanup_temp_file(path: str):
    try:
        with TEMP_FILES_LOCK:
            TEMP_FILES.discard(path)
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        traceback.print_exc()

@atexit.register
def cleanup_all_temp_files():
    with TEMP_FILES_LOCK:
        files = list(TEMP_FILES)
    for f in files:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception:
            traceback.print_exc()

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 25MB'}), 413

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@limiter.limit("30/minute")
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    register_temp_file(filepath)

    return jsonify({
        'success': True,
        'filename': filename,
        'url': url_for('get_temp_file', filename=filename)
    }), 200

@app.route('/temp/<filename>')
def get_temp_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath)

@app.route('/optimize/<filename>', methods=['POST'])
@limiter.limit("30/minute")
def optimize(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'Source file not found'}), 404

    try:
        # Read parameters
        quality = int(request.form.get('quality', 85))
        resize_percent = int(request.form.get('resize_percent', 100))
        strip_metadata = request.form.get('strip_metadata', 'true').lower() == 'true'
        auto_orient = request.form.get('auto_orient', 'true').lower() == 'true'
        sharpen_value = float(request.form.get('sharpen', 0.0))
        output_format = request.form.get('format', 'JPEG').upper()  # JPEG, PNG, WEBP

        # Prepare optimized filename
        optimized_filename = f"opt_{uuid.uuid4().hex}_{filename}"
        optimized_filepath = os.path.join(app.config['UPLOAD_FOLDER'], optimized_filename)

        # Ensure previous optimized file cleaned up
        if os.path.exists(optimized_filepath):
            cleanup_temp_file(optimized_filepath)

        # Open and process image with Pillow
        with Image.open(filepath) as img:
            if auto_orient:
                img = ImageOps.exif_transpose(img)

            # Resize if needed
            if resize_percent != 100:
                width = max(1, int(img.width * resize_percent / 100))
                height = max(1, int(img.height * resize_percent / 100))
                img = img.resize((width, height), Image.LANCZOS)

            # Sharpen/blur handling: use UnsharpMask for sharpening, GaussianBlur for negative values
            if sharpen_value > 0:
                # UnsharpMask expects integers for percent - compute safe int
                percent = max(0, min(500, int(round(sharpen_value * 100))))
                img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=percent, threshold=3))
            elif sharpen_value < 0:
                radius = max(0, abs(sharpen_value))
                img = img.filter(ImageFilter.GaussianBlur(radius=radius))

            # Handle metadata: include EXIF only when strip_metadata is False and EXIF exists
            save_kwargs = {}
            if not strip_metadata:
                exif_bytes = img.info.get('exif')
                if exif_bytes:
                    save_kwargs['exif'] = exif_bytes

            # Format-aware saving and mode adjustments
            fmt = output_format
            if fmt == 'JPEG':
                # JPEG cannot handle alpha - convert if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                save_kwargs['quality'] = max(1, min(95, quality))
                save_kwargs['optimize'] = True
                save_kwargs['progressive'] = True
                fmt = 'JPEG'
            elif fmt == 'WEBP':
                save_kwargs['quality'] = max(1, min(100, quality))
                fmt = 'WEBP'
            else:  # PNG or other
                fmt = 'PNG'

            img.save(optimized_filepath, format=fmt, **save_kwargs)

        register_temp_file(optimized_filepath)
        return jsonify({'success': True, 'optimized_url': url_for('get_temp_file', filename=optimized_filename)}), 200

    except Exception as e:
        print(f"Optimization error: {e}")
        traceback.print_exc()
        return jsonify({'error': f'Failed to optimize image: {str(e)}'}), 500

if __name__ == '__main__':
    # If port 5000 is in use by system services (e.g., macOS AirPlay Receiver), choose a different port
    app.run(debug=True, port=5001)
```

Notes:

* Keep the `cv2` import available but prefer Pillow operations for cross-platform portability and smaller runtime surface.
* The code prints tracebacks on exceptions to help during interactive debugging—a useful habit for long sessions.

***

## requirements.txt (example)

```text theme={null}
Flask==2.3.3
Flask-Limiter==3.5.0
Pillow==10.0.0
opencv-python-headless==4.8.1.78
gunicorn==20.1.0
```

***

## Run locally: virtual environment, install, run

Quick local setup:

```bash theme={null}
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run in development (choose an available port)
python app.py
# or explicitly
python -m flask run --port 5001
```

Common console messages and how to address them:

* zsh: command not found: python
  * Use `python3` instead of `python` on systems where `python` is not aliased.
* Flask-Limiter warning about in-memory storage:
  * Development-only; configure Redis for production.
* Address already in use (port 5000):
  * Use `lsof` to find the process and stop it, or run the app on another port.

Troubleshooting commands (macOS / Linux):

```bash theme={null}
# Find process using port 5000
lsof -i :5000

# Kill process by PID (be careful)
kill -9 <PID>

# Alternatively, run app on a different port:
python app.py  # if app.py sets port=5001 or use flask run --port 5001
```

***

## UI and example workflow

The app provides:

* Drag-and-drop upload (client-side JS)
* "Before" pane that displays the uploaded image
* "After" pane with placeholder until the image is optimized
* Controls: quality slider, resize percent, sharpen/blur slider, strip metadata toggle, format dropdown, presets

When a user uploads an image, the server stores it temporarily. The UI displays the "before" image and allows the user to adjust optimization parameters, which are applied server-side against the same temporary source so you can iterate without re-uploading.

Here’s the UI screenshot referenced in the lesson:

<Frame>
  <img alt="A screenshot of an &#x22;Image Optimizer&#x22; webpage showing a vintage black-and-white family portrait in the &#x22;Before&#x22; pane and an empty &#x22;After&#x22; pane with an &#x22;Optimize Image&#x22; button highlighted. The interface sits on a purple gradient background with a red notice bar along the bottom." />
</Frame>

***

## Debugging: common runtime errors & fixes

1. 500 Internal Server Error on /optimize:
   * Inspect server logs and printed tracebacks.
   * Common causes:
     * Passing float where an integer is required (e.g., UnsharpMask percent).
     * Trying to save a JPEG from an image with an alpha channel.
     * Attempting to re-optimize a non-existent or already-deleted source file.
   * Fixes:
     * Cast or round floats to integers where Pillow expects ints.
     * Convert image mode to RGB before saving as JPEG.
     * Ensure the original upload is preserved as the canonical source; write optimized images to new temp files.

2. Port conflicts:
   * On macOS, system services (like AirPlay Receiver) may claim port 5000. Use `lsof` to identify or change the app port.

Example console error captured in the lesson:

```text theme={null}
Failed to load resource: the server responded with a status of 500 (INTERNAL SERVER ERROR)
http://localhost:5001/optimize/b0376_eb95a_morgans.png 500 (INTERNAL SERVER ERROR)
```

Add a robust exception handler (with traceback printing and JSON error payloads) to speed up iterative debugging.

***

## Adding new features iteratively

During the lesson we iteratively added:

* Quality slider for JPEG/WebP (1–95 for JPEG)
* Resize by percentage (10–200%) while preserving aspect ratio
* Strip metadata toggle (EXIF removal)
* Sharpen and blur sliders (convert floats safely for Pillow filters)
* Contrast/brightness controls (planned/added later)
* Format conversion (JPEG, PNG, WebP)
* Live preview workflow (optimize multiple times without re-uploading)
* Auto-cleanup for temp files and thread-safe tracking of temp file paths

When adding features:

* Validate all incoming parameters (type and bounds).
* Cast floats to ints where required by Pillow filtering APIs (or compute safe integer equivalents).
* Preserve the original upload as the source for all reprocessing so iterative tuning produces reproducible results.

***

## Session documentation (SESSION\_NOTES.md)

Capture progress and decisions in a session notes file so future sessions or collaborators can rehydrate context quickly. Example (excerpt):

```markdown theme={null}
## Project Overview
Built a Flask app for image optimization:
- Drag-and-drop upload
- JPEG/PNG/WebP support (SVG/GIF rejected)
- Rate limiting 30 req/min per IP
- Max upload 25MB
- Auto-cleanup of temp files
- Before/After UI
- Uses Pillow (OpenCV available)

## SESSION 1: Core features
- Upload, validation, temp file handling
- Rate limiting with Flask-Limiter (in-memory store for dev)
- Error handlers for 413 and 429 responses

## SESSION 2: Advanced features
- Quality slider, resize by percent
- Sharpen/blur controls, contrast/brightness (added)
- Format conversion (JPEG/PNG/WebP)
- Live iterative optimization workflow: upload once, optimize multiple times
- Fix: convert float sharpen values to int percent for UnsharpMask
- UI improvements: responsive layout, presets, live preview

## Development notes
- Use python3 -m venv venv and source venv/bin/activate
- If port 5000 in use on macOS, run on a different port or disable AirPlay Receiver
- For production, configure Redis for rate limiter storage

## Next steps / Roadmap
- Add persistent rate-limiter storage (Redis)
- Add presets persistence and user accounts (requires DB)
- Add server-side caching for repeated identical optimizations
```

Keeping `SESSION_NOTES.md` concise and up to date helps you break long sessions into logical steps and prevents context loss.

***

## Best practices for long interactive sessions

<Callout icon="warning">
  Avoid attempting an entire project or a major refactor in a single continuous interactive session. Long contexts can cause confusion and increase the risk of mistakes. Instead:

  * Break work into logical steps and commit frequently.
  * Maintain a session notes file and update it after each major change.
  * When context becomes noisy, compact or restart your session and rehydrate from SESSION\_NOTES.md.
</Callout>

Practical tips:

* Summarize progress before adding large new features.
* Use session notes to provide a concise context snapshot for a fresh session.
* Start a fresh session for major refactors or when debugging unexpected behavior.
* Print tracebacks and return structured JSON error payloads to speed up iterative debugging.
* For production, replace in-memory rate-limiter storage with Redis and run the app under Gunicorn inside Docker.

***

## Quick links and references

* Flask documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* Pillow (PIL) docs: [https://pillow.readthedocs.io/](https://pillow.readthedocs.io/)
* Flask-Limiter: [https://flask-limiter.readthedocs.io/](https://flask-limiter.readthedocs.io/)
* Gunicorn: [https://gunicorn.org/](https://gunicorn.org/)
* Docker: [https://www.docker.com/](https://www.docker.com/)

***

## Summary

This lesson walked through building an image-optimization Flask app with practical choices for safe iteration:

* Core features: MAX\_CONTENT\_LENGTH, allowed types, UUID filenames, temp file cleanup.
* Rate limiting with Flask-Limiter (dev vs. production).
* Image processing with Pillow (and keeping OpenCV available).
* Debugging tips for 500 errors and port conflicts.
* Session hygiene: `SESSION_NOTES.md`, breaking work into chunks, and restarting sessions when necessary.

Next steps: implement contrast/brightness refinements, persist presets, add production hardening (Redis-backed rate limiter, Docker + Gunicorn), and maintain session notes to keep long development efforts reproducible and maintainable.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/3e896e50-3c07-4fdc-8603-bf125255d0a9/lesson/1f4ed59a-414b-47c8-acb4-1d5683a136c1" />
</CardGroup>


# Demo Multi file Project Navigation

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Working-with-Claude-Code/Demo-Multi-file-Project-Navigation/page

Guide to using Claude Code for navigating multi-file projects, summarizing structure, proposing and verifying cross-file refactors such as database migrations.

In this lesson you'll learn how to navigate multi-file projects, inspect project structure, and perform cross-file analysis and refactors with Claude Code. We'll cover how Claude Code reads the working directory, summarizes relationships between files, proposes changes (for example, a DB migration), and verifies refactors across multiple files.

<Frame>
  <img alt="A presentation slide titled &#x22;Multi-file Project Navigation&#x22; with a dark curved panel on the right that prominently shows the word &#x22;Demo.&#x22; The slide uses a light background and teal/blue accent colors." />
</Frame>

## What Claude Code provides for multi-file projects

Claude Code can:

* Inspect the current working directory and list files and folders.
* Produce a project-level summary (entry points, route structure, DB layer, where business logic lives).
* Identify which files need changing for a cross-file task (for example, migrating a database driver).
* Execute or propose targeted refactors while respecting file-level constraints.
* Verify that intended changes were applied to the correct files.

## Launching Claude Code from a project directory

Example of starting Claude Code in a local repo:

```bash theme={null}
jeremy@MACSTUDIO Express-login-demo % claude

* Welcome to Claude Code!
/help for help, /status for your current setup

cwd: /Users/jeremy/Repos/Claude Code Course/Express-login-demo

> Try "create a small logging.py that..."

? for shortcuts
```

## Show the file structure

Ask Claude Code to show the repository layout. Example output:

```bash theme={null}
> show me the file structure of this application

• List(~/Repos/Claude Code Course/Express-login-demo)
└ Listed 12 paths (ctrl+r to expand)

• Express-login-demo/
    ├── config/
    │   └ database.js
    ├── examples.md
    ├── node_modules/
    ├── package.json
    ├── package-lock.json
    ├── routes/
    │   └ auth.js
    ├── schema.sql
    └ server.js

>
? for shortcuts
```

## Project-level summary (condensed)

Claude Code can turn a file listing into an actionable summary. The following table captures the information from the example project:

| Path               | Role / Purpose           | Notes                                                |
| ------------------ | ------------------------ | ---------------------------------------------------- |
| server.js          | Main Express entry point | Mounts routers and configures middleware             |
| config/database.js | DB connection pool       | Uses pg for PostgreSQL pooling                       |
| routes/auth.js     | Authentication routes    | Contains /login endpoint and inline controller logic |
| schema.sql         | Database schema          | Users table, indexes, and timestamps                 |

High-level architecture:

* Route-controller pattern: server.js mounts auth routes at /api/auth; auth router contains inline controllers (no separate controller layer).
* Database: PostgreSQL with the pg client, connection pooling, bcrypt for password hashing, and JWT for tokens.

Claude Code can answer follow-up questions like:

* How are routes connected to controllers?
* What database driver and pooling strategy are in use?

## Example workflow: migrating PostgreSQL → MariaDB

When planning a migration (for example PostgreSQL → MariaDB), Claude Code lists affected files and the exact types of changes required.

Files likely to need direct modification:

| File               | Change Required                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| package.json       | Replace `pg` with `mysql2` or `mariadb` dependency                                               |
| config/database.js | Reimplement connection pooling using the chosen MariaDB client                                   |
| routes/auth.js     | Update parameter placeholder syntax (Postgres `$1` → `?`) and any client-specific query handling |
| schema.sql         | Convert Postgres-specific SQL to MariaDB/MySQL equivalents                                       |

Schema-level adjustments to review:

* SERIAL PRIMARY KEY → AUTO\_INCREMENT PRIMARY KEY
* Remove or replace `\c` database commands (use `USE dbname` or omit)
* Review timestamp defaults, UUID usage, and any Postgres-specific data types

Environment updates:

* .env: change default port (MariaDB usually 3306 vs Postgres 5432) and driver-specific connection variables.

Example text output Claude Code might produce when identifying required changes:

```text theme={null}
Based on the codebase analysis, these files would need changes for MariaDB migration:

Direct changes required:
- package.json: replace pg dependency with mysql2 or mariadb
- config/database.js: rewrite to use MariaDB client and connection pooling
- routes/auth.js: update parameter placeholder syntax ($1 -> ?) and any client-specific query code

Schema changes:
- schema.sql: convert PostgreSQL-specific syntax
  - SERIAL PRIMARY KEY -> AUTO_INCREMENT PRIMARY KEY
  - \c database commands -> USE statement (or remove if not needed)
  - adjust defaults and data type specifics if required (timestamps, uuid usage, etc.)

Environment variables:
- .env: update connection parameters (default port 3306 for MariaDB vs 5432 for Postgres)
```

## Existing PostgreSQL connection pool (example)

Here is the typical pattern you might find in config/database.js when using Postgres. This is the code you would replace when migrating to MariaDB:

```javascript theme={null}
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT) || 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

pool.on('connect', () => {
  console.log('Connected to PostgreSQL database');
});

module.exports = pool;
```

Note: When migrating, swap this implementation for a MariaDB client (for example, mysql2 or mariadb) and adapt pooling and query methods accordingly.

<Callout icon="lightbulb">
  Parameterized queries separate values from SQL, improving safety. Placeholder syntax differs between drivers — Postgres uses $1, $2, ...; many MySQL/MariaDB clients use `?` or named placeholders. Update your query placeholders and any client-specific methods when switching drivers.
</Callout>

## File-level instructions and safety controls

Claude Code accepts precise file-level instructions:

* Tell it exactly which files it may modify (e.g., only auth-related files).
* Or explicitly list files that must not be changed; Claude will warn if a requested modification would require touching those files.

Best practices:

* Provide contextual information about how files relate (for example: “server.js mounts the routers; auth logic lives in routes/auth.js”).
* Limit the list of files you paste — Claude Code already knows the repository layout and can focus on the relevant files.

## Verifying refactors

After a refactor, ask Claude Code to:

* Confirm which files were modified.
* Show diffs or summarize the applied changes.
* Run static checks (lint/test) or provide commands to run tests locally.

## Do's and don'ts

| Do                                              | Don't                                                           |
| ----------------------------------------------- | --------------------------------------------------------------- |
| Provide relationships between files for context | Paste huge unstructured file lists and expect manual sorting    |
| Specify which files can or cannot be modified   | Mix incompatible contexts without clear adaptation instructions |
| Ask for verification after changes              | Assume a large refactor is safe without testing or review       |

## Summary

Claude Code helps you navigate multi-file projects by:

* Mapping file structure and relationships,
* Summarizing architecture and responsibilities,
* Proposing and implementing targeted cross-file refactors (like DB migrations),
* Respecting file-level constraints, and
* Verifying the results.

This workflow accelerates working with legacy codebases, multi-file apps, and incremental migrations while reducing human error.

## Links and references

* [PostgreSQL Documentation](https://www.postgresql.org/docs/)
* [MariaDB Documentation](https://mariadb.com/kb/en/documentation/)
* [node-postgres (pg) npm package](https://www.npmjs.com/package/pg)
* [mysql2 npm package](https://www.npmjs.com/package/mysql2)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/3e896e50-3c07-4fdc-8603-bf125255d0a9/lesson/bfa6b4dc-8e40-4166-8c38-5562a79301b5" />
</CardGroup>
