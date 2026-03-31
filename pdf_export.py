"""
pdf_export.py — Generates a downloadable PDF report using fpdf2.

Install: pip install fpdf2
"""

from fpdf import FPDF
import datetime


# ── Colour palette ──────────────────────────────────────────────────────────────
RED_DARK   = (194, 40,  40)
RED_LIGHT  = (255, 235, 238)
AMBER_DARK = (249, 168, 37)
AMBER_LIGHT= (255, 248, 225)
GREEN_DARK = (56,  142, 60)
GREEN_LIGHT= (232, 245, 233)
GREY_LIGHT = (245, 245, 245)
GREY_MID   = (200, 200, 200)
BLACK      = (30,  30,  30)
WHITE      = (255, 255, 255)

SECTION_LABELS = {
    "p1":  "Pillar 1 — Compliance Officer",
    "p2":  "Pillar 2 — Policies & Procedures",
    "p3":  "Pillar 3 — Risk Assessment",
    "p4":  "Pillar 4 — Training Program",
    "p5":  "Pillar 5 — Effectiveness Review",
    "kyc": "Know Your Client (KYC)",
    "rep": "Transaction Reporting",
    "rec": "Record Keeping",
    "dir": "Ministerial Directives",
}


def _rag(pct):
    if pct >= 80: return "green"
    if pct >= 50: return "amber"
    return "red"

def _rag_colours(r):
    return {
        "green": (GREEN_DARK, GREEN_LIGHT),
        "amber": (AMBER_DARK, AMBER_LIGHT),
        "red":   (RED_DARK,   RED_LIGHT),
    }[r]

def _rag_label(r):
    return {
        "green": "Substantially Compliant",
        "amber": "Material Gaps",
        "red":   "Significant Risk",
    }[r]


class FINTRACReport(FPDF):
    def __init__(self, entity_type, entity_size, obligation_length):
        super().__init__()
        self.entity_type       = entity_type
        self.entity_size       = entity_size
        self.obligation_length = obligation_length
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

    # ── Header on every page ────────────────────────────────────────────────────
    def header(self):
        self.set_fill_color(*RED_DARK)
        self.rect(0, 0, 210, 10, "F")
        self.set_y(14)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*WHITE)
        self.set_fill_color(*RED_DARK)
        self.cell(0, 0, "  FINTRAC READINESS ASSESSMENT", ln=False, align="L")
        self.set_text_color(*BLACK)

    # ── Footer on every page ────────────────────────────────────────────────────
    def footer(self):
        self.set_y(-14)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5,
                  f"© Asset Tech an Alberta incorporated entity. Preliminary self-assessment only — not legal advice.  |  Page {self.page_no()}",
                  align="C")
        self.set_text_color(*BLACK)

    # ── Coloured section heading ────────────────────────────────────────────────
    def section_heading(self, text):
        self.ln(4)
        self.set_fill_color(*GREY_LIGHT)
        self.set_draw_color(*RED_DARK)
        self.set_line_width(0.8)
        # Left accent bar
        self.set_fill_color(*RED_DARK)
        self.rect(self.get_x(), self.get_y(), 2, 8, "F")
        self.set_x(self.get_x() + 4)
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(*GREY_LIGHT)
        self.cell(0, 8, text, ln=True, fill=True)
        self.ln(2)
        self.set_line_width(0.2)

    # ── RAG badge cell ──────────────────────────────────────────────────────────
    def rag_row(self, label, pct, rag_key, w_label=120, w_pct=20, w_status=42):
        fg, bg = _rag_colours(rag_key)
        status = _rag_label(rag_key)
        self.set_font("Helvetica", "", 9)
        self.set_fill_color(*GREY_LIGHT)
        self.set_text_color(*BLACK)
        self.cell(w_label, 8, f"  {label}", border="B", fill=True)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*fg)
        self.cell(w_pct, 8, f"{pct}%", border="B", align="C", fill=True)
        self.set_fill_color(*bg)
        self.set_text_color(*fg)
        self.cell(w_status, 8, status, border="B", fill=True, align="C")
        self.ln()
        self.set_text_color(*BLACK)
        self.set_fill_color(*WHITE)

    # ── Gap bullet ─────────────────────────────────────────────────────────────
    def gap_bullet(self, section_label, question_text, score):
        fg = RED_DARK if score == 0 else AMBER_DARK
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*fg)
        bullet = "●  "
        self.cell(6, 6, bullet)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(80, 80, 80)
        self.cell(30, 6, f"[{section_label}]")
        self.set_text_color(*BLACK)
        # Truncate long questions
        q = question_text if len(question_text) <= 95 else question_text[:92] + "..."
        self.multi_cell(0, 6, q)
        self.set_text_color(*BLACK)

    # ── Action item ─────────────────────────────────────────────────────────────
    def action_item(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BLACK)
        self.cell(5, 6, "–")
        self.multi_cell(0, 6, text)


def generate_pdf(sections, overall_pct, entity_type, entity_size, obligation_length):
    """
    Build and return the PDF as bytes.

    Args:
        sections: dict of section_key -> {score, max, pct, rag, gaps}
        overall_pct: int 0-100
        entity_type, entity_size, obligation_length: strings from classifier

    Returns:
        bytes — the PDF file content, ready for st.download_button
    """
    pdf = FINTRACReport(entity_type, entity_size, obligation_length)
    pdf.add_page()
    today = datetime.date.today().strftime("%B %d, %Y")
    overall_rag = _rag(overall_pct)
    fg_main, bg_main = _rag_colours(overall_rag)

    # ── Title block ─────────────────────────────────────────────────────────────
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*RED_DARK)
    pdf.cell(0, 10, "FINTRAC Readiness Report", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Generated: {today}   |   Entity: {entity_type}   |   Size: {entity_size}   |   Obligated: {obligation_length}", ln=True)
    pdf.set_text_color(*BLACK)
    pdf.ln(4)

    # ── Overall score box ────────────────────────────────────────────────────────
    pdf.set_fill_color(*bg_main)
    pdf.set_draw_color(*fg_main)
    pdf.set_line_width(0.8)
    box_x, box_y = 20, pdf.get_y()
    pdf.rect(box_x, box_y, 170, 28, "FD")
    pdf.set_xy(box_x, box_y + 3)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*fg_main)
    pdf.cell(50, 12, f"{overall_pct}%", align="C")
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(box_x + 52, box_y + 3)
    pdf.cell(0, 7, _rag_label(overall_rag), ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.set_xy(box_x + 52, box_y + 12)
    pdf.cell(0, 6, "Overall Readiness Score", ln=True)
    pdf.set_text_color(*BLACK)
    pdf.ln(10)

    # ── Pillar breakdown ─────────────────────────────────────────────────────────
    pdf.section_heading("Compliance Pillar Breakdown")
    # Table header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(120, 7, "  Section", border="B", fill=True)
    pdf.cell(20,  7, "Score",    border="B", fill=True, align="C")
    pdf.cell(42,  7, "Status",   border="B", fill=True, align="C")
    pdf.ln()

    for sec_key, data in sections.items():
        label = SECTION_LABELS.get(sec_key, data.get("label", sec_key))
        pdf.rag_row(label, data["pct"], data["rag"])

    pdf.ln(6)

    # ── Priority gaps ────────────────────────────────────────────────────────────
    all_gaps = []
    for sec_key, data in sections.items():
        label = SECTION_LABELS.get(sec_key, data.get("label", sec_key))
        for gap in data["gaps"]:
            all_gaps.append({**gap, "section_label": label})
    all_gaps.sort(key=lambda x: x["score"])

    if all_gaps:
        pdf.section_heading("Priority Gaps")
        red_gaps   = [g for g in all_gaps if g["score"] == 0][:8]
        amber_gaps = [g for g in all_gaps if g["score"] == 1][:6]

        if red_gaps:
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*RED_DARK)
            pdf.cell(0, 7, "Critical — Address Immediately", ln=True)
            pdf.set_text_color(*BLACK)
            for g in red_gaps:
                pdf.gap_bullet(g["section_label"], g["q"], 0)

        if amber_gaps:
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(*AMBER_DARK)
            pdf.cell(0, 7, "Moderate — Address Within 60 Days", ln=True)
            pdf.set_text_color(*BLACK)
            for g in amber_gaps:
                pdf.gap_bullet(g["section_label"], g["q"], 1)

    pdf.ln(4)

    # ── Action plan ──────────────────────────────────────────────────────────────
    pdf.section_heading("Recommended Action Plan")
    newly_obligated = obligation_length in ["Less than 6 months", "6–18 months"]
    col_w = 55
    col_titles = ["30 Days", "60 Days", "90 Days"]
    col_colors = [RED_LIGHT, AMBER_LIGHT, GREEN_LIGHT]
    col_fg     = [RED_DARK,  AMBER_DARK,  GREEN_DARK]

    # Column headers
    start_x = pdf.get_x()
    for i, (title, bg, fg) in enumerate(zip(col_titles, col_colors, col_fg)):
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*fg)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col_w, 8, f"  {title}", border=1, fill=True)
    pdf.ln()
    pdf.set_text_color(*BLACK)

    # Build action lists
    actions_30 = []
    actions_60 = []
    actions_90 = []

    if sections.get("p1", {}).get("pct", 100) < 80:
        actions_30.append("Appoint a Compliance Officer with documented authority")
    if sections.get("p3", {}).get("pct", 100) < 80:
        actions_30.append("Begin documented ML/TF risk assessment")
    if newly_obligated:
        actions_30.append("Confirm entity classification with legal counsel")
    actions_30.append("Confirm FINTRAC registration status")

    if sections.get("p2", {}).get("pct", 100) < 80:
        actions_60.append("Draft sector-specific policies and procedures")
    if sections.get("kyc", {}).get("pct", 100) < 80:
        actions_60.append("Implement KYC identification procedures")
    if sections.get("p4", {}).get("pct", 100) < 80:
        actions_60.append("Deliver staff AML training with records")
    actions_60.append("Review Ministerial Directive obligations")

    if sections.get("p5", {}).get("pct", 100) < 80:
        actions_90.append("Schedule independent effectiveness review")
    if sections.get("rep", {}).get("pct", 100) < 80:
        actions_90.append("Test STR identification and filing process")
    if sections.get("rec", {}).get("pct", 100) < 80:
        actions_90.append("Implement 5-year records retention policy")
    actions_90.append("Run a tabletop compliance scenario with staff")

    # Render action columns — store row content, render line by line
    max_rows = max(len(actions_30), len(actions_60), len(actions_90))
    row_h = 10
    all_actions = [actions_30, actions_60, actions_90]

    for row in range(max_rows):
        row_y = pdf.get_y()
        max_h = row_h
        for col, (actions, bg) in enumerate(zip(all_actions, col_colors)):
            pdf.set_xy(start_x + col * col_w, row_y)
            pdf.set_fill_color(*bg)
            text = f"  • {actions[row]}" if row < len(actions) else ""
            pdf.set_font("Helvetica", "", 7.5)
            pdf.multi_cell(col_w, row_h, text, border="LR", fill=True)
            cell_h = pdf.get_y() - row_y
            if cell_h > max_h:
                max_h = cell_h
        pdf.set_y(row_y + max_h)

    # Bottom border
    for col, bg in enumerate(col_colors):
        pdf.set_fill_color(*bg)
        pdf.cell(col_w, 2, "", border="B", fill=True)
    pdf.ln(8)

    # ── FINTRAC Resources ────────────────────────────────────────────────────────
    pdf.section_heading("Key FINTRAC Resources")
    resources = [
        ("Compliance Program Requirements",   "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng"),
        ("Risk Assessment Guidance",           "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng"),
        ("Methods to Verify Identity",         "https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/Guide11/11-eng"),
        ("Reporting Suspicious Transactions",  "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/str-dod/str-dod-eng"),
        ("Beneficial Ownership Requirements",  "https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/bor-eng"),
        ("Ministerial Directives",             "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/min/min-eng"),
    ]
    for label, url in resources:
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(70, 6, f"  {label}")
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.set_text_color(0, 80, 160)
        pdf.cell(0, 6, url, ln=True)
        pdf.set_text_color(*BLACK)

    pdf.ln(4)

    # ── Disclaimer ───────────────────────────────────────────────────────────────
    pdf.set_fill_color(*GREY_LIGHT)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 5,
        "DISCLAIMER: This assessment tool provides a high-level preliminary self-assessment only. "
        "It does not constitute legal advice, compliance certification, or a formal FINTRAC gap assessment. "
        "Results reflect the answers provided and may not capture all obligations applicable to your specific "
        "circumstances. Consult a qualified AML/ATF compliance professional or legal counsel. "
        "All guidance references: fintrac-canafe.canada.ca",
        fill=True
    )

    return bytes(pdf.output())
