"""
report.py — Report generation utilities.
Currently a placeholder; the report is rendered directly in app.py via Streamlit.
This module is reserved for future PDF export functionality.
"""

def generate_report_html(sections, overall_pct, entity_type, entity_size, obligation_length):
    """
    Returns an HTML string of the full report.
    Can be used for print/PDF export via browser or future wkhtmltopdf integration.
    """
    from questions import SECTORS
    import datetime

    rag_color = {"green": "#388e3c", "amber": "#f9a825", "red": "#c62828"}
    rag_label = {"green": "Substantially Compliant", "amber": "Material Gaps", "red": "Significant Risk"}

    def rag(pct):
        if pct >= 80: return "green"
        if pct >= 50: return "amber"
        return "red"

    overall_rag = rag(overall_pct)
    color = rag_color[overall_rag]
    today = datetime.date.today().strftime("%B %d, %Y")

    section_labels = {
        "p1": "Pillar 1 — Compliance Officer",
        "p2": "Pillar 2 — Policies & Procedures",
        "p3": "Pillar 3 — Risk Assessment",
        "p4": "Pillar 4 — Training Program",
        "p5": "Pillar 5 — Effectiveness Review",
        "kyc": "Know Your Client (KYC)",
        "rep": "Transaction Reporting",
        "rec": "Record Keeping",
        "dir": "Ministerial Directives",
    }
    sector_key = SECTORS.get(entity_type, {}).get("key")
    if sector_key:
        section_labels[f"sec_{sector_key}"] = "Sector-Specific Obligations"

    rows = ""
    for sec_key, data in sections.items():
        label = section_labels.get(sec_key, sec_key)
        r = data["rag"]
        c = rag_color[r]
        rows += f"""
        <tr>
            <td style="padding:8px 12px;">{label}</td>
            <td style="padding:8px 12px; text-align:center; font-weight:700; color:{c};">{data['pct']}%</td>
            <td style="padding:8px 12px; color:{c};">{rag_label[r]}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>FINTRAC Readiness Report — {today}</title>
<style>
  body {{ font-family: Arial, sans-serif; color: #222; max-width: 860px; margin: 40px auto; padding: 0 20px; }}
  h1 {{ color: #1a1a2e; border-bottom: 3px solid #d32f2f; padding-bottom: 8px; }}
  h2 {{ color: #1a1a2e; margin-top: 32px; }}
  table {{ width:100%; border-collapse:collapse; margin-top:12px; }}
  th {{ background:#f5f5f5; padding:8px 12px; text-align:left; border-bottom:2px solid #ddd; }}
  td {{ border-bottom:1px solid #eee; }}
  .score-box {{ display:inline-block; padding:20px 40px; border:3px solid {color};
                border-radius:8px; text-align:center; margin:16px 0; }}
  .score-num {{ font-size:3rem; font-weight:700; color:{color}; }}
  .disclaimer {{ font-size:0.8rem; color:#666; border:1px solid #ddd;
                 padding:12px; border-radius:4px; margin-top:32px; }}
</style>
</head>
<body>
<h1>🍁 FINTRAC Readiness Assessment Report</h1>
<p><strong>Date:</strong> {today} &nbsp;&nbsp;
   <strong>Entity type:</strong> {entity_type} &nbsp;&nbsp;
   <strong>Size:</strong> {entity_size} &nbsp;&nbsp;
   <strong>Time obligated:</strong> {obligation_length}</p>

<h2>Overall Readiness Score</h2>
<div class="score-box">
  <div class="score-num">{overall_pct}%</div>
  <div style="font-weight:600;">{rag_label[overall_rag]}</div>
</div>

<h2>Compliance Pillar Breakdown</h2>
<table>
  <tr><th>Section</th><th>Score</th><th>Status</th></tr>
  {rows}
</table>

<div class="disclaimer">
<strong>Disclaimer:</strong> This tool provides a preliminary self-assessment only and does not constitute
legal or compliance advice. Consult a qualified AML/ATF compliance professional or legal counsel for a
formal compliance review. All guidance references are sourced from fintrac-canafe.canada.ca.
</div>
</body>
</html>"""
