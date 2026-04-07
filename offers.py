"""
offers.py — Gumroad product mapping and offer card renderer.

To activate a product: replace the placeholder URL with your live Gumroad link.
To deactivate a product (not yet listed): set the url to None — the card will show
a "Coming soon" state instead of a purchase button.
"""

# ─── Product catalogue ────────────────────────────────────────────────────────
# Keys match SECTORS["key"] values in questions.py
# Set url to None until the product is live on Gumroad

PRODUCTS = {
    "lease": {
        "title": "FINTRAC Compliance Guide for Financing & Leasing Entities",
        "tagline": "Pillar-by-pillar instructions to build required element of your compliance program — from compliance officer appointment to effectiveness review unique to your sector.",
        "includes": [
            "Pillar-by-pillar build instructions with questions to guide your writing",
            "Reporting trigger reference for your specific entity type",
            "Complete build checklist",
            "Relevant FINTRAC source links verified March 2026",
        ],
        "price": "CAD $139",
        "url": None,  # Replace with: "https://..."
    },
    "factor": {
        "title": "FINTRAC Compliance Guide for Factors",
        "tagline": "Pillar-by-pillar instructions to build required element of your compliance program — from compliance officer appointment to effectiveness review unique to your sector.",
        "includes": [
            "Pillar-by-pillar build instructions with questions to guide your writing",
            "Reporting trigger reference for your specific entity type",
            "Complete build checklist",
            "Relevant FINTRAC source links verified March 2026",
        ],
        "price": "CAD $139",
        "url": None,  # Replace with: "https://..."
    },
    "cheque": {
        "title": "FINTRAC Compliance Guide for Cheque Cashers",
        "tagline": "Pillar-by-pillar instructions to build required element of your compliance program — from compliance officer appointment to effectiveness review unique to your sector.",
        "includes": [
            "Pillar-by-pillar build instructions with questions to guide your writing",
            "Reporting trigger reference for your specific entity type",
            "Complete build checklist",
            "Relevant FINTRAC source links verified March 2026",
        ],
        "price": "CAD $139",
        "url": None,  # Replace with: "https://..."
    },
    "abm": {
        "title": "FINTRAC Compliance Guide for Private ABM Acquirers",
        "tagline": "Pillar-by-pillar instructions to build required element of your compliance program — from compliance officer appointment to effectiveness review unique to your sector.",
        "includes": [
            "Pillar-by-pillar build instructions with questions to guide your writing",
            "Reporting trigger reference for your specific entity type",
            "Complete build checklist",
            "Relevant FINTRAC source links verified March 2026",
        ],
        "price": "CAD $139",
        "url": None,  # Replace with: "https://..."
    },
    "title": {
        "title": "FINTRAC Compliance Guide for Title Insurers",
        "tagline": "Pillar-by-pillar instructions to build required element of your compliance program — from compliance officer appointment to effectiveness review unique to your sector.",
        "includes": [
            "Pillar-by-pillar build instructions with questions to guide your writing",
            "Reporting trigger reference for your specific entity type",
            "Complete build checklist",
            "Relevant FINTRAC source links verified March 2026",
        ],
        "price": "CAD $139",
        "url": None,  # Replace with: "https://..."
    },
}

# Sectors with no product yet — show a generic resource card instead
NO_PRODUCT_SECTORS = {"fin", "msb", "mort", "re", "sec", "li", "acct", "dpms", "casino", "other"}


# ─── Renderer ────────────────────────────────────────────────────────────────
def render_offer_card(sector_key: str):
    """
    Call this at the bottom of the report page, after the disclaimer.
    Renders a contextual product offer card for the entity's sector.
    """
    import streamlit as st

    product = PRODUCTS.get(sector_key)

    # ── Sectors with no product yet ──────────────────────────────────────────
    if sector_key in NO_PRODUCT_SECTORS or product is None:
        st.markdown("---")
        st.markdown("### 📚 Need Help Building Your Program?")
        st.info(
            "Compliance guides for your sector are in development. "
            "Follow Asset Tech founder on LinkedIn for updates."
        )
        return

    # ── Newly-obligated sectors with a product ────────────────────────────────
    st.markdown("---")
    st.markdown("""
<div style="background:#f0f7ff; border:1px solid #1565c0; border-radius:8px;
            padding:20px 24px; margin-top:8px;">
    <div style="font-size:0.75rem; font-weight:700; color:#1565c0;
                letter-spacing:0.08em; margin-bottom:8px;">
        NEXT STEP FOR YOUR BUSINESS
    </div>
""", unsafe_allow_html=True)

    st.markdown(f"#### 📘 {product['title']}")
    st.markdown(f"*{product['tagline']}*")
    st.markdown("**What's inside:**")
    for item in product["includes"]:
        st.markdown(f"- {item}")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"**{product['price']}**")

    with col2:
        if product["url"]:
            st.markdown(
                f'<a href="{product["url"]}" target="_blank">'
                f'<button style="background:#1565c0; color:white; border:none; '
                f'padding:10px 24px; border-radius:6px; font-size:1rem; '
                f'cursor:pointer; width:100%;">Get the Guide →</button>'
                f'</a>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="background:#e3e3e3; color:#666; border:none; '
                'padding:10px 24px; border-radius:6px; font-size:0.9rem; '
                'text-align:center;">Coming Soon</div>',
                unsafe_allow_html=True,
            )

    st.markdown("""
<div style="font-size:0.75rem; color:#777; margin-top:12px;">
    Educational guide only. Does not constitute legal advice.
    Consult a qualified AML professional for formal compliance review.
</div>
</div>
""", unsafe_allow_html=True)
