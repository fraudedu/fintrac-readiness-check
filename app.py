"""
FINTRAC Readiness Assessment Tool
A self-serve gap assessment tool for newly and existing obligated entities under the PCMLTFA.

Run with: streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1
from questions import SECTORS, PILLAR_QUESTIONS, SECTOR_QUESTIONS, SCORE_MAP, get_score
from report import generate_report_html
from demo import load_demo
from pdf_export import generate_pdf
from offers import render_offer_card
import datetime

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FINTRAC Readiness Assessment",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { max-width: 860px; margin: 0 auto; }
    .stProgress > div > div { background-color: #d32f2f; }
    h1 { color: #1a1a2e; font-size: 2rem; }
    h2 { color: #1a1a2e; font-size: 1.3rem; border-bottom: 2px solid #d32f2f; padding-bottom: 6px; }
    h3 { color: #333; font-size: 1.05rem; }
    .pillar-header {
        background: #f5f5f5;
        border-left: 4px solid #d32f2f;
        padding: 12px 16px;
        border-radius: 4px;
        margin: 18px 0 10px 0;
    }
    /* Force dark text on RAG backgrounds — overrides dark mode inheritance */
    .rag-green  { background:#e8f5e9 !important; border-left:4px solid #388e3c;
                  padding:10px 14px; border-radius:4px; margin:6px 0;
                  color:#1a1a2e !important; }
    .rag-amber  { background:#fff8e1 !important; border-left:4px solid #f9a825;
                  padding:10px 14px; border-radius:4px; margin:6px 0;
                  color:#1a1a2e !important; }
    .rag-red    { background:#ffebee !important; border-left:4px solid #c62828;
                  padding:10px 14px; border-radius:4px; margin:6px 0;
                  color:#1a1a2e !important; }
    .rag-green *, .rag-amber *, .rag-red * { color: #1a1a2e !important; }
    .score-card { border:1px solid #e0e0e0; border-radius:8px; padding:18px; text-align:center; }
    .score-big  { font-size:3rem; font-weight:700; }
    .disclaimer { background:#f9f9f9 !important; color:#555 !important; border:1px solid #ddd;
                  border-radius:6px; padding:12px 16px; font-size:0.82rem; margin-top:24px; }
    .disclaimer * { color:#555 !important; }
    .nav-btn { margin-top: 20px; }
    .step-indicator { color: #888; font-size: 0.9rem; margin-bottom: 4px; }
    .question-block { margin-bottom: 20px; }
    .new-badge {
        display:inline-block; background:#d32f2f; color:white !important;
        font-size:0.7rem; padding:2px 7px; border-radius:10px;
        vertical-align:middle; margin-left:6px;
    }
    .copyright-footer {
        text-align: center; color: #999 !important; font-size: 0.75rem;
        margin-top: 40px; padding-top: 12px; border-top: 1px solid #e0e0e0;
    }
    /* Print styles — white background, dark text universally */
    @media print {
        .stApp, .main, body { background-color: white !important; }
        * { color: #1a1a2e !important; }
        .rag-green  { background: #e8f5e9 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .rag-amber  { background: #fff8e1 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .rag-red    { background: #ffebee !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .disclaimer { background: #f9f9f9 !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
        .stButton, .stDownloadButton { display: none !important; }
        .print-section { page-break-before: always; }
    }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ──────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "intro",
        "answers": {},
        "entity_type": None,
        "entity_size": None,
        "obligation_length": None,
        "current_pillar": 0,
        "completed_pillars": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# Handle ?demo=true in URL
if st.query_params.get("demo") == "true" and st.session_state.page == "intro":
    load_demo()
    st.rerun()


# ─── Navigation helpers ──────────────────────────────────────────────────────────
def go(page):
    st.session_state.page = page
    # Scroll to top on page navigation
    st.components.v1.html(
        "<script>window.parent.document.querySelector('.main').scrollTo(0, 0);</script>",
        height=0,
    )
    st.rerun()

def answer_key(section, qnum):
    return f"{section}_q{qnum}"


# ─── Progress bar ────────────────────────────────────────────────────────────────
PAGES_ORDER = ["intro", "classifier", "pillar_1", "pillar_2", "pillar_3",
               "pillar_4", "pillar_5", "kyc", "reporting", "recordkeeping",
               "directives", "sector", "report"]

def show_progress():
    if st.session_state.page in PAGES_ORDER:
        idx = PAGES_ORDER.index(st.session_state.page)
        pct = idx / (len(PAGES_ORDER) - 1)
        st.progress(pct)
        st.markdown(f"<div class='step-indicator'>Step {idx} of {len(PAGES_ORDER)-1}</div>",
                    unsafe_allow_html=True)


# ─── Reusable question renderer ──────────────────────────────────────────────────
def render_questions(section_key, questions):
    """Render a list of question dicts; store answers in session state."""
    all_answered = True
    for i, q in enumerate(questions):
        key = answer_key(section_key, i)
        st.markdown(f"<div class='question-block'>", unsafe_allow_html=True)

        label = q["text"]
        if q.get("new_2025"):
            label += " <span class='new-badge'>NEW 2025</span>"

        st.markdown(f"**{label}**", unsafe_allow_html=True)

        if q.get("hint"):
            st.caption(q["hint"])

        options = q["options"]
        current = st.session_state.answers.get(key)
        idx = options.index(current) if current in options else None

        answer = st.radio(
            label=" ",
            options=options,
            index=idx,
            key=f"radio_{section_key}_{i}",
            label_visibility="collapsed",
        )

        if answer:
            st.session_state.answers[key] = answer
        else:
            all_answered = False

        st.markdown("</div>", unsafe_allow_html=True)

    return all_answered


# ─── Disclaimer text ─────────────────────────────────────────────────────────────
DISCLAIMER_TEXT = """**Disclaimer & Terms of Use**
*Last updated: April 06, 2026*

**1. Nature of Service**
This tool is an automated self-assessment provided for educational and informational purposes only. It is designed to help users identify potential compliance gaps at a high level. It does not constitute legal, regulatory, accounting, financial, or professional compliance advice. Use of this tool does not create a solicitor-client, consultant-client, or any other professional advisory relationship.

**2. No Compliance Determination**
Results are indicative only and are based solely on the answers selected by the user. This tool does not certify compliance, does not constitute a FINTRAC assessment, and does not guarantee compliance with the Proceeds of Crime (Money Laundering) and Terrorist Financing Act (PCMLTFA), the associated regulations, FINTRAC guidance, or any other federal, provincial, or territorial legal requirement. Regulatory obligations are fact-specific and may differ based on entity type, activities, geography, and operating model.

**3. User Responsibility**
The user is solely responsible for the accuracy, completeness, and truthfulness of all inputs. The user is also responsible for independently verifying current legal and regulatory requirements before acting on any output from this tool. Laws, regulations, and FINTRAC guidance may change, and this tool may not reflect the most current version at the time of use.

**4. Scope Limitation**
This tool is limited to a preliminary AML/ATF self-assessment. It does not assess all possible obligations under federal or provincial law, and it does not replace a formal compliance program review, legal review, internal audit, or independent AML/ATF consultation.

**5. No Reliance**
Users agree not to rely on this tool or its output as the sole basis for compliance decisions, regulatory filings, or operational changes. Any reliance on the tool is at the user's own risk.

**6. Data Handling and Privacy**
This tool does not collect, store, or process client data, transaction data, or other personally identifiable information through the questionnaire. Responses are anonymous and used only to generate results within the current session. No analytics tools are used on this site.

**7. Limitation of Liability**
To the maximum extent permitted by applicable law, Asset Tech, its owners, officers, employees, contractors, affiliates, and agents shall not be liable for any direct, indirect, incidental, consequential, special, exemplary, or punitive damages, losses, penalties, fines, administrative monetary penalties, claims, costs, or expenses arising from or related to the use of, or reliance on, this tool or its results.

**8. Indemnity**
To the maximum extent permitted by law, the user agrees to indemnify, defend, and hold harmless Asset Tech and its affiliates from and against any claims, liabilities, losses, damages, costs, and expenses arising out of the user's use of this tool, the user's inputs, the user's reliance on the results, or the user's failure to obtain appropriate professional advice.

**9. Governing Law**
These Terms of Use are governed by the laws of the Province of Alberta and the federal laws of Canada applicable therein. Any dispute arising from or relating to this tool shall be subject to the exclusive jurisdiction of the courts of Alberta, unless applicable law requires otherwise.

**10. Changes and Availability**
Asset Tech may update, suspend, or discontinue this tool or these Terms of Use at any time without notice. Continued use of the tool after any update constitutes acceptance of the revised terms.

**11. Acceptance**
By checking the box below and clicking "Begin Assessment," you confirm that you have read, understood, and agree to these Terms of Use and Disclaimer.
"""

DISCLAIMER_SHORT = (
    "This tool provides a preliminary self-assessment only. Results are a heuristic indicator — "
    "they do not certify compliance, constitute a FINTRAC assessment, or replace professional legal "
    "or compliance advice. Do not rely on this output as the sole basis for compliance decisions, "
    "regulatory filings, or operational changes. © Asset Tech | Last updated: April 06, 2026"
)


# ─── PAGE: Intro ─────────────────────────────────────────────────────────────────
def page_intro():
    st.markdown("# 🍁 FINTRAC Readiness Assessment")
    st.markdown("### Know where you stand before FINTRAC comes to you.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**⏱ 15–20 minutes**\nComplete self-assessment")
    with col2:
        st.markdown("**📋 5 Compliance Pillars**\nPlus sector-specific checks")
    with col3:
        st.markdown("**📊 Instant Report**\nRAG scores + action plan")

    st.markdown("---")

    # ── Privacy statement ──
    st.markdown("""
<div style="background:#e8f5e9; border-left:4px solid #388e3c; padding:10px 16px;
            border-radius:4px; margin-bottom:16px; color:#1a1a2e;">
<strong>🔒 Privacy:</strong> This tool does not collect, store, or process any personal
information, client data, or transaction data. Your responses are anonymous and exist
only within your current browser session. No analytics tools are used on this site.
</div>
""", unsafe_allow_html=True)

    # ── Full disclaimer ──
    with st.expander("📋 Disclaimer & Terms of Use — read before proceeding", expanded=True):
        st.markdown(DISCLAIMER_TEXT)

    # ── Checkbox gate ──
    agreed = st.checkbox(
        "I have read and agree to the Disclaimer & Terms of Use.",
        key="terms_agreed",
        value=st.session_state.get("terms_agreed_value", False),
    )
    if agreed:
        st.session_state["terms_agreed_value"] = True

    st.markdown("---")

    # ── Who this is for ──
    st.markdown("""
This tool helps Canadian businesses assess their compliance with the
*Proceeds of Crime (Money Laundering) and Terrorist Financing Act* (PCMLTFA)
and FINTRAC's associated regulations — including the significant changes
that came into force in **April 2025** and **October 2025**.

**Who this is for:**
- Newly obligated entities (cheque cashers, factors, financing/leasing entities, private ABM acquirers, title insurers)
- Established reporting entities preparing for a FINTRAC examination
- Compliance officers, consultants, and legal advisors conducting preliminary gap assessments
""")

    # ── Buttons ──
    col_a, col_b = st.columns([3, 1])
    with col_a:
        if st.button(
            "Begin Assessment →",
            type="primary",
            use_container_width=True,
            disabled=not agreed,
        ):
            go("classifier")
    with col_b:
        if st.button("View Demo", use_container_width=True):
            load_demo()
            st.rerun()

    if not agreed:
        st.caption("Please read and accept the Disclaimer & Terms of Use to begin.")


# ─── PAGE: Entity Classifier ─────────────────────────────────────────────────────
def page_classifier():
    show_progress()
    st.markdown("## Step 1 — Tell us about your business")

    st.markdown("**What best describes your business type?**")
    entity = st.radio(
        " ",
        options=list(SECTORS.keys()),
        index=list(SECTORS.keys()).index(st.session_state.entity_type)
              if st.session_state.entity_type else None,
        label_visibility="collapsed",
        key="entity_radio",
    )

    st.markdown("**How long has your entity been subject to FINTRAC obligations?**")
    obligation = st.radio(
        " ",
        options=["Less than 6 months", "6–18 months", "2–5 years", "More than 5 years"],
        index=["Less than 6 months", "6–18 months", "2–5 years", "More than 5 years"]
              .index(st.session_state.obligation_length)
              if st.session_state.obligation_length else None,
        label_visibility="collapsed",
        key="obligation_radio",
    )

    st.markdown("**Approximately how many employees does your entity have?**")
    size = st.radio(
        " ",
        options=["1–5 (sole proprietor / micro)", "6–25 (small)", "26–100 (mid-size)", "101+ (large)"],
        index=["1–5 (sole proprietor / micro)", "6–25 (small)", "26–100 (mid-size)", "101+ (large)"]
              .index(st.session_state.entity_size)
              if st.session_state.entity_size else None,
        label_visibility="collapsed",
        key="size_radio",
    )

    col1, col2 = st.columns([1, 4])
    with col2:
        if st.button("Continue →", type="primary", disabled=not (entity and obligation and size)):
            st.session_state.entity_type = entity
            st.session_state.obligation_length = obligation
            st.session_state.entity_size = size
            go("pillar_1")
    with col1:
        if st.button("← Back"):
            go("intro")


# ─── PAGE: Pillar questions (generic renderer) ───────────────────────────────────
PILLAR_PAGES = {
    "pillar_1": {"title": "Pillar 1 — Compliance Officer",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng",
                 "key": "p1", "next": "pillar_2", "prev": "classifier"},
    "pillar_2": {"title": "Pillar 2 — Policies & Procedures",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng",
                 "key": "p2", "next": "pillar_3", "prev": "pillar_1"},
    "pillar_3": {"title": "Pillar 3 — Risk Assessment",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng",
                 "key": "p3", "next": "pillar_4", "prev": "pillar_2"},
    "pillar_4": {"title": "Pillar 4 — Training Program",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng",
                 "key": "p4", "next": "pillar_5", "prev": "pillar_3"},
    "pillar_5": {"title": "Pillar 5 — Effectiveness Review",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng",
                 "key": "p5", "next": "kyc", "prev": "pillar_4"},
    "kyc":      {"title": "Know Your Client (KYC)",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/Guide11/11-eng",
                 "key": "kyc", "next": "reporting", "prev": "pillar_5"},
    "reporting":{"title": "Transaction Reporting",
                 "source": "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/str-dod/str-dod-eng",
                 "key": "rep", "next": "recordkeeping", "prev": "kyc"},
    "recordkeeping": {"title": "Record Keeping",
                 "source": "https://fintrac-canafe.canada.ca/re-ed/fin-eng",
                 "key": "rec", "next": "directives", "prev": "reporting"},
    "directives":{"title": "Ministerial Directives",
                 "source": "https://fintrac-canafe.canada.ca/obligations/directives-eng",
                 "key": "dir", "next": "sector", "prev": "recordkeeping"},
}

def page_pillar(page_id):
    cfg = PILLAR_PAGES[page_id]
    show_progress()
    st.markdown(f"## {cfg['title']}")
    st.caption(f"📎 FINTRAC guidance: [{cfg['source']}]({cfg['source']})")

    questions = PILLAR_QUESTIONS[cfg["key"]]
    render_questions(cfg["key"], questions)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            go(cfg["prev"])
    with col2:
        if st.button("Continue →", type="primary"):
            go(cfg["next"])


# ─── PAGE: Sector-specific ───────────────────────────────────────────────────────
def page_sector():
    show_progress()
    entity = st.session_state.entity_type
    sector_info = SECTORS.get(entity, {})
    sector_key = sector_info.get("key")
    questions = SECTOR_QUESTIONS.get(sector_key, [])

    if not questions:
        st.markdown("## Sector-Specific Questions")
        st.info(f"No additional sector-specific questions for **{entity}**. "
                "Your assessment is based on the universal compliance pillars above.")
    else:
        label = sector_info.get("label", entity)
        is_new = sector_info.get("new_2025", False)
        badge = " <span class='new-badge'>NEW 2025</span>" if is_new else ""
        st.markdown(f"## Sector-Specific: {label}{badge}", unsafe_allow_html=True)

        if is_new:
            st.warning(f"⚠️ Your sector became subject to FINTRAC obligations in 2025. "
                       "These questions are especially important for your compliance status.")

        source = sector_info.get("source", "")
        if source:
            st.caption(f"📎 FINTRAC sector guidance: [{source}]({source})")

        render_questions(f"sec_{sector_key}", questions)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            go("directives")
    with col2:
        if st.button("Generate My Report →", type="primary"):
            go("report")


# ─── Scoring engine ──────────────────────────────────────────────────────────────
def compute_scores():
    """Returns dict of section_key -> {score, max, pct, rag, gaps}"""
    answers = st.session_state.answers
    entity = st.session_state.entity_type
    sector_key = SECTORS.get(entity, {}).get("key")

    sections = {}
    # Universal pillars + sections
    for section_key, questions in PILLAR_QUESTIONS.items():
        pts, max_pts, gaps = 0, 0, []
        for i, q in enumerate(questions):
            key = answer_key(section_key, i)
            ans = answers.get(key)
            score = get_score(ans)
            if score is None:   # not applicable — already handled below, so skip
                continue
            if ans and ans.lower().startswith("not applicable"):
                continue
            max_pts += 2
            pts += score
            if score < 2:
                gaps.append({"q": q["text"], "answer": ans, "score": score})
        pct = (pts / max_pts * 100) if max_pts > 0 else 100
        sections[section_key] = {
            "score": pts, "max": max_pts, "pct": round(pct),
            "rag": rag(pct), "gaps": gaps
        }

    # Sector-specific
    if sector_key:
        s_questions = SECTOR_QUESTIONS.get(sector_key, [])
        pts, max_pts, gaps = 0, 0, []
        for i, q in enumerate(s_questions):
            key = answer_key(f"sec_{sector_key}", i)
            ans = answers.get(key)
            score = get_score(ans)
            if score is None:   # not applicable — already handled below, so skip
                continue
            if ans and ans.lower().startswith("not applicable"):
                continue
            max_pts += 2
            pts += score
            if score < 2:
                gaps.append({"q": q["text"], "answer": ans, "score": score})
        pct = (pts / max_pts * 100) if max_pts > 0 else 100
        sections[f"sec_{sector_key}"] = {
            "score": pts, "max": max_pts, "pct": round(pct),
            "rag": rag(pct), "gaps": gaps, "label": "Sector-Specific Obligations"
        }

    # Overall
    total_pts = sum(v["score"] for v in sections.values())
    total_max = sum(v["max"] for v in sections.values())
    overall_pct = (total_pts / total_max * 100) if total_max > 0 else 100

    return sections, round(overall_pct)

def rag(pct):
    if pct >= 80: return "green"
    if pct >= 50: return "amber"
    return "red"

RAG_EMOJI = {"green": "🟢", "amber": "🟡", "red": "🔴"}
RAG_LABEL = {"green": "Substantially Compliant", "amber": "Material Gaps", "red": "Significant Risk"}

SECTION_LABELS = {
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


# ─── PAGE: Report ────────────────────────────────────────────────────────────────
def page_report():
    show_progress()
    sections, overall_pct = compute_scores()
    overall_rag = rag(overall_pct)
    entity = st.session_state.entity_type

    # ── Header ──
    st.markdown("## 📊 Your FINTRAC Readiness Report")
    st.caption(f"Generated: {datetime.date.today().strftime('%B %d, %Y')} · Entity type: {entity}")

    # ── Overall score card ──
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        color = {"green": "#388e3c", "amber": "#f9a825", "red": "#c62828"}[overall_rag]
        st.markdown(f"""
        <div class='score-card' style='border-top: 5px solid {color};'>
            <div style='color:{color}' class='score-big'>{overall_pct}%</div>
            <div style='font-size:1.1rem; font-weight:600;'>{RAG_EMOJI[overall_rag]} {RAG_LABEL[overall_rag]}</div>
            <div style='color:#777; font-size:0.9rem; margin-top:4px;'>Overall Readiness Score</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Score warning banner — shown for all results ──
    st.markdown("""
<div style="background:#fff8e1; border-left:4px solid #f9a825; padding:10px 16px;
            border-radius:4px; margin:12px 0; color:#1a1a2e;">
<strong>⚠️ Important:</strong> This score is a heuristic indicator based solely on your
self-reported answers. It does not certify compliance, does not constitute a FINTRAC
assessment, and must not be used as the sole basis for compliance decisions, regulatory
filings, or operational changes. Consult a qualified AML/ATF professional for a formal review.
</div>
""", unsafe_allow_html=True)

    # ── High-risk banner — shown only for Red overall score ──
    if overall_rag == "red":
        st.markdown("""
<div style="background:#ffebee; border:2px solid #c62828; padding:12px 16px;
            border-radius:4px; margin-bottom:12px; color:#1a1a2e;">
<strong>🔴 Significant gaps identified.</strong> Do not rely on this output for regulatory
filings, submissions to FINTRAC, or compliance representations to third parties.
Engage a qualified AML/ATF compliance professional or legal counsel before taking
action based on these results.
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Pillar-by-pillar breakdown ──
    st.markdown("<div class='print-section'>", unsafe_allow_html=True)
    st.markdown("### Compliance Pillar Breakdown")

    for sec_key, data in sections.items():
        label = SECTION_LABELS.get(sec_key, data.get("label", sec_key))
        r = data["rag"]
        pct = data["pct"]
        bar_color = {"green": "#388e3c", "amber": "#f9a825", "red": "#c62828"}[r]

        st.markdown(f"""
        <div class='rag-{r}'>
            <strong>{RAG_EMOJI[r]} {label}</strong>
            <span style='float:right; font-weight:700; color:{bar_color};'>{pct}%</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Top gaps ──
    st.markdown("<div class='print-section'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Priority Gaps")

    all_gaps = []
    for sec_key, data in sections.items():
        label = SECTION_LABELS.get(sec_key, data.get("label", sec_key))
        for gap in data["gaps"]:
            all_gaps.append({**gap, "section": label})

    all_gaps.sort(key=lambda x: x["score"])

    if not all_gaps:
        st.success("✅ No significant gaps identified. Maintain your program and ensure "
                   "your effectiveness review is completed every 24 months.")
    else:
        red_gaps = [g for g in all_gaps if g["score"] == 0]
        amber_gaps = [g for g in all_gaps if g["score"] == 1]

        if red_gaps:
            st.markdown("#### 🔴 Critical")
            for g in red_gaps[:8]:
                st.markdown(f"- **{g['section']}:** {g['q']}")

        if amber_gaps:
            st.markdown("#### 🟡 Moderate")
            for g in amber_gaps[:8]:
                st.markdown(f"- **{g['section']}:** {g['q']}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Action plan ──
    st.markdown("<div class='print-section'>", unsafe_allow_html=True)
    st.markdown("### 📅 Recommended Action Plan")

    newly_obligated = st.session_state.obligation_length in ["Less than 6 months", "6–18 months"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Phase 1**")
        if sections.get("p1", {}).get("pct", 100) < 80:
            st.markdown("- Formally appoint a Compliance Officer with documented authority")
        if sections.get("p3", {}).get("pct", 100) < 80:
            st.markdown("- Begin your documented ML/TF risk assessment")
        if newly_obligated:
            st.markdown("- Confirm your entity classification with legal counsel")
        st.markdown("- Register with FINTRAC if required for your sector")

    with col2:
        st.markdown("**Phase 2**")
        if sections.get("p2", {}).get("pct", 100) < 80:
            st.markdown("- Draft or update sector-specific policies and procedures")
        if sections.get("kyc", {}).get("pct", 100) < 80:
            st.markdown("- Implement client identification and verification procedures")
        if sections.get("p4", {}).get("pct", 100) < 80:
            st.markdown("- Complete staff AML/ATF training and retain records")
        st.markdown("- Review and implement Ministerial Directive obligations")

    with col3:
        st.markdown("**Phase 3**")
        if sections.get("p5", {}).get("pct", 100) < 80:
            st.markdown("- Schedule an independent effectiveness review")
        if sections.get("rep", {}).get("pct", 100) < 80:
            st.markdown("- Verify STR, LCTR and EFTR reporting procedures are operational")
        if sections.get("rec", {}).get("pct", 100) < 80:
            st.markdown("- Implement a 5-year records retention policy")
        st.markdown("- Test your STR identification process with a tabletop scenario")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Key FINTRAC resources ──
    st.markdown("<div class='print-section'>", unsafe_allow_html=True)
    st.markdown("### 📚 Key FINTRAC Resources for Your Sector")
    sector_info = SECTORS.get(entity, {})
    sector_source = sector_info.get("source", "")

    resources = [
        ("Compliance Program Requirements", "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng"),
        ("Risk Assessment Guidance", "https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng"),
        ("Methods to Verify Identity", "https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/Guide11/11-eng"),
        ("Reporting Suspicious Transactions", "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/str-dod/str-dod-eng"),
        ("Beneficial Ownership Requirements", "https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/bor-eng"),
        ("Ministerial Directives", "https://fintrac-canafe.canada.ca/obligations/directives-eng"),
    ]
    if sector_source:
        resources.insert(0, (f"Sector Guidance — {entity}", sector_source))

    for label, url in resources:
        st.markdown(f"- [{label}]({url})")
    st.markdown("</div>", unsafe_allow_html=True)

#    st.markdown("---")

    # ── Sector-specific product offer ──
    st.markdown("<div class='print-section'>", unsafe_allow_html=True)
    sector_key = SECTORS.get(st.session_state.entity_type, {}).get("key", "other")
    render_offer_card(sector_key)

    # ── Disclaimer ──
    st.markdown("<div class='print-section'>", unsafe_allow_html=True)
#    st.markdown("""
#<div class='disclaimer'>
#<strong>⚠️ Important Disclaimer:</strong> This assessment tool provides a high-level preliminary
#self-assessment only. It does not constitute legal advice, compliance certification, or a formal
#FINTRAC gap assessment. Results reflect the answers provided and may not capture all obligations
#applicable to your specific circumstances. Regulatory obligations under the PCMLTFA and associated
#Regulations are complex and fact-specific. You should consult a qualified AML/ATF compliance
#professional or legal counsel before relying on these results. All guidance links reference
#<a href="https://fintrac-canafe.canada.ca" target="_blank">fintrac-canafe.canada.ca</a> —
#always verify against the current published version.
#</div>
#""", unsafe_allow_html=True)

    # ── Full Terms of Use (always visible for print) ──
    st.markdown("---")
    st.markdown(DISCLAIMER_TEXT)
    st.caption("Last updated: April 06, 2026")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Retake Assessment"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_state()
            go("intro")
    with col2:
        try:
            pdf_bytes = generate_pdf(
                sections, overall_pct,
                st.session_state.entity_type,
                st.session_state.entity_size,
                st.session_state.obligation_length,
            )
            st.download_button(
                label="⬇ Download PDF Report",
                data=pdf_bytes,
                file_name=f"FINTRAC_Readiness_Report_{datetime.date.today()}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
        except Exception as e:
            st.info("💾 Use your browser's print function (Ctrl+P / Cmd+P) to save this report as PDF.")


    st.markdown("""
<div class='copyright-footer'>
    &copy Asset Tech. All rights reserved.
</div>
""", unsafe_allow_html=True)

# ─── Router ──────────────────────────────────────────────────────────────────────
def main():
    page = st.session_state.page

    if page == "intro":
        page_intro()
    elif page == "classifier":
        page_classifier()
    elif page in PILLAR_PAGES:
        page_pillar(page)
    elif page == "sector":
        page_sector()
    elif page == "report":
        page_report()
    else:
        go("intro")


if __name__ == "__main__":
    main()
