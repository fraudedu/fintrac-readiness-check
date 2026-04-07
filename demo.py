"""
demo.py — Pre-filled demo answers simulating a newly-obligated financing/leasing entity
(mid-size, obligated less than 6 months) with realistic mixed Red/Amber/Green scores.

The scenario: A 40-person equipment leasing company in Calgary. They have a compliance
officer on paper but no real program in place. Typical of entities caught by the April 2025
PCMLTFA expansion with zero prior FINTRAC experience.

Usage in app.py:
    from demo import DEMO_ANSWERS, DEMO_ENTITY, DEMO_SIZE, DEMO_OBLIGATION, load_demo
    if st.query_params.get("demo") == "true":
        load_demo()
"""

import streamlit as st

DEMO_ENTITY     = "Demo entity"
DEMO_SIZE       = "26–100 (mid-size)"
DEMO_OBLIGATION = "Less than 6 months"

DEMO_ANSWERS = {

    # ── Pillar 1: Compliance Officer ──────────────────────────────────────────
    # Has someone, but role is weak and unsupported
    "p1_q0": "Yes — formally appointed with written documentation",
    "p1_q1": "Partial — the role exists but authority is not clearly defined",
    "p1_q2": "No — they report only to a middle manager with no board access",
    "p1_q3": "Partial — some knowledge but no formal training record",
    "p1_q4": "No",

    # ── Pillar 2: Policies & Procedures ──────────────────────────────────────
    # Downloaded a template, never customised it
    "p2_q0": "Yes — but they are generic/template-based and not tailored to your business",
    "p2_q1": "Partial — some elements are addressed but not all",   # ← NEW: compliance program coverage
    "p2_q2": "Partial",        # was p2_q1
    "p2_q3": "No",             # was p2_q2
    "p2_q4": "No",             # was p2_q3
    "p2_q5": "No",             # was p2_q4
    "p2_q6": "Partial",        # was p2_q5
    "p2_q7": "No",             # was p2_q6
    "p2_q8": "No — more than 2 years ago / never reviewed since creation",  # was p2_q7
    "p2_q9": "No — still operating on old or no policies",                  # was p2_q8
    "p2_q10": "Partial — they exist but staff awareness is inconsistent",   # was p2_q9

    # ── Pillar 3: Risk Assessment ─────────────────────────────────────────────
    # Nothing documented — common for newly-obligated entities
    "p3_q0": "Partial — an informal assessment was done but not documented",
    "p3_q1": "Partial — some categories are covered but not all",
    "p3_q2": "No — more than 4 years ago / never",
    "p3_q3": "No",
    "p3_q4": "Partial — the assessment is generic and does not reflect our specific model",
    "p3_q5": "No",
    "p3_q6": "Not yet completed",

    # ── Pillar 4: Training ────────────────────────────────────────────────────
    # Nothing formal — onboarding mentions AML vaguely
    "p4_q0": "Yes — training happens but is informal with no records",
    "p4_q1": "Partial — some topics are covered but not all",
    "p4_q2": "Partial — one or neither is covered",
    "p4_q3": "No",
    "p4_q4": "Partial — at onboarding only",
    "p4_q5": "No",
    "p4_q6": "No — all staff receive the same generic training",
    "p4_q7": "No — training has not been updated",

    # ── Pillar 5: Effectiveness Review ───────────────────────────────────────
    # Never done
    "p5_q0": "No — never conducted",
    "p5_q1": "No review has been conducted",
    "p5_q2": "No review was conducted",
    "p5_q3": "No",

    # ── KYC ──────────────────────────────────────────────────────────────────
    # Basic ID checking but no framework
    "kyc_q0": "Partial — procedures exist but are not consistently followed",
    "kyc_q1": "Partial — methods are used but not formalised",
    "kyc_q2": "No — we only verify individuals",
    "kyc_q3": "No",
    "kyc_q4": "No",
    "kyc_q5": "Partial — at onboarding only",
    "kyc_q6": "No",
    "kyc_q7": "Partial — some monitoring occurs but it is not systematic",

    # ── Transaction Reporting ─────────────────────────────────────────────────
    # Unaware of STR obligations
    "rep_q0": "Partial — procedures exist but staff awareness is inconsistent",
    "rep_q1": "No — we were not aware of this timing requirement",
    "rep_q2": "No",
    "rep_q3": "Partial — we are aware of the requirement but procedures are not formalised",
    "rep_q4": "Not applicable — we do not conduct international EFTs",
    "rep_q5": "Not applicable — we do not conduct EFTs",
    "rep_q5": "Not applicable — we do not handle virtual currency",

    # ── Record Keeping ────────────────────────────────────────────────────────
    # Keeps records but no retention policy
    "rec_q0": "Partial — records are kept but the five-year period is not formally managed",
    "rec_q1": "Probably — but retrieval is manual and may take time",
    "rec_q2": "Partial — format is inconsistent",
    "rec_q3": "Partial — some categories are retained but not all",

    # ── Ministerial Directives ────────────────────────────────────────────────
    # Completely unaware
    "dir_q0": "Not aware",
    "dir_q1": "No",
    "dir_q2": "No",
    "dir_q3": "No — not yet updated",

    # ── Sector-Specific: Leasing/Financing ───────────────────────────────────
    "sec_lease_q0": "We believe so based on our own reading",
    "sec_lease_q1": "No — we were not aware registration may be required",
    "sec_lease_q2": "Partial — some activities are identified but not all",
    "sec_lease_q3": "No",
    "sec_lease_q4": "No",
}


def load_demo():
    """Load demo state into Streamlit session. Call from app.py before rendering."""
    st.session_state.entity_type     = DEMO_ENTITY
    st.session_state.entity_size     = DEMO_SIZE
    st.session_state.obligation_length = DEMO_OBLIGATION
    st.session_state.answers         = dict(DEMO_ANSWERS)
    st.session_state.page            = "report"
