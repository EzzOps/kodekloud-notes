# Create project directories and initialize backend
bash -c "mkdir -p backend frontend && cd backend && npm init -y"

# Scaffold a React frontend (TypeScript)
bash -c "cd /Users/jeremy/Repos/Claude\ Code\ Course/Simple-React-App/frontend && npx create-react-app . --template typescript"
```

If a relative path fails, Claude Code may retry with an absolute path. If `create-react-app` is deprecated in your environment, it may adapt the command and notify you.

Example backend dependency installation:

```bash theme={null}
cd /Users/jeremy/Repos/Claude\ Code\ Course/Simple-React-App/backend && \
npm install express mongoose bcryptjs jsonwebtoken nodemailer express-rate-limit helmet cors dotenv express-validator
```

Claude Code typically updates `package.json` with convenient scripts:

```json theme={null}
{
  "name": "backend",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": []
}
```

A sample `.env.example` is added so you can quickly configure environment variables:

```dotenv theme={null}
PORT=5000
MONGODB_URI=mongodb://localhost:27017/auth_app
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_EXPIRE=24h
EMAIL_FROM=noreply@yourapp.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
FRONTEND_URL=http://localhost:3000
```

Claude Code creates core backend files (e.g., `server.js`, `routes/auth.js`, `models/User.js`, `utils/email.js`) and frontend React components, contexts, and styles. It reports file sizes as it writes them so you can inspect large generated files.

Example header for `server.js`:

```javascript theme={null}
// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const authRoutes = require('./routes/auth');

const app = express();
app.use(helmet());
app.use(express.json());
app.use(cors());

// Add rate limiting, connect to MongoDB, mount auth routes, etc.
```

When generating models and routes, Claude Code often implements fully functional endpoints for register, login, verify email, and reset password, along with middleware and an email utility for delivery.

***

## Running the applications

Claude Code supplies a "get started" summary and recommended commands:

1. Start MongoDB (locally or via MongoDB Atlas)
2. Configure SMTP credentials in `.env`
3. Start backend: cd backend && npm run dev
4. Start frontend: cd frontend && npm start
5. Open [http://localhost:3000](http://localhost:3000)

Example backend startup with `nodemon`:

```bash theme={null}
cd backend && npm run dev

> backend@1.0.0 dev
> nodemon server.js

[nodemon] 3.1.10
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] starting `node server.js`
[dotenv@17.2.1] injecting env (10) from .env — tip: write to custom object with { processEnv: myObject }
Server running on port 5000
MongoDB connected
```

You may see runtime warnings when connecting to MongoDB or working with Mongoose. Example warnings:

```text theme={null}
(node:51439) [MONGOOSE] Warning: Duplicate schema index on {"email":1} found. ...
(node:51439) [MONGODB DRIVER] Warning: useNewUrlParser is a deprecated option ...
(node:51439) [MONGODB DRIVER] Warning: useUnifiedTopology is a deprecated option ...
```

Front-end startup can produce ESLint or TypeScript warnings for unused variables in generated code:

```text theme={null}
WARNING in [eslint]
src/components/auth/Register.tsx
  Line 16:9: 'navigate' is assigned a value but never used  @typescript-eslint/no-unused-vars

src/contexts/AuthContext.tsx
  Line 2:25: 'AuthResponse' is defined but never used  @typescript-eslint/no-unused-vars

src/services/api.ts
  Line 163:1: Assign instance to a variable before exporting as module default  import/no-anonymous-default-export
```

If SMTP credentials are not configured, actions that require sending email (verification or password reset) will fail and the UI may show a "Network error" until SMTP is configured.

<Frame>
  <img alt="A browser window showing a &#x22;Create Account&#x22; registration form with fields for full name, email, password and a pink &#x22;Network error&#x22; alert. The form sits on a purple gradient background over a code editor/IDE visible behind it." />
</Frame>

***

## What was generated (summary)

Below is a concise summary table of the typical artifacts Claude Code generates for an authentication system.

| Component                     | Purpose                | Typical Files / Features                                                                |
| ----------------------------- | ---------------------- | --------------------------------------------------------------------------------------- |
| Backend (Express + MongoDB)   | API and auth logic     | `server.js`, `routes/auth.js`, `models/User.js`, middleware, `utils/email.js`           |
| Authentication                | User flows & security  | Registration, login, email verification, password reset, JWT issuance                   |
| Security                      | Hardening & validation | `helmet`, rate limiting, input validation, password hashing (`bcryptjs`)                |
| Frontend (React + TypeScript) | UI & client-side auth  | `Login`, `Register`, `ForgotPassword`, `ResetPassword`, `AuthContext`, protected routes |
| Dev tooling                   | Run & test locally     | `nodemon` dev script, `.env.example`, build/start scripts                               |

Key details included in generated code

* Secure password hashing and comparison (bcrypt)
* JWT token generation and expiry handling
* Email-based verification and reset token flows (via nodemailer)
* Auth middleware for protected routes
* Basic responsive UI and loading/error states in React

***

## Auditing and production considerations

Claude Code can scaffold a working prototype quickly, but generated code contains assumptions that require manual review. Before deploying:

> **warning** Generated code may include defaults and assumptions. Always audit authentication flows, secrets handling, input validation, token storage, and email configuration. Verify secure storage for JWTs, use HTTPS in production, and rotate any example secrets.

Important production checklist

* Review JWT secret management and consider using a secrets manager
* Enforce HTTPS and secure cookie flags if using cookies
* Harden rate limiting and account lockout policies
* Validate and sanitize all inputs; add strong password policies
* Configure robust SMTP or transactional email provider (e.g., SendGrid, SES)
* Add monitoring, logging, and alerting for auth failures and suspicious activity
* Run security tests, static analysis, and dependency vulnerability scans

***

## Key lessons from autonomous building

* Independent problem solving: Claude Code selects architectures and implements features — prompt precision controls assumptions.
* Multi-component orchestration: It can scaffold backend & frontend, install dependencies, and wire systems together.
* Time savings: Boilerplate that normally takes days can be scaffolded in minutes; use the output as a starting point.
* Control assumptions: Explicitly state technologies, constraints, and security requirements to get predictable results.

***

## Links and further reading

* Claude Code security & docs: [https://docs.anthropic.com/s/claude-code-security](https://docs.anthropic.com/s/claude-code-security)
* Express.js: [https://expressjs.com/](https://expressjs.com/)
* MongoDB: [https://www.mongodb.com/](https://www.mongodb.com/)
* Mongoose: [https://mongoosejs.com/](https://mongoosejs.com/)
* JSON Web Tokens (JWT): [https://jwt.io/](https://jwt.io/)
* React: [https://reactjs.org/](https://reactjs.org/)
* Nodemailer: [https://nodemailer.com/](https://nodemailer.com/)

This lesson showed how to instruct Claude Code to build a full authentication system from a single prompt, inspect the generated files, run the apps locally, and identify where manual review and hardening are required. Future lessons will cover prompt techniques to refine results and iterate on generated code.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/e36fd287-dee2-4916-a919-953391788143/lesson/4f5a333e-06cc-47b1-aa5e-f6e8c75300bc)


# Demo Building a project from scratch

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Getting-Started-with-Claude-Code/Demo-Building-a-project-from-scratch/page

Flask tutorial building a METAR reader that fetches METARs and decodes them into plain-English aviation weather summaries using NOAA/aviationweather.gov data.

This lesson walks through creating a lightweight Flask web application that fetches and decodes METAR weather reports into plain English. The result: a small web form where a user types an ICAO airport code (e.g., KJFK, KLAX) and receives a human-friendly weather summary plus the raw METAR.

Keywords: Flask METAR reader, METAR decoder, aviationweather.gov, ICAO, NOAA ADDS.

## What is a METAR?

METAR is the international (ICAO) standard format for aviation weather observations. The encoded lines can look cryptic to non-pilots but contain a compact, consistent representation of winds, visibility, clouds, temperature, pressure, and weather phenomena. Our app uses a public METAR API and decodes each field into readable phrases.

<Frame>
  <img
    alt="A screenshot of a web browser open to the Wikipedia article for &#x22;METAR,&#x22;
showing the article text and contents list on the left with a small photo and
appearance settings on the right. The browser window includes tabs and a dark
desktop
background."
  />
</Frame>

Example raw METAR (compact / cryptic):

```text theme={null}
KJFK 052151Z 16008KT 10SM SCT047 SCT210 BKN250 24/21 A3031 RMK AO2 SLP262 T02440206
```

A decoded app should present that as human-readable lines like:

* Winds 160° at 8 knots
* Visibility 10 statute miles
* Scattered clouds at 4,700 ft and 21,000 ft; broken at 25,000 ft
* Temperature 24°C / Dew point 21°C
* Altimeter 30.31 inHg

## METAR components quick reference

|         Component | What it means                                       | Example from KJFK    |
| ----------------: | --------------------------------------------------- | -------------------- |
|        Station ID | ICAO airport code                                   | KJFK                 |
|              Time | Timestamp of observation (DDHHMMZ)                  | 052151Z              |
|              Wind | Direction and speed                                 | 16008KT              |
|        Visibility | Prevailing visibility, usually in statute miles     | 10SM                 |
|      Cloud groups | CLR, FEW, SCT, BKN, OVC + height (hundreds of feet) | SCT047 SCT210 BKN250 |
|    Temp/Dew point | Temperature and dew point in °C                     | 24/21                |
|         Altimeter | Pressure (inHg)                                     | A3031                |
| Remarks/Phenomena | RMK, weather codes like RA, FG, TS                  | RA = rain, FG = fog  |

## Project plan and goals

* Build a Flask web app with:
  * An input form for ICAO codes (index page)
  * A results template showing parsed summary + raw METAR
  * Basic, responsive styling (static/style.css)
* Use a public METAR data source (NOAA/ADDS or aviationweather.gov)
* Implement a METAR decoder that:
  * Extracts winds, visibility, cloud layers, temperatures, altimeter, observation time, and weather phenomena
  * Converts wind degrees to compass headings and reports calm conditions
  * Converts units where helpful (°C ↔ °F, inHg)
* Include basic error handling: invalid ICAO, no data, network errors
* Provide a reproducible local workflow using a virtual environment

## Example CLI: starting Claude Code For Beginners

A typical interactive session starting Claude Code (example):

```bash theme={null}
jeremy@MACSTUDIO KodeKloud-METAR-Reader % claude

Do you trust the files in this folder?
/Users/jeremy/Repos/KodeKloud-METAR-Reader

Claude Code may read files in this folder. Reading untrusted files may lead Claude Code to behave in unexpected ways.

With your permission Claude Code may execute files in this folder. Executing untrusted code is unsafe.

https://docs.anthropic.com/s/claude-code-security

> 1. Yes, proceed
  2. No, exit

Enter to confirm · Esc to exit
```

Example condensed prompt sent to Claude Code For Beginners:

```text theme={null}
Create a FLASK web application. This application will be a "METAR Reader". The user can type in an airport code, and then the application will fetch the METAR reading from that airport, and decode it. METAR is a standardized weather report. It is somewhat cryptic so I would like to convert it into plain English that people can understand. For instance, "Clear day, 70 degrees, wind 5mph to the south". This app will be successful if people can type in an airport code, and receive a friendly readable weather report. Use an aviation weather API (for example NOAA/ADDS METAR service, e.g. https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&stationString=KHIO&format=xml) as a reference.
```

## What Claude generated and common tasks

Claude helped scaffold the project and suggested a todo list and file structure. Typical outputs and tasks include:

* Files generated
  * app.py — Flask application and route handlers
  * metar\_decoder.py — parsing and conversion helpers (wind, clouds, visibility, etc.)
  * templates/index.html — search form
  * templates/result.html — decoded results and raw METAR
  * static/style.css — basic styling
  * requirements.txt — Python dependencies

Example requirements.txt produced:

```text theme={null}
Flask==2.3.3
requests==2.31.0
```

Common coding tasks to implement:

* Fetch METAR data from aviationweather.gov or NOAA ADDS endpoints
* Implement a robust METAR decoder to parse:
  * Wind: "16008KT" → 160° at 8 knots; detect "00000KT" (calm)
  * Visibility: e.g., "10SM" → 10 statute miles or "1/2SM"
  * Clouds: convert "SCT047" to "scattered at 4,700 ft"; handle CLR/SKC
  * Temperature/dew: parse "24/21" and produce °C and approximate °F
  * Altimeter: "A3031" → 30.31 inHg
  * Phenomena codes: RA (rain), SN (snow), FG (fog), BR (mist), TS (thunderstorm), SH (showers)
* Create Jinja templates to display both the friendly summary and the raw METAR string
* Add unit tests for the decoder functions

## Project scaffolding (example commands)

* Create project layout:
  * `mkdir -p metar_reader/{templates,static}`
  * `touch app.py metar_decoder.py requirements.txt`
* Virtual environment and install:

```bash theme={null}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the app locally

After installing dependencies in a virtual environment:

```bash theme={null}
source venv/bin/activate
python app.py
```

Flask development server defaults to:

* [http://127.0.0.1:5000](http://127.0.0.1:5000)

Note: Ensure the venv is activated in the same shell where you run python so the installed packages are available.

> **lightbulb** Run: python3 -m venv venv && source venv/bin/activate && pip install -r
  requirements.txt. Then start the app with python app.py and open
  [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Testing in the browser — KHIO example

Try KHIO (Hillsboro, OR) in the web form. The app fetches the METAR and displays a readable weather card.

Example decoded output shown by the app:

* Clear skies, 27°C (≈81°F)
* Wind: 000° at 0 knots (calm)
* Visibility: 10+ statute miles
* Altimeter: 30.05 inHg
* Observation time: timestamp from the METAR

Raw METAR:

```text theme={null}
KHIO 052253Z 00000KT 10SM CLR 27/11 A3005 RMK AO2 SLP172 T02670106
```

<Frame>
  <img
    alt="A browser window showing a &#x22;Weather Report for KHIO&#x22; with current conditions
(clear skies, 81°F / 27°C, wind from the north at 0 knots) and a detailed
table of observation data. The report is centered on a purple gradient
background."
  />
</Frame>

## Testing in the browser — KLAX example

Enter KLAX (Los Angeles) to verify cloud layers, winds, and other fields are parsed and presented cleanly.

Raw METAR:

```text theme={null}
KLAX 052253Z 26011KT 10SM FEW250 24/17 A2996 RMK AO2 SLP145 T02390172
```

Decoded example:

* Few clouds at \~25,000 ft
* Temperature 24°C (≈75°F), dew point 17°C
* Wind 260° at 11 knots
* Visibility 10 statute miles

<Frame>
  <img
    alt="A browser screenshot of a &#x22;Weather Report for KLAX&#x22; webpage showing current
conditions (few clouds at 25,000 ft, 75°F / 24°C, wind from the west at 11
knots) and a detailed information table below. The page is displayed on a
purple gradient background with a white card in the
center."
  />
</Frame>

## Next steps and extensions

This project is a useful base for further improvements:

* Add unit tests for the METAR decoder (pytest)
* Improve UI/UX and accessibility (ARIA, keyboard nav)
* Harden error handling (API rate limits, retries, invalid ICAO codes)
* Cache or store historical METARs for trend displays
* Extend to other aviation products (TAFs, SIGMETs) or integrate with mapping libraries

## Links and references

* [NOAA / ADDS METAR data service example](https://aviationweather.gov/adds/dataserver_current/httpparam)
* [METAR — Wikipedia](https://en.wikipedia.org/wiki/METAR)
* [Flask documentation](https://flask.palletsprojects.com/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

Thanks for following this lesson — use this METAR reader as a foundation to explore more automated coding workflows and to build reliable, testable utilities around real-world aviation data.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/e36fd287-dee2-4916-a919-953391788143/lesson/aa659d6b-8e5e-422c-9197-cb670928e287)
