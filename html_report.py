# HTML report renderer for SecGuard.


def render_html(review: dict) -> str:
    """
    Convert security review JSON into styled HTML.
    """

    risk_level = review.get("overall_risk_level", "Unknown")

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SecGuard Report</title>

<style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        color: #222;
        margin: 40px;
        line-height: 1.6;
    }}

    .container {{
        max-width: 1000px;
        margin: auto;
        background: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }}

    h1 {{
        border-bottom: 2px solid #ddd;
        padding-bottom: 10px;
    }}

    h2 {{
        margin-top: 35px;
        color: #333;
    }}

    .risk {{
        border-left: 5px solid #ccc;
        padding: 15px;
        margin-bottom: 20px;
        background: #fafafa;
    }}

    .High {{
        border-color: #d9534f;
    }}

    .Medium {{
        border-color: #f0ad4e;
    }}

    .Low {{
        border-color: #5cb85c;
    }}

    ul {{
        padding-left: 20px;
    }}

    li {{
        margin-bottom: 1em;
    }}

    .meta {{
        background: #f8f8f8;
        padding: 15px;
        border-radius: 8px;
    }}
</style>
</head>

<body>

<div class="container">

<h1>SecGuard Report</h1>

<div class="meta">
    <p><strong>Project Summary:</strong> {review.get("project_summary", "")}</p>
    <p><strong>Overall Risk:</strong> {risk_level}</p>
    <p>{review.get("overall_risk_rationale", "")}</p>
</div>

<h2>Risks</h2>
"""

    for risk in review.get("risks", []):
        severity = risk.get("severity", "Low")

        html += f"""
<div class="risk {severity}">
    <h3>{risk.get("title", "")} ({severity})</h3>

    <p><strong>What Could Go Wrong:</strong><br>
    {risk.get("plain_english_explanation", "")}</p>

    <p><strong>Business Impact:</strong><br>
    {risk.get("business_impact", "")}</p>

    <p><strong>Recommended Control:</strong><br>
    {risk.get("recommended_control", "")}</p>
</div>
"""

    html += "<h2>Compliance Flags</h2><ul>"

    for flag in review.get("compliance_flags", []):
        html += f"""
<li>
    <strong>{flag.get("framework", "")}</strong><br>
    {flag.get("relevance", "")}<br>
    <strong>Action Required:</strong>
    {flag.get("action_required", "")}<br>
</li>
"""

    html += "</ul>"

    html += "<h2>Quick Wins</h2><ul>"

    for win in review.get("quick_wins", []):
        html += f"<li>{win}</li>"

    html += "</ul>"

    html += "<h2>Questions To Ask IT</h2><ul>"

    for q in review.get("questions_to_ask_your_it_team", []):
        html += f"<li>{q}</li>"

    html += """
</ul>

</div>
</body>
</html>
"""

    return html


def save_html(review: dict, filename: str = "last_review.html") -> None:
    """
    Save rendered HTML report to disk.
    """

    html = render_html(review)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[Saved HTML report to {filename}]")
