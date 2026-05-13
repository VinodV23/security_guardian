# 🔐 Security Guardian

## Overview

Security Guardian is a lightweight AI-powered security review tool that analyzes business project plans and returns structured security risk assessments.

It uses Google Gemini 2.5 Flash to evaluate non-technical project descriptions and translate them into clear, actionable security insights for project managers and business stakeholders.

The goal is to surface security, compliance, and operational risks early in the planning process — in plain English.

---

## What It Does

Given a project plan, Security Guardian automatically generates a structured security review including:

- Project summary  
- Overall risk level (High / Medium / Low)  
- Threat surface identification  
- Detailed security risks with business impact  
- Recommended mitigations  
- Compliance framework considerations (e.g., GDPR, SOC 2, CCPA)  
- Quick wins for immediate action  
- Questions to ask IT/security teams  

---

## Example Output Structure

The system returns a structured JSON report with:

- `project_summary`
- `overall_risk_level`
- `overall_risk_rationale`
- `threat_surfaces`
- `risks`
- `compliance_flags`
- `quick_wins`
- `questions_to_ask_your_it_team`

This is then rendered into a readable terminal report and optionally saved as JSON.

---

## Project Structure

```text
security_guardian/
├── guard.py              # Core application (Gemini integration + CLI)
├── last_review.json      # Saved output from last analysis
├── .env                  # API key configuration (not committed)
├── requirements.txt      # Dependencies
├── setup.sh              # Environment setup script (optional)