# SecGuard

## Overview

SecGuard is a lightweight AI-powered security review tool that analyzes business project plans and returns structured security risk assessments.

It uses an LLM to evaluate non-technical project descriptions and translate them into clear, actionable security insights for project managers and business stakeholders.

The goal is to surface security, compliance, and operational risks early in the planning process.

---

## What It Does

Given a project plan, SecGuard automatically generates a structured security review including:

- Project summary
- Overall risk level (High / Medium / Low)
- Detailed security risks with business impact
- Recommended mitigations
- Compliance framework considerations (e.g., GDPR, HIPAA, CCPA)
- Quick wins
- Questions to ask IT/security teams

---

## Output

SecGuard saves analysis in two files:

- `last_review.json` — the raw structured JSON output from the model
- `last_review.html` — a rendered HTML report built from the JSON output


---

## Usage

1. Create a `.env` file with your Gemini API key:

```env
GEMINI_API_KEY=your_key_here
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the tool:

```bash
python guard.py
```

4. Paste your project plan and type `END` on a new line to finish.

5. Open `last_review.html` in a browser to view the report.

---

## Project Structure

```text
security_guardian/
├── guard.py              # Core application (Gemini integration + CLI)
├── html_report.py        # Renders the JSON review into an HTML report
├── last_review.json      # Saved structured report output
├── last_review.html      # Saved rendered HTML report
├── requirements.txt      # Python dependencies
├── setup.cfg             # Linting and formatting configuration
├── setup.sh              # Environment setup script (optional)
├── .env                  # API key configuration (not committed)
```

---

## Notes

- `guard.py` uses `google-genai` and `python-dotenv`
- `setup.cfg` configures `flake8`, `isort`, and `mypy`
- `html_report.py` takes the parsed JSON review and writes a styled HTML file
