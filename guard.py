# Core logic for SecGuard: collecting project plan input, sending to Gemini, and outputting into a review.

import json
import os
import traceback

from dotenv import load_dotenv
from google import genai
from google.genai import types

from html_report import save_html

# CONFIG
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a proactive security advisor/consultant embedded in a project planning tool.
Your job is to review business process and operations project plans written
by non-technical project managers and identify security risks.

Your audience has little to no security background. Write clearly, avoid
jargon, and explain WHY each risk matters in plain business terms (data
exposure, regulatory fines, operational disruption, reputational damage).

Analyze the provided project plan and return a structured JSON security
review with exactly this format:

{
  "project_summary": "One sentence describing what this project does",
  "overall_risk_level": "High | Medium | Low",
  "overall_risk_rationale": "2-3 sentence plain-English explanation",

  "risks": [
    {
      "title": "Short risk title",
      "severity": "High | Medium | Low",
      "plain_english_explanation": "What could go wrong, in non-technical terms",
      "business_impact": "What this means for the business if it happens",
      "recommended_control": "Specific, actionable step the PM can take or request"
    }
  ],

  "compliance_flags": [
    {
      "framework": "e.g. HIPAA, SOC 2, GDPR, CCPA",
      "relevance": "Why this framework may apply to this project",
      "action_required": "What the team should verify or do"
    }
  ],

  "quick_wins": [
    "Simple immediate action the PM can take today, no technical expertise needed"
  ],

  "questions_to_ask_your_it_team": [
    "Plain-English question a PM can bring to their IT or security team"
  ]
}

Rules:
- Return valid JSON only. No preamble, no markdown, no explanation outside the JSON.
- If the project plan is vague, still analyze based on what IS there and flag
  where more information is needed inside the relevant fields.
- Identify 2-3 risks. More than 4 becomes noise for a non-technical reader.
- Aim to stick to 2-3 sentences for explanations and rationales to keep it digestible.
- Quick wins should require zero technical knowledge to action.
- Questions to ask IT should be things a PM could say in a meeting without
  feeling out of their depth.
- Flag compliance frameworks only when genuinely relevant, don't flag
  everything speculatively.
- Severity logic:
    High   = could cause data breach, regulatory violation, or operational shutdown
    Medium = creates meaningful exposure if unaddressed
    Low    = best practice gap, low immediate impact
"""


# CORE ANALYSIS FUNCTION
def analyze_project(project_text: str) -> dict:
    # Send to llm and parse
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = SYSTEM_PROMPT + "\n\nProject Plan:\n" + project_text

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    raw = (response.text or "").strip()

    # Strip markdown code fences if model adds them anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw)


# INPUT HELPER
def get_project_input() -> str:
    """
    Collect multi-line project plan input from the terminal.
    Type END on a new line to finish.
    """
    print("\n" + "─" * 60)
    print("SecGuard")
    print("─" * 60)
    print("\nPaste or type your project plan below.")
    print("When done, type END on a new line and press Enter.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    return "\n".join(lines).strip()


# SAVE OUTPUT
def save_json(review: dict, filename: str = "last_review.json") -> None:
    with open(filename, "w") as f:
        json.dump(review, f, indent=2)
    print(f"[Saved raw JSON to {filename}]")


# MAIN
def main():
    load_dotenv()
    if not GEMINI_API_KEY:
        print("\n  GEMINI_API_KEY not found.")
        print("   Add it to your .env file:")
        print("   GEMINI_API_KEY=your_key_here\n")
        return

    project_text = get_project_input()

    if not project_text:
        print("\n No input provided. Exiting.\n")
        return

    print("\nAnalyzing project plan...\n")

    try:
        review = analyze_project(project_text)
        save_json(review)
        save_html(review)

    except json.JSONDecodeError as e:
        print(f"\n Failed to parse Gemini response as JSON: {e}")
        print("   Try running again, usually a one-off model output issue.\n")

    except Exception as e:
        print(f"\n Error: {e}\n")
        traceback.print_exc()
        print()


if __name__ == "__main__":
    main()
