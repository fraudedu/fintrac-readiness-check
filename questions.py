"""
questions.py — All FINTRAC assessment questions and sector definitions.

SCORE_MAP maps answer prefixes to points:
  2 = fully compliant (Green)
  1 = partial (Amber)
  0 = non-compliant or unaware (Red)
  "not applicable" = excluded from scoring
"""

# ─── Score mapping ────────────────────────────────────────────────────────────────
# Keys are matched by startswith() in lowercase — order matters (most specific first)
SCORE_MAP = {
    "Yes — fully":           2,
    "Yes — formal":          2,
    "Yes — comprehensive":   2,
    "Yes — documented":      2,
    "Yes — registered":      2,
    "Yes — completed":       2,
    "Yes — in compliance":   2,
    "Yes — verified":        2,
    "Yes — sector-specific": 2,
    "Yes — procedures":      2,
    "Yes — monitoring":      2,
    "Yes — policy":          2,
    "Yes — training":        2,
    "Yes — fully mapped":    2,
    "Yes — fully updated":   2,
    "Yes — formally":        2,
    "Yes — records":         2,
    "Yes":                   2,
    "An independent":        2,
    "An external":           2,
    "Myself / the compliance officer — we do not have":  1,
    "Partial":               1,
    "In progress":           1,
    "Probably":              1,
    "Aware":                 1,
    "Completed after":       1,
    "We believe":            1,
    "Believe":               1,
    "Yes — but":             1,
    "Not yet":               0,
    "No —":                  0,
    "No":                    0,
    "Never":                 0,
    "Not aware":             0,
    "Unsure":                0,
    "Not applicable":        None,  # excluded from score
    "Not sure":              0,
}

def get_score(answer):
    if not answer:
        return 0
    a = answer.strip()
    if a.lower().startswith("not applicable"):
        return None
    for prefix, score in SCORE_MAP.items():
        if a.startswith(prefix):
            return score if score is not None else None
    return 0


# ─── Sector definitions ──────────────────────────────────────────────────────────
SECTORS = {
    "Acquirer services for private ABMs (ATMs)": {
        "key": "abm", "label": "Private ABM Acquirers",
        "new_2025": True,
        "source": "https://fintrac-canafe.canada.ca/re-ed/abm-gap-eng",
    },
    "Cheque casher": {
        "key": "cheque", "label": "Cheque Cashers",
        "new_2025": True,
        "source": "https://fintrac-canafe.canada.ca/re-ed/cheque-eng",
    },
    "Factor (accounts receivable financing)": {
        "key": "factor", "label": "Factors",
        "new_2025": True,
        "source": "https://fintrac-canafe.canada.ca/re-ed/fact-affact-eng",
    },
    "Financing or leasing entity": {
        "key": "lease", "label": "Financing / Leasing Entities",
        "new_2025": True,
        "source": "https://fintrac-canafe.canada.ca/re-ed/lease-bail-eng",
    },
    "Title insurer": {
        "key": "title", "label": "Title Insurers",
        "new_2025": True,
        "source": "https://fintrac-canafe.canada.ca/re-ed/title-titre-eng",
    },
    "Accountant or accounting firm": {
        "key": "acct", "label": "Accountants",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/accts-eng",
    },
    "Casino": {
        "key": "casino", "label": "Casinos",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/casinos-eng",
    },
    "Dealer in precious metals and precious stones": {
        "key": "dpms", "label": "Dealers in Precious Metals/Stones",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/dpms-eng",
    },
    "Financial entity (bank, credit union, trust/loan company)": {
        "key": "fin", "label": "Financial Entities",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/fin-eng",
    },
    "Life insurance company, broker or agent": {
        "key": "li", "label": "Life Insurance",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/li-eng",
    },
    "Money services business (MSB) — currency exchange, remittance, crypto": {
        "key": "msb", "label": "Money Services Businesses",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/msb-esm/msb-eng",
    },
    "Mortgage administrator, broker or lender": {
        "key": "mort", "label": "Mortgage Entities",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/mortgage-hypotheque-eng",
    },
    "Real estate broker, sales representative or developer": {
        "key": "re", "label": "Real Estate",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/real-eng",
    },
    "Securities dealer": {
        "key": "sec", "label": "Securities Dealers",
        "new_2025": False,
        "source": "https://fintrac-canafe.canada.ca/re-ed/sec-eng",
    },
    "Other / Not sure": {
        "key": "other", "label": "Other",
        "new_2025": False,
        "source": "",
    },
}


# ─── Universal Pillar Questions ──────────────────────────────────────────────────

PILLAR_QUESTIONS = {

    # ── Pillar 1: Compliance Officer ──
    "p1": [
        {
            "text": "Has your entity designated a compliance officer responsible for implementing your AML/CFT compliance program?",
            "options": [
                "Yes — formally appointed with written documentation",
                "Yes — but the role is informal and not documented",
                "No",
            ],
        },
        {
            "text": "Does the designated compliance officer have sufficient authority to implement and enforce the compliance program?",
            "options": [
                "Yes — authority is documented (job description, board resolution, or equivalent)",
                "Partial — the role exists but authority is not clearly defined",
                "No — the compliance function has no formal authority",
            ],
        },
        {
            "text": "Is the compliance officer sufficiently senior to report compliance issues directly to senior management or the board?",
            "options": [
                "Yes",
                "No — they report only to a middle manager with no board access",
                "Not sure",
            ],
        },
        {
            "text": "Does your compliance officer have documented AML/CFT knowledge or training relevant to your sector?",
            "options": [
                "Yes — formal training or certification on record",
                "Partial — some knowledge but no formal training record",
                "No",
            ],
        },
        {
            "text": "If the compliance officer left tomorrow, is there a documented backup or succession plan?",
            "options": [
                "Yes",
                "No",
                "Not applicable (sole proprietor)",
            ],
        },
    ],

    # ── Pillar 2: Policies & Procedures ──
    "p2": [
        {
            "text": "Does your entity have written AML/CFT policies and procedures?",
            "options": [
                "Yes — comprehensive, sector-specific, and currently in force",
                "Yes — but they are generic/template-based and not tailored to your business",
                "Partial — some procedures exist but they are incomplete",
                "No",
            ],
        },
        {
            "text": "Do your written policies cover your overall compliance program — including the five required elements (compliance officer, policies and procedures, risk assessment, training, and effectiveness review)?",
            "hint": "Source: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng",
            "options": [
                "Yes — all five compliance program elements are addressed in our policies",
                "Partial — some elements are addressed but not all",
                "No",
            ],
        },
        {
            "text": "Do your written policies cover client identification and verification (KYC)?",
            "options": ["Yes", "Partial", "No"],
        },
        {
            "text": "Do your written policies cover business relationship establishment, ongoing monitoring, and termination?",
            "options": ["Yes", "Partial", "No"],
        },
        {
            "text": "Do your written policies cover beneficial ownership determination and third-party determination (where applicable)?",
            "options": ["Yes", "Partial", "No", "Not applicable"],
        },
        {
            "text": "Do your written policies cover PEP and HIO screening and enhanced due diligence?",
            "options": ["Yes", "Partial", "No", "Not applicable"],
        },
        {
            "text": "Do your written policies cover transaction reporting (STR, LPEPR, LCTR, LVCTR, and EFTR where applicable)?",
            "options": ["Yes", "Partial", "No"],
        },
        {
            "text": "Do your written policies cover record-keeping, retention periods, and Ministerial Directive compliance?",
            "options": ["Yes", "Partial", "No"],
        },
        {
            "text": "When were your policies and procedures last reviewed and updated?",
            "options": [
                "Yes — within the last 12 months",
                "Partial — 1–2 years ago",
                "No — more than 2 years ago / never reviewed since creation",
            ],
        },
        {
            "text": "Were your policies specifically updated to reflect 2025 regulatory changes?",
            "new_2025": True,
            "options": [
                "Yes — fully updated before or shortly after the effective date",
                "In progress — updates are underway",
                "No — still operating on old or no policies",
                "Not applicable (not a newly obligated entity)",
            ],
        },
        {
            "text": "Are your policies and procedures accessible to all relevant staff at all times?",
            "options": [
                "Yes — centrally stored and staff know where to find them",
                "Partial — they exist but staff awareness is inconsistent",
                "No",
            ],
        },
    ],

    # ── Pillar 3: Risk Assessment ──
    "p3": [
        {
            "text": "Has your entity completed a documented business-wide ML/TF risk assessment?",
            "options": [
                "Yes — documented, approved by senior management, and dated",
                "Partial — an informal assessment was done but not documented",
                "No",
            ],
        },
        {
            "text": "Does your risk assessment cover your products/services, client types, geographic exposure, delivery channels, and new technologies?",
            "options": [
                "Yes — all five risk factor categories are addressed",
                "Partial — some categories are covered but not all",
                "No",
            ],
        },
        {
            "text": "When was your risk assessment last updated?",
            "options": [
                "Yes — within the last 24 months (meets FINTRAC's two-year review cycle)",
                "Partial — 2–4 years ago (overdue)",
                "No — more than 4 years ago / never",
            ],
        },
        {
            "text": "Does your risk assessment result in a documented client risk rating methodology (e.g. low / medium / high)?",
            "options": [
                "Yes — clients are formally rated based on defined criteria",
                "Partial — some client segmentation exists but it is not systematic",
                "No",
            ],
        },
        {
            "text": "Does your risk assessment address ML/TF risks specific to your sector and business model?",
            "options": [
                "Yes — sector-specific risks are explicitly identified",
                "Partial — the assessment is generic and does not reflect our specific model",
                "No",
            ],
        },
        {
            "text": "Are enhanced due diligence (EDD) measures documented and consistently applied to high-risk clients?",
            "options": [
                "Yes — EDD triggers are defined and applied consistently",
                "Partial — some enhanced measures exist but are applied inconsistently",
                "No",
            ],
        },
        {
            "text": "Did you complete an initial risk assessment before your FINTRAC obligations came into force?",
            "new_2025": True,
            "options": [
                "Yes — completed before the effective date",
                "Completed after the effective date",
                "Not yet completed",
                "Not applicable (existing obligated entity)",
            ],
        },
    ],

    # ── Pillar 4: Training ──
    "p4": [
        {
            "text": "Does your entity have a documented AML/CFT training program?",
            "options": [
                "Yes — formal, documented, with training records per employee",
                "Yes — training happens but is informal with no records",
                "No",
            ],
        },
        {
            "text": "Does the training program cover PCMLTFA obligations, KYC procedures, and how to recognise ML/TF red flags relevant to your sector?",
            "options": [
                "Yes — all of the above are covered",
                "Partial — some topics are covered but not all",
                "No",
            ],
        },
        {
            "text": "Does the training cover how and when to file an STR and an LCTR (where applicable), including timing requirements?",
            "options": [
                "Yes — STR and LCTR (where applicable) filing procedures are part of training",
                "Partial — one or neither is covered",
                "No",
            ],
        },
        {
            "text": "Does the training cover Ministerial Directive restrictions?",
            "options": [
                "Yes",
                "Partial — mentioned but not in depth",
                "No",
            ],
        },
        {
            "text": "How frequently are employees trained?",
            "options": [
                "Yes — at onboarding AND on an ongoing/annual basis",
                "Partial — at onboarding only",
                "No — ad hoc with no regular schedule / no training provided",
            ],
        },
        {
            "text": "Are training records (dates, attendees, content) retained for potential FINTRAC examination?",
            "options": [
                "Yes — records are maintained and could be produced within 30 days",
                "Partial — some records exist but they are incomplete",
                "No",
            ],
        },
        {
            "text": "Is training tailored to roles? (e.g. front-line staff vs compliance officer receive different content)",
            "options": [
                "Yes — role-based training is in place",
                "Partial — some differentiation but not systematic",
                "No — all staff receive the same generic training",
            ],
        },
        {
            "text": "Was training updated to reflect the 2025 regulatory changes?",
            "new_2025": True,
            "options": [
                "Yes — fully updated before or shortly after the effective date",
                "In progress",
                "No — training has not been updated",
                "Not applicable (not affected by 2025 changes)",
            ],
        },
    ],

    # ── Pillar 5: Effectiveness Review ──
    "p5": [
        {
            "text": "Has your entity conducted a formal review of the effectiveness of your compliance program within the last 24 months?",
            "options": [
                "Yes — reviewed within the last 24 months as required",
                "Partial — reviewed but more than 24 months ago (overdue)",
                "No — never conducted",
            ],
        },
        {
            "text": "Who conducted the effectiveness review?",
            "hint": "FINTRAC guidance states the review may be carried out by an internal or external auditor, or by yourself if you do not have an auditor. Source: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng",
            "options": [
                "An independent internal audit function",
                "An external third-party reviewer",
                "Myself / the compliance officer — we do not have an internal or external auditor",
                "Partial — the compliance officer reviewed their own program but an auditor is available and was not engaged",
                "No review has been conducted",
            ],
        },
        {
            "text": "Did the effectiveness review result in documented findings and a remediation plan that was actioned?",
            "options": [
                "Yes — findings were documented and a remediation plan was actioned",
                "Partial — findings were noted but no remediation plan was created",
                "No review was conducted",
            ],
        },
        {
            "text": "Were the results of the effectiveness review reported to senior management or the board?",
            "options": [
                "Yes",
                "No",
                "Not applicable (sole proprietor / owner-operated)",
            ],
        },
    ],

    # ── KYC ──
    "kyc": [
        {
            "text": "Does your entity have documented procedures for verifying the identity of clients at the thresholds required by your sector?",
            "options": [
                "Yes — procedures are documented and consistently applied",
                "Partial — procedures exist but are not consistently followed",
                "No",
            ],
        },
        {
            "text": "Are formal identity verification methods used (e.g. government-issued photo ID, credit file method, dual-process method)?",
            "hint": "Accepting self-declared information without verification does not satisfy FINTRAC requirements.",
            "options": [
                "Yes — documented methods are consistently applied",
                "Partial — methods are used but not formalised",
                "No — no formal verification method is in place",
            ],
        },
        {
            "text": "Does your entity verify the identity of corporate/entity clients (not just individuals)?",
            "options": [
                "Yes — entity verification procedures are documented",
                "Partial — we only sometimes verify entities",
                "No — we only verify individuals",
                "Not applicable — our entity only has individual clients",
            ],
        },
        {
            "text": "Does your entity collect and verify beneficial ownership information for corporate clients, in compliance with the October 2025 updated requirements?",
            "new_2025": True,
            "hint": "Source: https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/bor-eng",
            "options": [
                "Yes — in compliance with the updated beneficial ownership requirements",
                "Partial — some collection but not systematic or updated for 2025",
                "No",
                "Not applicable",
            ],
        },
        {
            "text": "Does your entity determine whether a client is acting on behalf of a third party?",
            "options": [
                "Yes — third-party determination procedures are in place for relevant transactions",
                "Partial",
                "No",
                "Not applicable",
            ],
        },
        {
            "text": "Does your entity screen clients against PEP and HIO lists at onboarding and on an ongoing basis?",
            "hint": "One-time screening at onboarding is insufficient — ongoing monitoring is required.",
            "options": [
                "Yes — screening is done at onboarding AND on an ongoing basis",
                "Partial — at onboarding only",
                "No",
                "Not applicable",
            ],
        },
        {
            "text": "For clients identified as PEPs or HIOs, does your entity apply the required enhanced measures and document them?",
            "options": [
                "Yes — enhanced due diligence is applied and documented",
                "Partial — we identify PEPs/HIOs but do not consistently apply enhanced measures",
                "No",
                "Not applicable — no PEP/HIO clients identified (note: this does not eliminate the obligation to screen)",
            ],
        },
        {
            "text": "Does your entity conduct ongoing monitoring of business relationships in accordance with FINTRAC requirements?",
            "options": [
                "Yes — ongoing monitoring procedures are documented and applied",
                "Partial — some monitoring occurs but it is not systematic",
                "No",
            ],
        },
    ],

    # ── Transaction Reporting ──
    "rep": [
        {
            "text": "Does your entity have documented procedures for identifying and reporting Suspicious Transactions (STRs)?",
            "options": [
                "Yes — staff know the triggers, process, and filing deadline",
                "Partial — procedures exist but staff awareness is inconsistent",
                "No",
            ],
        },
        {
            "text": "Does your entity understand that an STR must be submitted as soon as practicable after suspicion is formed — not at end of day or end of week?",
            "hint": "The 'as soon as practicable' standard is strictly interpreted by FINTRAC.",
            "options": [
                "Yes — this is documented and staff are trained on it",
                "Partial — we are aware but it is not formally documented",
                "No — we were not aware of this timing requirement",
            ],
        },
        {
            "text": "Does your entity have sector-specific ML/TF indicators that staff are trained to recognise?",
            "options": [
                "Yes — sector-specific indicators are incorporated into training and procedures",
                "Partial — generic indicators are used but not sector-specific ones",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures to identify and report Large Cash Transactions (CAD $10,000 or more, single or aggregated within 24 hours)?",
            "options": [
                "Yes — LCTR procedures are in place and staff are trained",
                "Partial — we are aware of the requirement but procedures are not formalised",
                "No",
                "Not applicable — our sector does not receive large cash transactions",
            ],
        },
        {
            "text": "Does your entity have procedures to identify and report Electronic Funds Transfers (EFTs) of CAD $10,000 or more to FINTRAC?",
            "hint": "The EFT reporting threshold is $10,000 CAD (single transaction or aggregated within 24 hours). Source: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/eft-dt/eft-dt-eng",
            "options": [
                "Yes — EFTR procedures are in place and staff are trained",
                "Partial — we are aware of the requirement but procedures are not formalised",
                "No",
                "Not applicable — we do not conduct international EFTs",
            ],
        },
        {
            "text": "When initiating or transmitting EFTs, does your entity include the required originator and beneficiary information in accordance with the Travel Rule?",
            "hint": "The Travel Rule requires originator and beneficiary information to be transmitted with EFTs. This is separate from the $10,000 EFTR reporting obligation. Source: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/travel-acheminement/1-eng",
            "options": [
                "Yes — originator and beneficiary information is transmitted as required",
                "Partial — compliance is inconsistent",
                "No",
                "Not applicable — we do not conduct EFTs",
            ],
        },
        {
            "text": "Does your entity have procedures for reporting virtual currency transactions of CAD $10,000 or more, where applicable?",
            "hint": "The LVCTs threshold is $10,000 CAD (single transaction or aggregated within 24 hours). Source: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/lvctr/lvctr-eng",
            "options": [
                "Yes — virtual currency reporting procedures are in place",
                "Partial",
                "No",
                "Not applicable — we do not handle virtual currency",
            ],
        },
    ],

    # ── Record Keeping ──
    "rec": [
        {
            "text": "Does your entity retain transaction and client identification records for the minimum five-year period required under the PCMLTFA?",
            "options": [
                "Yes — a retention policy is documented and enforced",
                "Partial — records are kept but the five-year period is not formally managed",
                "No — records are not systematically retained",
            ],
        },
        {
            "text": "Can your entity produce records requested by FINTRAC within 30 days?",
            "options": [
                "Yes — records are organised and retrievable on request",
                "Probably — but retrieval is manual and may take time",
                "No — we do not have a systematic records management process",
            ],
        },
        {
            "text": "Are records kept in a format acceptable to FINTRAC (electronic or paper, with an audit trail)?",
            "options": [
                "Yes — records are in an acceptable format with audit trail",
                "Partial — format is inconsistent",
                "No",
                "Not sure",
            ],
        },
        {
            "text": "Does your entity retain all required record types for your sector (e.g. KYC records, transaction records, business relationship records, training records)?",
            "options": [
                "Yes — all required record categories are retained",
                "Partial — some categories are retained but not all",
                "No",
                "Not sure which records are required for our sector",
            ],
        },
    ],

    # ── Ministerial Directives ──
    "dir": [
        {
            "text": "Is your entity aware that Ministerial Directives impose enhanced measures and transaction restrictions for clients/transactions linked to designated foreign jurisdictions or entities?",
            "options": [
                "Yes — we are fully aware and have implemented required measures",
                "Aware — but have not implemented specific measures",
                "Not aware",
            ],
        },
        {
            "text": "Does your entity screen new and existing clients against sanctions lists referenced in the Ministerial Directives?",
            "options": [
                "Yes — formal screening is conducted and documented",
                "Partial — informal review only",
                "No",
            ],
        },
        {
            "text": "Does your entity have documented procedures for what to do when a sanctions match is identified?",
            "options": [
                "Yes — escalation and reporting procedures are documented",
                "Partial — we know to escalate but procedures are not formalised",
                "No",
            ],
        },
        {
            "text": "Have your policies, training, and procedures been updated to reflect the most recent Ministerial Directive updates (all three directives updated in 2025)?",
            "new_2025": True,
            "hint": "Russia, Iran, and DPRK directives were all updated in 2025. Source: https://fintrac-canafe.canada.ca/obligations/directives-eng",
            "options": [
                "Yes — fully updated",
                "Partial — some updates made",
                "No — not yet updated",
                "Not sure when updates were last made",
            ],
        },
    ],
}


# ─── Sector-Specific Question Sets ──────────────────────────────────────────────

SECTOR_QUESTIONS = {

    # ── Financing / Leasing [NEW Apr 2025] ──
    "lease": [
        {
            "text": "Has your entity confirmed it meets the legal definition of a 'financing or leasing entity' under the amended PCMLTFA?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/lease-bail-eng",
            "options": [
                "Yes — confirmed with legal counsel",
                "We believe so based on our own reading",
                "Unsure — we have not sought legal confirmation",
            ],
        },
        {
            "text": "Has your entity identified which products and services trigger KYC obligations under the new leasing entity rules?",
            "hint": "Source: https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/client/lease-bail-eng",
            "options": [
                "Yes — trigger activities are mapped and procedures are in place",
                "Partial — some activities are identified but not all",
                "No",
            ],
        },
        {
            "text": "Have your staff been trained specifically on the April 1, 2025 financing/leasing entity obligations?",
            "options": [
                "Yes — training completed before or shortly after April 1, 2025",
                "Training is planned but not yet completed",
                "No",
            ],
        },
        {
            "text": "Does your risk assessment reflect the ML/TF risks specific to your financing and leasing activities?",
            "hint": "FINTRAC has not yet published sector-specific ML/TF indicators for financing/leasing entities. Use FINTRAC's general risk assessment guidance and your own business knowledge to identify applicable risks. Source: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng",
            "options": [
                "Yes — sector-specific risks are explicitly identified in the risk assessment",
                "Partial — generic risks only",
                "No",
            ],
        },
    ],

    # ── Cheque Cashers [NEW Apr 2025] ──
    "cheque": [
        {
            "text": "Has your entity confirmed it meets the definition of a 'cheque casher' under the amended PCMLTFA?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/cheque-eng",
            "options": [
                "Yes — confirmed",
                "We believe so based on our own reading",
                "Unsure",
            ],
        },
        {
            "text": "Has your entity registered as a Money Services Business (MSB) with FINTRAC as required by the 2025 regulations?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/cheque-eng",
            "options": [
                "Yes — registered",
                "Registration in progress",
                "No — not yet registered",
            ],
        },
        {
            "text": "Does your entity have documented procedures to identify and report listed person or entity property?",
            "options": [
                "Yes — LPEPR procedures are in place",
                "Partial — aware of the requirement but not formalised",
                "No",
            ],
        },
        {
            "text": "Does your entity have a documented client identification procedure for cheque cashing transactions that trigger KYC requirements?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/cheque-eng",
            "options": [
                "Yes — documented and applied",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have documented procedures for identifying and reporting Suspicious Transactions (STRs) arising from cheque cashing activities?",
            "hint": "STR obligations apply to all reporting entity sectors including cheque cashers. Source: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/str-dod/str-dod-eng",
            "options": [
                "Yes — STR procedures are in place and staff can identify red flags",
                "Partial — some awareness but procedures are not formalised",
                "No",
            ],
        },
        {
            "text": "Does your entity monitor for structuring — clients deliberately breaking transactions below KYC thresholds to avoid ID verification?",
            "options": [
                "Yes — staff are trained to identify and report structuring",
                "Partial — aware of the risk but no formal monitoring",
                "No",
            ],
        },
        {
            "text": "Have your staff been trained on the April 1, 2025 cheque casher obligations?",
            "options": [
                "Yes — training completed",
                "In progress",
                "No",
            ],
        },
    ],

    # ── Factors [NEW Apr 2025] ──
    "factor": [
        {
            "text": "Has your entity confirmed it meets the definition of a 'factor' under the amended PCMLTFA (i.e. purchasing accounts receivable at a discount)?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/fact-affact-eng",
            "options": [
                "Yes — confirmed",
                "We believe so",
                "Unsure",
            ],
        },
        {
            "text": "Does your entity have KYC procedures for both the client selling receivables and other parties to the transaction, where required?",
            "hint": "Source: https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/client/fact-affect-eng",
            "options": [
                "Yes — procedures address all required parties",
                "Partial — only one party is verified",
                "No",
            ],
        },
        {
            "text": "Has your risk assessment been updated to reflect ML/TF risks specific to your factoring activities?",
            "hint": "Use FINTRAC's general risk assessment guidance before sector-specific ML/TF indicators for factors is published. Source: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng",
            "options": [
                "Yes — sector-specific factoring risks are identified in the risk assessment",
                "Partial — generic risks only",
                "No",
            ],
        },
        {
            "text": "Have staff been trained on the April 1, 2025 factor obligations, including how to identify and report suspicious transactions (and other applicable transactions)?",
            "options": [
                "Yes — training completed",
                "In progress",
                "No",
            ],
        },
    ],

    # ── Private ABM Acquirers [NEW Oct 2025] ──
    "abm": [
        {
            "text": "Has your entity registered as a Money Services Business (MSB) with FINTRAC as required by the October 2025 regulations?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/abm-gap-eng",
            "options": [
                "Yes — registered",
                "Registration in progress",
                "No — not yet registered",
            ],
        },
        {
            "text": "Has your entity implemented client identification procedures for any person or entity that you provide acquirer services in relation to private ABMs?",
            "options": [
                "Yes — procedures are in place",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have processes to detect and report unusual cash patterns at individual ABM locations?",
            "hint": "Structuring at ABMs is a known ML typology.",
            "options": [
                "Yes — monitoring is in place and staff/systems are configured to flag this",
                "Partial — no automated monitoring but manual review occurs",
                "No",
            ],
        },
        {
            "text": "Does your entity maintain the records required for ABM acquirer activities (transaction records, client identification records) for the five-year retention period?",
            "options": [
                "Yes — records are maintained for five years",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Have staff or management been trained on the October 2025 obligations specific to private ABM acquirers?",
            "options": [
                "Yes — training completed",
                "In progress",
                "No",
            ],
        },
    ],

    # ── Title Insurers [NEW Oct 2025] ──
    "title": [
        {
            "text": "Has your entity reviewed its obligations as a newly designated reporting entity and mapped which transactions trigger KYC, record-keeping, and reporting requirements?",
            "hint": "Source: https://fintrac-canafe.canada.ca/re-ed/title-titre-eng",
            "options": [
                "Yes — fully mapped with procedures in place",
                "Partially mapped",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures for verifying the identity of parties to real estate transactions for which you provide title insurance?",
            "hint": "Source: https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/client/title-titre-eng",
            "options": [
                "Yes — verified procedures are in place",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures to flag and report suspicious patterns in title insurance transactions?",
            "hint": "Refer to FINTRAC's real estate ML/TF indicators as a starting reference before sector-specific ML/TF indicators for title insurers is published: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/real_mltf-eng",
            "options": [
                "Yes — ML/TF indicators for title insurance are incorporated into STR procedures",
                "Partial — generic STR procedures exist but not title-specific indicators",
                "No",
            ],
        },
        {
            "text": "Has your entity assessed the ML/TF risks specific to your title insurance activities?",
            "hint": "Use FINTRAC's general risk assessment guidance before sector-specific ML/TF indicators for title insurers is published: https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng",
            "options": [
                "Yes — risk assessment addresses title insurance-specific risks",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Have staff been trained on the October 2025 title insurer obligations?",
            "options": [
                "Yes — training completed",
                "In progress",
                "No",
            ],
        },
    ],

    # ── Mortgage Entities ──
    "mort": [
        {
            "text": "Does your entity verify the identity of all relevant parties to a mortgage transaction (borrower, guarantor, and where applicable, the third party directing the transaction)?",
            "options": [
                "Yes — all parties are verified before the transaction is completed",
                "Partial — not all parties are consistently verified",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures to detect and report suspicious mortgage transactions (e.g. straw buyers, unexplained large down payments, rapid property flipping, misrepresented income)?",
            "options": [
                "Yes — sector-specific ML indicators are incorporated into STR procedures",
                "Partial — generic STR indicators only",
                "No",
            ],
        },
        {
            "text": "Does your entity verify the source of funds for down payments where they are unusually large or come from non-standard sources?",
            "options": [
                "Yes — source of funds procedures are documented and applied",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity monitor mortgage referral relationships for AML risk (e.g. brokers who consistently refer high-risk clients)?",
            "options": [
                "Yes",
                "Partial",
                "No",
                "Not applicable (we do not use referral brokers)",
            ],
        },
    ],

    # ── Real Estate ──
    "re": [
        {
            "text": "Does your entity have documented procedures for receiving, reporting, and recording large cash transactions of $10,000 or more in connection with real estate transactions?",
            "hint": "Under current PCMLTFA obligations, real estate brokers/sales representatives/developers must submit an LCTR within 15 calendar days of receiving $10,000+ in cash (single or aggregated within 24 hours), keep a large cash transaction record, and take reasonable measures to determine if a third party is involved. Note: Bill C-2 proposes a future prohibition on accepting such cash payments, but this has not yet passed into law. Source: https://fintrac-canafe.canada.ca/re-ed/real-eng",
            "options": [
                "Yes — policy is in place and staff are trained on the prohibition",
                "Partial — aware of the requirement but no formal procedure",
                "No — not aware of this prohibition",
            ],
        },
        {
            "text": "Does your entity conduct KYC on both the buyer and seller in a transaction at the required trigger points?",
            "options": [
                "Yes — both buyer and seller are verified",
                "Partial — only one side of the transaction is verified",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures for identifying and reporting suspicious real estate transactions (e.g. all-cash purchases, nominee buyers, rapid flips, offshore financing)?",
            "options": [
                "Yes — sector-specific ML indicators are incorporated",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity screen all parties to a transaction for PEP/HIO status and sanctions exposure?",
            "options": [
                "Yes — all transaction parties are screened",
                "Partial — screening is not applied to all parties",
                "No",
            ],
        },
    ],

    # ── Financial Entities (banks, credit unions) ──
    "fin": [
        {
            "text": "Does your entity have a documented correspondent banking policy with enhanced due diligence procedures for respondent institutions?",
            "options": [
                "Yes — correspondent banking procedures are documented",
                "Partial",
                "No",
                "Not applicable (no correspondent banking relationships)",
            ],
        },
        {
            "text": "Does your entity's transaction monitoring system detect structuring (deliberately breaking transactions to avoid the $10,000 reporting threshold)?",
            "options": [
                "Yes — structuring detection is built into transaction monitoring",
                "Partial — manual monitoring only",
                "No",
            ],
        },
        {
            "text": "Does your entity's ongoing monitoring program flag dormant accounts that suddenly become active with large or unusual transaction volumes?",
            "options": [
                "Yes — this is a monitored scenario",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have documented procedures for de-risking decisions (terminating customer relationships for AML risk) that comply with regulatory expectations?",
            "options": [
                "Yes — de-risking procedures are documented and reviewed for appropriateness",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity keep its ML/TF typologies and red-flag indicators current, reviewing them as part of your ongoing compliance program maintenance and effectiveness review cycle?",
            "hint": "FINTRAC publishes sector-specific ML/TF indicators for financial entities: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/fin_mltf-eng",
            "options": [
                "Yes — typologies are reviewed and updated as part of the compliance program cycle",
                "Partial — ad hoc updates only",
                "No",
            ],
        },
    ],

    # ── MSBs ──
    "msb": [
        {
            "text": "Is your entity registered with FINTRAC as an MSB or Foreign MSB, and is the registration current?",
            "options": [
                "Yes — registered and registration is current",
                "Registered but may be overdue for update",
                "No — not registered",
            ],
        },
        {
            "text": "Does your entity comply with virtual currency transaction reporting and record-keeping obligations (for crypto services)?",
            "options": [
                "Yes — virtual currency procedures are fully in place",
                "Partial",
                "No",
                "Not applicable (no cryptocurrency services)",
            ],
        },
        {
            "text": "Does your entity comply with the Travel Rule for EFTs and virtual currency transfers?",
            "options": [
                "Yes — originator and beneficiary information is transmitted as required",
                "Partial",
                "No",
                "Not applicable",
            ],
        },
        {
            "text": "Does your entity screen all remittance corridors for high-risk jurisdictions, particularly those subject to Ministerial Directives?",
            "options": [
                "Yes — corridor risk is assessed and high-risk corridors have enhanced procedures",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity monitor the eligibility of agents or mandataries for AML compliance where applicable?",
            "options": [
                "Yes — agent monitoring procedures are in place",
                "Partial",
                "No",
                "Not applicable (no agents or mandataries)",
            ],
        },
    ],

    # ── Securities Dealers ──
    "sec": [
        {
            "text": "Does your entity have procedures to verify beneficial ownership of accounts held by corporations or other legal entities?",
            "options": [
                "Yes — beneficial ownership procedures are documented",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity screen for PEP/HIO status for all clients who open accounts?",
            "options": [
                "Yes — PEP/HIO screening at onboarding and ongoing",
                "Partial — onboarding only",
                "No",
            ],
        },
        {
            "text": "Does your entity have ML/TF indicators specific to securities (e.g. wash trading, pump-and-dump schemes, unusual third-party fund sources for securities purchases)?",
            "options": [
                "Yes — sector-specific indicators are in STR procedures",
                "Partial — generic indicators only",
                "No",
            ],
        },
    ],

    # ── Life Insurance ──
    "li": [
        {
            "text": "Does your entity verify the identity of both the policyholder and the beneficial owner (where different) at policy issuance?",
            "options": [
                "Yes — both parties are verified where applicable",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures to identify and report suspicious life insurance transactions?",
            "hint": "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/li_mltf-eng)",
            "options": [
                "Yes — life insurance-specific ML indicators are incorporated",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity screen for PEP/HIO status and apply enhanced due diligence to PEP/HIO clients who hold or apply for policies?",
            "options": [
                "Yes — PEP/HIO-specific life insurance procedures are in place",
                "Partial",
                "No",
            ],
        },
    ],

    # ── Accountants ──
    "acct": [
        {
            "text": "Does your entity have documented procedures to identify when an accounting engagement triggers FINTRAC KYC obligations (i.e. specific listed activities under the PCMLTFA)?",
            "hint": "https://fintrac-canafe.canada.ca/guidance-directives/client-clientele/client/acc-eng",
            "options": [
                "Yes — trigger activities are mapped and staff are trained",
                "Partial — awareness exists but mapping is incomplete",
                "No",
            ],
        },
        {
            "text": "Does your entity have a process to identify and report suspicious transactions arising from client engagements?",
            "options": [
                "Yes — STR procedures are in place for applicable engagements",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have sector-specific ML/TF indicators (e.g. clients asking to hold funds outside normal business purposes, unexplained offshore structures)?",
            "hint": "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/accts_mltf-eng",
            "options": [
                "Yes — accounting sector indicators are incorporated",
                "Partial — generic only",
                "No",
            ],
        },
    ],

    # ── DPMS ──
    "dpms": [
        {
            "text": "Does your entity have documented procedures for the $10,000 cash transaction reporting threshold in precious metals and stones transactions?",
            "options": [
                "Yes — LCTR procedures are in place",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity verify client identity for transactions at or above applicable thresholds?",
            "options": [
                "Yes — KYC procedures are consistently applied",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have ML/TF indicators specific to precious metals and stones (e.g. unusual interest in anonymity, purchases structured below $10,000, mixed payment methods)?",
            "options": [
                "Yes — sector-specific indicators are in place",
                "Partial",
                "No",
            ],
        },
    ],

    # ── Casinos ──
    "casino": [
        {
            "text": "Does your entity have a documented Player Information Record (PIR) or equivalent procedure for large cash transactions?",
            "options": [
                "Yes — PIR procedures are documented and consistently applied",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Does your entity have procedures for monitoring large cash-outs, chip redemptions, and unusual patterns of play?",
            "options": [
                "Yes — monitoring procedures are in place",
                "Partial",
                "No",
            ],
        },
        {
            "text": "Are casino staff trained on sector-specific ML/TF indicators?",
            "hint": "https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/casinos_mltf-eng",
            "options": [
                "Yes — casino-specific training is in place",
                "Partial",
                "No",
            ],
        },
    ],

    # ── Other ──
    "other": [],
}
