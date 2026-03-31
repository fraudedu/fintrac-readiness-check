# FINTRAC Readiness Assessment Tool

**A free, self-serve compliance gap assessment tool for Canadian businesses subject to the *Proceeds of Crime (Money Laundering) and Terrorist Financing Act* (PCMLTFA).**

🔗 [**Live Tool →**](https://fintrac-readiness.streamlit.app/)  |  🎯 [**View Demo Report →**](https://fintrac-readiness.streamlit.app/?demo=true)

\---

## What It Does

Canada's AML regulatory landscape expanded significantly in 2025, bringing thousands of businesses under FINTRAC's compliance obligations for the first time — including financing and leasing entities, factors, cheque cashers, private ABM acquirers, and title insurers.

This tool helps any reporting entity under the PCMLTFA understand where their compliance program stands across FINTRAC's five mandatory pillars:

1. Compliance Officer
2. Written Policies \& Procedures
3. Risk Assessment
4. Training Program
5. Effectiveness Review

Plus sector-specific checks covering KYC, transaction reporting, record-keeping, and Ministerial Directives — tailored to 14 regulated entity types.

**Output:** A scored RAG report (Red / Amber / Green) across every compliance area, a prioritised list of gaps, and a 30/60/90-day action plan. Downloadable as PDF.

\---

## Who It's For

* **Newly obligated businesses** (2025) that need to understand what a FINTRAC-compliant program actually requires
* **Established reporting entities** preparing for a FINTRAC examination
* **Compliance consultants and legal advisors** conducting preliminary assessments with clients
* **Credit unions, MSBs, mortgage brokers**, and other mid-market financial services operators

\---

## Covered Sectors

|New in 2025|Established|
|-|-|
|Financing / Leasing Entities|Financial Entities (banks, credit unions)|
|Factors|Money Services Businesses (MSBs)|
|Cheque Cashers|Mortgage Administrators, Brokers \& Lenders|
|Private ABM Acquirers|Real Estate Brokers / Developers|
|Title Insurers|Securities Dealers|
||Life Insurance Companies, Brokers \& Agents|
||Accountants|
||Dealers in Precious Metals \& Stones|
||Casinos|

\---

## Quick Start

```bash
git clone https://github.com/YOUR\_USERNAME/fintrac-readiness-tool.git
cd fintrac-readiness-tool
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. Click **View Demo** to see a pre-filled report without completing the assessment.

\---

## Project Structure

```
├── app.py            # Streamlit app — routing, UI, scoring engine
├── questions.py      # All question banks, sector definitions, score mapping
├── pdf\_export.py     # PDF report generator (fpdf2)
├── demo.py           # Pre-filled demo scenario (newly-obligated leasing company)
├── report.py         # HTML report helper
└── requirements.txt  # streamlit, fpdf2
```

\---

## Regulatory Basis

All questions are sourced directly from FINTRAC's published guidance at [fintrac-canafe.canada.ca](https://fintrac-canafe.canada.ca), including:

* [Compliance Program Requirements](https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/Guide4/4-eng)
* [Risk Assessment Guidance](https://fintrac-canafe.canada.ca/guidance-directives/compliance-conformite/rba/rba-eng)
* [FINTRAC Assessment Manual](https://fintrac-canafe.canada.ca/guidance-directives/exam-examen/cam/cams-eng)
* [Ministerial Directives and Transaction Restrictions](https://fintrac-canafe.canada.ca/obligations/directives-eng)
* Sector-specific guidance pages for all 14 covered sectors

The question bank reflects regulatory requirements as of **March 2026**, including the April 2025 and October 2025 expansions to newly-obligated entity types.

\---

## Keeping It Current

FINTRAC updates its guidance frequently. To update the tool after regulatory changes:

1. Edit the relevant questions in `questions.py`
2. `git push` — Streamlit Cloud redeploys automatically within \~60 seconds

The question bank is intentionally separated from the app logic to make maintenance straightforward.

\---

## Disclaimer

This tool provides a **preliminary self-assessment only**. It does not constitute legal or compliance advice and does not certify compliance with the PCMLTFA. Results reflect the answers provided and may not capture all obligations applicable to your specific circumstances. Consult a qualified AML/ATF compliance professional or legal counsel before relying on these results.

\---

## About

Built by [Howard Wong](https://www.linkedin.com/in/howardchwong/) — fintech and compliance professional based in Calgary, Alberta.  
Background: Ex-Head of CDD, technology and operational leadership, financial technology consulting, and business and data analysis.

*© Asset Tech*


