"""
Minimalist Routine Diagnostic Engine (student prototype)
KPI Detective | MBA561B Digital and Social Media Analytics | CIA 1

A Streamlit prototype that converts high-intent PDP hesitators into a safe,
personalised 3-step regimen while logging GA4-style micro-conversion events.
Styled after the structure of beminimalist.co (announcement bar, header with
cart, product cards with badge / concern line / price / size / add to cart,
brand-pillar strip). It is an academic simulation, not an official Minimalist
tool, and uses no logos or images.

Run:  pip install streamlit
      streamlit run app.py

Prices tagged "Site price" were read from the beminimalist.co homepage
(smallest size shown). "Indicative" prices are estimates: verify on the site.
"""

from datetime import datetime

import streamlit as st

# ----------------------------------------------------------------------------
# PAGE CONFIG + STYLING
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Routine Diagnostic | Minimalist (student prototype)",
    page_icon="◼",
    layout="wide",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"], .stApp {
        font-family: -apple-system, "Segoe UI", "Helvetica Neue", Helvetica, Arial, sans-serif;
        background-color: #FFFFFF;
        color: #111111;
    }
    .block-container { padding-top: 0 !important; max-width: 1240px; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    /* announcement bar */
    .announce {
        background: #111111; color: #FFFFFF; text-align: center;
        font-size: 0.82rem; letter-spacing: 0.04em; padding: 0.55rem 1rem;
        margin: 0 -5rem 0 -5rem;
    }
    /* header */
    .site-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 0 0.8rem 0; border-bottom: 1px solid #E6E6E6; margin-bottom: 0.4rem;
    }
    .wordmark { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.03em; }
    .wordmark small { font-size: 0.7rem; font-weight: 500; color: #777777; letter-spacing: 0.02em; margin-left: 0.5rem; }
    .cart-pill {
        border: 1px solid #111111; border-radius: 999px; padding: 0.35rem 0.9rem;
        font-size: 0.9rem; font-weight: 600;
    }
    .nav { display: flex; gap: 1.6rem; font-size: 0.88rem; color: #333333; padding: 0.55rem 0 0.9rem 0; border-bottom: 1px solid #F0F0F0; margin-bottom: 1.4rem; }
    .nav span.active { font-weight: 700; border-bottom: 2px solid #111111; padding-bottom: 2px; }

    /* hero */
    .hero { background: #F4F4F2; border-radius: 12px; padding: 1.6rem 1.8rem; margin-bottom: 1.4rem; }
    .hero h1 { font-size: 2rem; font-weight: 700; letter-spacing: -0.03em; margin: 0 0 0.3rem 0; color: #111111; }
    .hero p { margin: 0; color: #555555; font-size: 0.98rem; }

    .section-title { font-size: 1.25rem; font-weight: 700; letter-spacing: -0.02em; margin: 0.4rem 0 0.7rem 0; }

    /* product card */
    .pcard {
        border: 1px solid #E6E6E6; border-radius: 12px; padding: 1rem 1.2rem;
        margin-bottom: 0.9rem; background: #FFFFFF;
    }
    .pcard .top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; }
    .step-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; color: #777777; }
    .badge { background: #111111; color: #FFFFFF; font-size: 0.68rem; font-weight: 600; padding: 0.15rem 0.55rem; border-radius: 999px; letter-spacing: 0.04em; }
    .badge-light { background: #F0F0EE; color: #111111; font-size: 0.68rem; font-weight: 600; padding: 0.15rem 0.55rem; border-radius: 999px; }
    .pname { font-size: 1.12rem; font-weight: 700; letter-spacing: -0.01em; margin: 0.1rem 0 0.15rem 0; }
    .pline { color: #555555; font-size: 0.88rem; margin-bottom: 0.5rem; }
    .price-row { display: flex; align-items: baseline; gap: 0.6rem; margin-top: 0.55rem; }
    .price { font-size: 1.15rem; font-weight: 700; }
    .size { font-size: 0.8rem; color: #666666; border: 1px solid #DDDDDD; border-radius: 6px; padding: 0.05rem 0.5rem; }
    .src { font-size: 0.72rem; color: #888888; }
    .safety { display: inline-block; font-size: 0.74rem; font-weight: 600; border: 1px solid #111111; border-radius: 6px; padding: 0.08rem 0.5rem; margin: 0.15rem 0 0.4rem 0; }
    .muted { color: #555555; font-size: 0.85rem; line-height: 1.45; }
    .pill { display: inline-block; border: 1px solid #111111; border-radius: 999px; padding: 0.08rem 0.65rem; font-size: 0.76rem; margin-right: 0.4rem; }
    .pill-solid { display: inline-block; background: #111111; color: #FFFFFF; border-radius: 999px; padding: 0.08rem 0.65rem; font-size: 0.76rem; margin-right: 0.4rem; }

    .total-card { background: #111111; color: #FFFFFF; border-radius: 12px; padding: 1.1rem 1.3rem; margin-bottom: 0.9rem; }
    .total-card .lbl { font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase; color: #BBBBBB; }
    .total-card .amt { font-size: 1.9rem; font-weight: 700; }

    /* buttons: black, like the site's Add to cart */
    div.stButton > button {
        background-color: #111111; color: #FFFFFF; border: 1px solid #111111;
        border-radius: 8px; padding: 0.6rem 1.2rem; font-weight: 600; width: 100%;
    }
    div.stButton > button:hover { background-color: #FFFFFF; color: #111111; border: 1px solid #111111; }

    /* inputs */
    div[data-baseweb="select"] > div { border-radius: 8px; }

    /* sidebar */
    [data-testid="stSidebar"] { background-color: #F7F7F5; border-right: 1px solid #E6E6E6; }
    [data-testid="stSidebar"] * { color: #111111; }
    .event-row {
        border-left: 3px solid #111111; padding: 0.3rem 0.6rem; margin: 0.35rem 0;
        background: #FFFFFF; border-radius: 0 6px 6px 0;
        font-family: "SFMono-Regular", Consolas, "Courier New", monospace; font-size: 0.76rem;
    }

    /* pillars */
    .pillars { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.9rem; margin: 0.6rem 0 1rem 0; }
    .pillar { border: 1px solid #E6E6E6; border-radius: 12px; padding: 1rem 1.1rem; background: #FAFAF8; }
    .pillar b { display: block; font-size: 0.98rem; margin-bottom: 0.25rem; }
    .pillar span { font-size: 0.84rem; color: #555555; line-height: 1.4; }
    .exec { border: 1px solid #111111; border-radius: 12px; padding: 1.1rem 1.3rem; }
    .disclaimer { color: #888888; font-size: 0.78rem; margin-top: 0.8rem; text-align: center; }


    /* product image tile */
    .pimg { background: #F4F4F2; border-radius: 10px; height: 190px; display: flex; align-items: center; justify-content: center; margin-bottom: 0.7rem; overflow: hidden; }
    .pimg img { max-height: 176px; max-width: 90%; object-fit: contain; }
    .pimg svg { height: 172px; width: auto; }
        /* ---- force light widgets even if the viewer's Streamlit is in dark mode ---- */
    [data-testid="stWidgetLabel"] *, [data-testid="stWidgetLabel"] p { color: #111111 !important; }
    label[data-baseweb="checkbox"] p, [data-testid="stCheckbox"] p, [data-testid="stToggle"] p { color: #111111 !important; }
    [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"], [data-testid="stMetricValue"] * { color: #111111 !important; }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: #666666 !important; }
    div[data-baseweb="select"] > div { background: #FFFFFF !important; border: 1px solid #CFCFCF !important; border-radius: 8px; }
    div[data-baseweb="select"] * { color: #111111 !important; }
    div[data-baseweb="select"] svg { fill: #111111 !important; }
    div[data-baseweb="popover"] ul, ul[role="listbox"] { background: #FFFFFF !important; }
    li[role="option"] { color: #111111 !important; background: #FFFFFF !important; }
    li[role="option"]:hover { background: #F0F0EE !important; }
    div[data-baseweb="input"] > div { background: #FFFFFF !important; border: 1px solid #CFCFCF !important; border-radius: 8px; }
    div[data-baseweb="input"] input { color: #111111 !important; }
    [data-testid="stRadio"] label p { color: #111111 !important; }

    /* buttons: label colour must beat the generic sidebar text rule */
    div.stButton > button, div.stButton > button p { color: #FFFFFF !important; }
    div.stButton > button:hover, div.stButton > button:hover p { color: #111111 !important; }

    /* top navigation buttons (real page links) */
    div[class*="st-key-nav_"] div.stButton > button {
        background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important;
        border-radius: 0 !important; padding: 0.35rem 0 !important; font-weight: 500 !important;
        justify-content: flex-start !important; width: auto !important; box-shadow: none !important;
    }
    div[class*="st-key-nav_"] div.stButton > button, div[class*="st-key-nav_"] div.stButton > button p { color: #333333 !important; }
    div[class*="st-key-nav_"] div.stButton > button:hover { border-bottom: 2px solid #BBBBBB !important; background: transparent !important; }
    div[class*="st-key-nav_"] div.stButton > button:hover p { color: #111111 !important; }
    div.st-key-nav_cart div.stButton > button {
        border: 1px solid #111111 !important; border-radius: 999px !important; padding: 0.35rem 0.9rem !important;
        justify-content: center !important; font-weight: 600 !important; float: right;
    }
        </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# CATALOGUE (INR). tag: "site" = price seen on beminimalist.co homepage
# (smallest size shown); "est" = indicative estimate, verify on the site.
# ----------------------------------------------------------------------------
GENTLE_CLEANSER = {
    "name": "Gentle Non-Exfoliating Cleanser",
    "active": "Mild, sulphate-free surfactants (no strong actives)",
    "line": "Cleans without stripping, so your treatment step does the work",
    "price": 249, "size": "100 ml", "tag": "est", "badge": "Starter-safe",
}
ACTIVE_CLEANSER = {
    "name": "Salicylic Acid + LHA 2% Cleanser",
    "active": "2% Salicylic Acid + LHA (wash-off)",
    "line": "Deep-cleans pores and controls oil",
    "price": 269, "size": "100 ml", "tag": "site", "badge": "Best Seller",
}
MOISTURISER = {
    "name": "Vitamin B5 10% Moisturiser",
    "active": "10% Vitamin B5 (Panthenol)",
    "line": "Barrier support while your skin adjusts to an active",
    "price": 314, "size": "50 g", "tag": "site", "badge": "Best Seller",
}
SUNSCREEN = {
    "name": "SPF 50 Sunscreen",
    "active": "Broad-spectrum SPF 50",
    "line": "Daily protection that locks in tone and anti-ageing results",
    "price": 224, "size": "from", "tag": "site", "badge": "Best Seller",
}


def _t(name, active, price, size, tag, badge, line, risk, frequency, purge, layering, strong=False):
    return {
        "name": name, "active": active, "price": price, "size": size, "tag": tag,
        "badge": badge, "line": line, "risk": risk, "frequency": frequency,
        "purge": purge, "layering": layering, "strong": strong,
    }


TREATMENTS = {
    "Acne & Blemishes": {
        "gentle": _t("Azelaic Acid 10% Serum", "10% Azelaic Acid", 399, "30 ml", "est", "Gentle start",
                     "Helps clear blemishes and calm redness", "Low",
                     "PM, 3 nights a week, then daily after 2 weeks",
                     "Mild tingling is possible. Genuine purging is unlikely at this strength.",
                     "Apply on dry skin, then moisturiser. Do not combine with exfoliating acids."),
        "standard": _t("Salicylic Acid 2% Face Serum", "2% Salicylic Acid (BHA)", 249, "10 ml", "site", "Best Seller",
                       "Clears blemishes, whiteheads and blackheads", "Moderate",
                       "PM, alternate nights for 2 weeks, then nightly if comfortable",
                       "Small breakouts in your usual acne zones for 2 to 6 weeks can be purging. New areas or anything beyond 8 weeks means stop and review.",
                       "Use before moisturiser. Do not add a retinoid or Vitamin C on the same night.", True),
        "advanced": _t("Salicylic Acid 2% Face Serum", "2% Salicylic Acid (BHA)", 249, "10 ml", "site", "Best Seller",
                       "Clears blemishes, whiteheads and blackheads", "Moderate",
                       "PM nightly, with one rest night a week",
                       "Purging, if any, usually settles within 4 to 6 weeks.",
                       "Keep other exfoliants out of the routine. Niacinamide can be added on alternate mornings.", True),
    },
    "Pigmentation & Dark Spots": {
        "gentle": _t("Alpha Arbutin 2% Face Serum", "2% Alpha Arbutin", 349, "30 ml", "est", "Gentle start",
                     "Fades dark spots and marks gradually", "Low", "AM and PM",
                     "Purging is not expected. Results typically need 8 to 12 weeks.",
                     "Apply to clean skin, then moisturiser, then sunscreen in the morning."),
        "standard": _t("Vitamin C 10% Face Serum", "10% Vitamin C", 299, "10 ml", "site", "Best Seller",
                       "Brightens skin and fades dark spots", "Moderate", "AM, then sunscreen",
                       "Purging is uncommon. Stinging means reduce to alternate days.",
                       "Apply before moisturiser and sunscreen. Keep retinoids and strong acids to the evening."),
        "advanced": _t("Vitamin C 20% Face Serum", "20% Vitamin C", 499, "30 ml", "est", "Advanced",
                       "Stronger brightening for experienced users", "Moderate to High", "AM only, then sunscreen",
                       "Redness or stinging can occur. Drop to alternate days if so.",
                       "Morning only, never in the same routine as an exfoliating acid.", True),
    },
    "Fine Lines & Ageing": {
        "gentle": _t("Copper Peptide + PDRN 1.25% Face Serum", "1.25% Copper Peptide + PDRN", 629, "10 ml", "site", "New Launch",
                     "Supports firmness and visible repair, no retinoid", "Low", "AM and PM",
                     "Not expected.",
                     "Apply on damp skin, then moisturiser. Generally safe with most products."),
        "standard": _t("Retinol 0.3% Face Serum", "0.3% Retinol", 349, "30 ml", "est", "Intermediate",
                       "Targets fine lines and uneven texture", "Moderate",
                       "PM, twice a week for 2 weeks, then every other night",
                       "Dryness, flaking and a breakout phase of 2 to 6 weeks are common.",
                       "Night only. Buffer with moisturiser if skin feels tight. No acids on retinol nights. Sunscreen daily.", True),
        "advanced": _t("Retinol 0.6% Face Serum", "0.6% Retinol", 399, "30 ml", "est", "Advanced",
                       "Stronger anti-ageing for experienced users", "High",
                       "PM, every other night, building to nightly only if tolerated",
                       "Expect some peeling or breakouts for up to 6 to 8 weeks.",
                       "Night only. No exfoliating acids or Vitamin C in the same routine. Sunscreen is essential.", True),
    },
    "Dullness & Uneven Tone": {
        "gentle": _t("Niacinamide 10% Face Serum", "10% Niacinamide", 249, "10 ml", "site", "Best Seller",
                     "Evens tone and refines texture", "Low to Moderate",
                     "Start once a day (AM) for a week, then add PM if comfortable",
                     "Rare. Slight flushing means drop to once a day.",
                     "Apply to clean skin before moisturiser. Safe alongside most routines."),
        "standard": _t("Niacinamide 10% Face Serum", "10% Niacinamide", 249, "10 ml", "site", "Best Seller",
                       "Evens tone and refines texture", "Low to Moderate",
                       "AM and PM",
                       "Rare. Slight flushing means drop to once a day.",
                       "Apply to clean skin before moisturiser. Safe alongside most routines."),
        "advanced": _t("Lactic Acid 5% Face Serum", "5% Lactic Acid (AHA)", 349, "30 ml", "est", "Advanced",
                       "Gentle exfoliation for glow and smoother texture", "Moderate",
                       "PM, twice a week, building to alternate nights",
                       "Short-term texture or small breakouts can occur for 2 to 4 weeks.",
                       "Night only. Do not combine with retinoids or Vitamin C on the same night. Sunscreen daily.", True),
    },
    "Large Pores & Excess Oil": {
        "gentle": _t("Niacinamide 10% Face Serum", "10% Niacinamide", 249, "10 ml", "site", "Best Seller",
                     "Controls oil and visibly refines pores", "Low to Moderate",
                     "Start once a day for a week, then AM and PM",
                     "Rare. Slight flushing or tightness means reduce frequency.",
                     "Apply before moisturiser. Avoid pairing with Vitamin C in the same step."),
        "standard": _t("Niacinamide 10% Face Serum", "10% Niacinamide", 249, "10 ml", "site", "Best Seller",
                       "Controls oil and visibly refines pores", "Low to Moderate",
                       "AM and PM",
                       "Rare. Slight flushing or tightness means reduce frequency.",
                       "Apply before moisturiser. Avoid pairing with Vitamin C in the same step."),
        "advanced": _t("Salicylic Acid 2% Face Serum", "2% Salicylic Acid (BHA)", 249, "10 ml", "site", "Best Seller",
                       "Unclogs pores and controls oil", "Moderate", "PM, alternate nights",
                       "Surface congestion may surface for 2 to 6 weeks.",
                       "Keep other exfoliants out of the routine. Moisturise after.", True),
    },
    "Dehydration & Tightness": {
        "gentle": _t("Hyaluronic Acid 2% + B5 Face Serum", "2% Hyaluronic Acid + Vitamin B5", 399, "30 ml", "est", "Hydration",
                     "Plumps and relieves tightness", "Low", "AM and PM on damp skin",
                     "Not expected.", "Apply on slightly damp skin and seal with moisturiser."),
    },
}
TREATMENTS["Dehydration & Tightness"]["standard"] = TREATMENTS["Dehydration & Tightness"]["gentle"]
TREATMENTS["Dehydration & Tightness"]["advanced"] = TREATMENTS["Dehydration & Tightness"]["gentle"]

SUN_PROTECT_CONCERNS = {"Pigmentation & Dark Spots", "Fine Lines & Ageing", "Dullness & Uneven Tone"}

FAQ = {
    "What is purging and is it normal?": (
        "Purging is a temporary increase in breakouts when an active speeds up cell turnover. "
        "It appears where you usually break out and fades within about 4 to 6 weeks. "
        "Breakouts in new areas, itching or swelling are irritation or allergy, not purging. Stop and consult a dermatologist."
    ),
    "Can I layer two serums together?": (
        "Keep one strong active per routine and pair it with a soothing or hydrating product. "
        "Do not combine retinoids, exfoliating acids and Vitamin C on the same night."
    ),
    "How do percentages differ, for example 10% vs 2%?": (
        "The percentage is the concentration of one ingredient, not a ranking of strength across ingredients. "
        "2% Salicylic Acid is a strong exfoliant. 10% Niacinamide is generally well tolerated. "
        "Compare within an ingredient and judge tolerance by your skin type and experience."
    ),
}

# ----------------------------------------------------------------------------
# SESSION STATE + GA4-STYLE EVENT LOGGING
# ----------------------------------------------------------------------------
if "events" not in st.session_state:
    st.session_state.events = []
if "regimen" not in st.session_state:
    st.session_state.regimen = None
if "cart_added" not in st.session_state:
    st.session_state.cart_added = False


def log_event(name, **params):
    """Append a GA4-style custom event to the session log."""
    st.session_state.events.append(
        {"event_name": name, "timestamp": datetime.now().strftime("%H:%M:%S"), "params": params}
    )


def count_events(name):
    return sum(1 for e in st.session_state.events if e["event_name"] == name)


# ----------------------------------------------------------------------------
# RECOMMENDATION ENGINE
# ----------------------------------------------------------------------------
def pick_tier(skin_type, experience):
    """Safety-first tier: sensitive skin and beginners always start gentle."""
    if skin_type == "Sensitive" or experience == "Beginner (never used actives)":
        return "gentle"
    if experience == "Intermediate (used 1 to 2 actives)":
        return "standard"
    return "advanced"


def pick_cleanser(skin_type, tier, treat):
    """Use the exfoliating cleanser only for oily/combination skin that is not
    already getting a strong active, to avoid stacking exfoliants."""
    if skin_type in ("Oily", "Combination") and tier != "gentle" and not treat["strong"]:
        return ACTIVE_CLEANSER
    return GENTLE_CLEANSER


def build_regimen(skin_type, concern, experience, budget):
    tier = pick_tier(skin_type, experience)
    treat = TREATMENTS[concern][tier]
    cleanse = pick_cleanser(skin_type, tier, treat)

    if concern in SUN_PROTECT_CONCERNS:
        protect = dict(SUNSCREEN)
        protect["step_title"] = "Protect"
        protect["why"] = "Actives that target tone and ageing raise sun sensitivity. Daily SPF protects results and prevents new pigmentation."
    else:
        protect = dict(MOISTURISER)
        protect["step_title"] = "Moisturise"
        protect["why"] = "A barrier-supporting moisturiser reduces dryness and irritation while your skin adjusts to the active."

    total = cleanse["price"] + treat["price"] + protect["price"]
    return {
        "tier": tier, "skin_type": skin_type, "concern": concern, "experience": experience,
        "budget": budget, "cleanse": cleanse, "treat": treat, "protect": protect,
        "total": total, "essential_total": cleanse["price"] + treat["price"],
    }


def on_generate():
    r = build_regimen(
        st.session_state["in_skin"], st.session_state["in_concern"],
        st.session_state["in_exp"], st.session_state["in_budget"],
    )
    st.session_state.regimen = r
    st.session_state.cart_added = False
    log_event("routine_quiz_complete", skin_type=r["skin_type"], concern=r["concern"],
              experience_tier=r["tier"], budget_inr=r["budget"])


def on_add_to_cart():
    r = st.session_state.regimen
    if r is None:
        return
    st.session_state.cart_added = True
    for step in ("cleanse", "treat", "protect"):
        name = r[step]["name"]
        st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1
    log_event("routine_add_to_cart", value_inr=r["total"], items=3, treat_active=r["treat"]["active"])


def on_faq_toggle(question):
    if st.session_state.get(f"faq_{question}"):
        log_event("ingredient_faq_expand", question=question)


# ----------------------------------------------------------------------------
# FLAT CATALOGUE, CART AND PAGE NAVIGATION (state + pure helpers)
# ----------------------------------------------------------------------------
PAGES = ["Shop", "Best Sellers", "Skin & Body Care", "Routine Diagnostic", "Track Order"]


def _build_catalogue():
    items = {}

    def add(p, category):
        if p["name"] not in items:
            q = dict(p)
            q["category"] = category
            items[p["name"]] = q

    add(ACTIVE_CLEANSER, "Cleanser")
    add(GENTLE_CLEANSER, "Cleanser")
    for tiers in TREATMENTS.values():
        for t in tiers.values():
            add(t, "Serum")
    add(MOISTURISER, "Moisturiser")
    add(SUNSCREEN, "Sunscreen")
    return items


CATALOGUE = _build_catalogue()

# Simulated orders for the Track Order page (demo data, not real orders).
ORDER_STEPS = ["Order placed", "Packed", "Shipped", "Out for delivery", "Delivered"]
RTO_STEPS = ["Order placed", "Packed", "Shipped", "Delivery attempt failed", "Return to origin initiated"]
ORDERS = {
    "MN-10021": {"status": "Delivered", "steps": ORDER_STEPS, "done": 5,
                 "items": ["Niacinamide 10% Face Serum", "Vitamin B5 10% Moisturiser"],
                 "note": "Delivered. Start the serum once a day for a week before adding a second use."},
    "MN-10022": {"status": "In transit", "steps": ORDER_STEPS, "done": 3,
                 "items": ["Salicylic Acid 2% Face Serum", "Salicylic Acid + LHA 2% Cleanser"],
                 "note": "Heads up: this order stacks two salicylic acid products. Use the Routine Diagnostic to check your pairing."},
    "MN-10023": {"status": "Return to origin", "steps": RTO_STEPS, "done": 5,
                 "items": ["Retinol 0.6% Face Serum"],
                 "note": "Delivery failed and the parcel is returning to origin. A routine quiz before purchase can reduce mismatched orders like this."},
}

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "page" not in st.session_state:
    st.session_state.page = "Routine Diagnostic"


def cart_totals():
    cart = st.session_state.cart
    n = sum(cart.values())
    value = sum(CATALOGUE[name]["price"] * qty for name, qty in cart.items() if name in CATALOGUE)
    return n, value


def go(page):
    """Navigate to a page and log a GA4-style page_view."""
    st.session_state.page = page
    log_event("page_view", page_title=page)


def on_add_product(name, source):
    cart = st.session_state.cart
    cart[name] = cart.get(name, 0) + 1
    log_event("add_to_cart", item=name, source=source)


def on_remove_product(name):
    st.session_state.cart.pop(name, None)


def on_clear_cart():
    st.session_state.cart = {}
    st.session_state.cart_added = False


def price_label(p):
    prefix = "From " if p["size"] == "from" else ""
    return f"{prefix}₹{p['price']:,}"


# ----------------------------------------------------------------------------
# MAIN LAYOUT
# ----------------------------------------------------------------------------
import base64
import os
import re

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(globals().get("__file__", "app.py"))), "images")
_IMG_CACHE = {}


def slug(name):
    """File name stem for a product photo, e.g. 'niacinamide-10-face-serum'."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def image_data_uri(name):
    """Return a data URI for images/<slug>.(png|jpg|jpeg|webp) if the file exists, else None."""
    if name in _IMG_CACHE:
        return _IMG_CACHE[name]
    for ext, mime in (("png", "image/png"), ("jpg", "image/jpeg"), ("jpeg", "image/jpeg"), ("webp", "image/webp")):
        path = os.path.join(IMG_DIR, f"{slug(name)}.{ext}")
        if os.path.exists(path):
            with open(path, "rb") as f:
                uri = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
            _IMG_CACHE[name] = uri
            return uri
    return None


def placeholder_svg(p):
    """Monochrome bottle / tube / jar drawing with the strength on the label."""
    m = re.search(r"\d+(?:\.\d+)?%", p["name"])
    label = m.group(0) if m else ("SPF 50" if "SPF" in p["name"] else "")
    stroke = 'fill="#FFFFFF" stroke="#111111" stroke-width="2"'
    cat = p.get("category", "Serum")
    if cat == "Moisturiser":
        shape = f'<rect x="24" y="76" width="72" height="58" rx="8" {stroke}/><rect x="28" y="56" width="64" height="20" rx="4" fill="#111111"/>'
        ty = 112
    elif cat in ("Cleanser", "Sunscreen"):
        shape = (f'<path d="M38 36 h44 l6 98 q0 8 -8 8 h-40 q-8 0 -8 -8 z" {stroke}/>'
                 '<rect x="42" y="20" width="36" height="16" rx="3" fill="#111111"/>')
        ty = 100
    else:
        shape = (f'<rect x="36" y="62" width="48" height="82" rx="8" {stroke}/>'
                 '<rect x="48" y="46" width="24" height="16" fill="#111111"/>'
                 f'<rect x="53" y="22" width="14" height="24" rx="7" {stroke}/>')
        ty = 108
    text = (f'<text x="60" y="{ty}" text-anchor="middle" font-size="{15 if len(label) <= 4 else 11}" font-weight="700" fill="#111111" '
            f'font-family="Helvetica, Arial, sans-serif">{label}</text>') if label else ""
    return f'<svg viewBox="0 0 120 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{p["name"]}">{shape}{text}</svg>'


def product_image_html(p):
    uri = image_data_uri(p["name"])
    inner = f'<img src="{uri}" alt="{p["name"]}">' if uri else placeholder_svg(p)
    return f'<div class="pimg">{inner}</div>'


def product_card(label, p, extra_html=""):
    src = "Site price" if p["tag"] == "site" else "Indicative price"
    size = f'<span class="size">{p["size"]}</span>' if p["size"] != "from" else ""
    if "category" not in p and p["name"] in CATALOGUE:
        p = dict(p, category=CATALOGUE[p["name"]]["category"])
    html = (
        '<div class="pcard">'
        + product_image_html(p)
        + f'<div class="top"><span class="step-label">{label}</span><span class="badge">{p["badge"]}</span></div>'
        + f'<div class="pname">{p["name"]}</div>'
        + f'<div class="pline">{p["line"]}</div>'
        + f'<div class="muted">Active: {p["active"]}</div>'
        + extra_html
        + f'<div class="price-row"><span class="price">{price_label(p)}</span>{size}<span class="src">{src}</span></div>'
        + "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def product_grid(products, ctx):
    """Browse grid: 3 cards per row, each with a working Add to cart button."""
    if not products:
        st.info("No products match this filter.")
        return
    for start in range(0, len(products), 3):
        cols = st.columns(3, gap="medium")
        for col, p in zip(cols, products[start:start + 3]):
            with col:
                product_card(p["category"], p)
                st.button("Add to cart", key=f"add_{ctx}_{p['name']}", on_click=on_add_product, args=(p["name"], ctx))


def page_banner(title, text):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{text}</p></div>', unsafe_allow_html=True)


def page_shop():
    page_banner("Shop all", "Every product in the diagnostic catalogue. Not sure what suits you? Try the Routine Diagnostic.")
    product_grid(list(CATALOGUE.values()), "shop")
    st.button("Find my routine instead", key="cta_shop_diag", on_click=go, args=("Routine Diagnostic",))


def page_best():
    page_banner("Best Sellers", "The products shoppers pick most often.")
    product_grid([p for p in CATALOGUE.values() if p["badge"] == "Best Seller"], "best")


def page_care():
    page_banner("Skin & Body Care", "Browse by step in your routine.")
    cat = st.radio("Product type", ["All", "Cleanser", "Serum", "Moisturiser", "Sunscreen"], horizontal=True, key="care_cat")
    items = [p for p in CATALOGUE.values() if cat == "All" or p["category"] == cat]
    product_grid(items, "care")


def page_diagnostic():
    page_banner("Which active is right for your skin?",
                "Choose your skin type, concern and experience. Get a safe 3-step routine, with the active, its strength and how to start.")
    left, right = st.columns([1, 1.5], gap="large")

    with left:
        st.markdown('<div class="section-title">Your skin profile</div>', unsafe_allow_html=True)
        st.selectbox("Primary Skin Type", ["Oily", "Dry", "Combination", "Sensitive", "Normal"], key="in_skin")
        st.selectbox("Main Skin Concern", list(TREATMENTS.keys()), key="in_concern")
        st.selectbox(
            "Active Serum Experience Level",
            ["Beginner (never used actives)", "Intermediate (used 1 to 2 actives)", "Advanced (regular active user)"],
            key="in_exp",
        )
        st.slider("Target Budget (INR) for the full regimen", min_value=500, max_value=3000, value=1500, step=50, key="in_budget")
        st.button("Build my routine", on_click=on_generate, key="btn_generate")

        st.markdown('<div class="section-title" style="margin-top:1.4rem;">Ingredient questions</div>', unsafe_allow_html=True)
        st.caption("Open any question for a plain-language answer.")
        for q in FAQ:
            st.toggle(q, key=f"faq_{q}", on_change=on_faq_toggle, args=(q,))
            if st.session_state.get(f"faq_{q}"):
                st.markdown(f'<div class="pcard"><span class="muted">{FAQ[q]}</span></div>', unsafe_allow_html=True)

    with right:
        r = st.session_state.regimen
        if r is None:
            st.markdown('<div class="section-title">Your custom routine</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="pcard"><span class="muted">Complete the profile and press <b>Build my routine</b>. '
                "Your three steps will appear here.</span></div>",
                unsafe_allow_html=True,
            )
            return
        st.markdown('<div class="section-title">Your custom 3-step routine</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="pill-solid">{r["skin_type"]} skin</span>'
            f'<span class="pill">{r["concern"]}</span>'
            f'<span class="pill">{r["experience"].split(" (")[0]}</span>',
            unsafe_allow_html=True,
        )
        st.write("")
        product_card("Step 1 · Cleanse", r["cleanse"])
        t = r["treat"]
        treat_extra = (
            f'<div class="safety">Safety: {t["risk"]} irritation risk</div>'
            f'<div class="muted"><b>How often:</b> {t["frequency"]}</div>'
            f'<div class="muted"><b>Purging note:</b> {t["purge"]}</div>'
            f'<div class="muted"><b>Layering:</b> {t["layering"]}</div>'
        )
        product_card("Step 2 · Treat", t, treat_extra)
        p3 = r["protect"]
        product_card(f"Step 3 · {p3['step_title']}", p3, f'<div class="muted" style="margin-top:0.3rem;">{p3["why"]}</div>')

        within = r["total"] <= r["budget"]
        status = "Within budget" if within else f"Over budget by ₹{r['total'] - r['budget']:,}"
        st.markdown(
            f"""
            <div class="total-card">
              <div class="lbl">Total routine price</div>
              <div class="amt">₹{r["total"]:,}</div>
              <div style="font-size:0.85rem;">Budget: ₹{r["budget"]:,} · {status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not within:
            if r["essential_total"] <= r["budget"]:
                st.info(f"Start with Cleanse + Treat only (₹{r['essential_total']:,}). Add the third step once budget allows. "
                        "Do not skip sunscreen if you use a tone or ageing active.")
            else:
                st.warning("Even the first two steps exceed this budget. Begin with the Treat step alone and use a gentle cleanser you already own.")

        if st.session_state.cart_added:
            st.success(f"Routine added to cart. Value: ₹{r['total']:,}")
            st.button("View cart", key="btn_view_cart", on_click=go, args=("Cart",))
        else:
            st.button("Add routine to cart", on_click=on_add_to_cart, key="btn_cart")
        st.caption("Safety note: patch-test any new active on the inner forearm for 24 hours. If you have a skin condition, "
                   "are pregnant or nursing, check with a dermatologist before starting retinoids or acids.")


def page_track():
    page_banner("Track your order", "Enter an order ID to see where it is. Demo orders for this prototype: MN-10021, MN-10022, MN-10023.")
    oid = st.text_input("Order ID", value="", placeholder="e.g. MN-10021", key="track_id").strip().upper()
    if not oid:
        return
    order = ORDERS.get(oid)
    if order is None:
        st.warning("No order found with that ID. Try one of the demo IDs above.")
        return
    if st.session_state.get("last_tracked") != oid:
        st.session_state.last_tracked = oid
        log_event("order_track", order_id=oid, status=order["status"])
    rows = ""
    for i, step in enumerate(order["steps"]):
        done = i < order["done"]
        marker = "Done" if done else "Pending"
        weight = "700" if done else "400"
        rows += (f'<div class="event-row" style="border-left-width:{3 if done else 1}px;font-weight:{weight};">'
                 f'{step} <span style="float:right;">{marker}</span></div>')
    items = "".join(f"<li>{n}</li>" for n in order["items"])
    st.markdown(
        f"""
        <div class="pcard">
          <div class="top"><span class="step-label">Order {oid}</span><span class="badge">{order["status"]}</span></div>
          <div class="pname">Status: {order["status"]}</div>
          <div class="pline"><ul style="margin:0.2rem 0 0 1.1rem;padding:0;">{items}</ul></div>
          {rows}
          <div class="muted" style="margin-top:0.7rem;">{order["note"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button("Check my routine", key="cta_track_diag", on_click=go, args=("Routine Diagnostic",))


def page_cart():
    page_banner("Your cart", "Items you added from the shop or the Routine Diagnostic.")
    cart = st.session_state.cart
    if not cart:
        st.info("Your cart is empty.")
        st.button("Go to shop", key="cta_cart_shop", on_click=go, args=("Shop",))
        return
    for name, qty in list(cart.items()):
        p = CATALOGUE.get(name)
        if p is None:
            continue
        c1, c2, c3 = st.columns([4, 1.6, 1.2])
        c1.markdown(f'<div class="pname">{name}</div><div class="muted">{p["active"]} · {p["size"] if p["size"] != "from" else "pack"}</div>',
                    unsafe_allow_html=True)
        c2.markdown(f'<div class="price">₹{p["price"] * qty:,}</div><div class="muted">Qty {qty}</div>', unsafe_allow_html=True)
        c3.button("Remove", key=f"rm_{name}", on_click=on_remove_product, args=(name,))
    n, value = cart_totals()
    st.markdown(
        f'<div class="total-card"><div class="lbl">Cart total ({n} items)</div><div class="amt">₹{value:,}</div>'
        '<div style="font-size:0.85rem;">Checkout is not part of this prototype.</div></div>',
        unsafe_allow_html=True,
    )
    st.button("Clear cart", key="btn_clear_cart", on_click=on_clear_cart)


# ---- header, announcement bar and real navigation ----
active = st.session_state.page
n_items, cart_value = cart_totals()

nav_css = "".join(
    f'div.st-key-nav_{i} div.stButton > button {{ border-bottom: 2px solid #111111 !important; font-weight: 700 !important; }}'
    f'div.st-key-nav_{i} div.stButton > button p {{ color: #111111 !important; }}'
    for i, pg in enumerate(PAGES) if pg == active
)
if active == "Cart":
    nav_css += "div.st-key-nav_cart div.stButton > button { background: #111111 !important; }" \
               "div.st-key-nav_cart div.stButton > button p { color: #FFFFFF !important; }"
st.markdown(f"<style>{nav_css}</style>", unsafe_allow_html=True)

st.markdown(
    '<div class="announce">Routine Diagnostic · Find your safe starting routine in four questions</div>'
    '<div class="site-header"><div class="wordmark">minimalist<small>student prototype</small></div></div>',
    unsafe_allow_html=True,
)
nav_cols = st.columns([0.8, 1.1, 1.6, 1.8, 1.2, 0.6, 1.5])
for i, pg in enumerate(PAGES):
    with nav_cols[i]:
        st.button(pg, key=f"nav_{i}", on_click=go, args=(pg,))
with nav_cols[6]:
    st.button(f"Cart ₹{cart_value:,} ({n_items})", key="nav_cart", on_click=go, args=("Cart",))
st.markdown('<div style="border-bottom:1px solid #F0F0F0;margin:0 0 1.2rem 0;"></div>', unsafe_allow_html=True)

# ---- page body ----
{
    "Shop": page_shop,
    "Best Sellers": page_best,
    "Skin & Body Care": page_care,
    "Routine Diagnostic": page_diagnostic,
    "Track Order": page_track,
    "Cart": page_cart,
}.get(active, page_diagnostic)()

# ----------------------------------------------------------------------------
# SIDEBAR: LIVE GA4 EVENT MONITOR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Live GA4 Event Monitor")
    st.caption("Custom micro-conversions logged to st.session_state as you interact.")

    n_quiz = count_events("routine_quiz_complete")
    n_faq = count_events("ingredient_faq_expand")
    n_cart = count_events("routine_add_to_cart")

    c1, c2, c3 = st.columns(3)
    c1.metric("Quiz", n_quiz)
    c2.metric("FAQ", n_faq)
    c3.metric("Cart", n_cart)

    st.markdown("#### Micro-conversion funnel")
    quiz_to_cart = (n_cart / n_quiz * 100) if n_quiz else 0.0
    faq_assist = (n_faq / n_quiz * 100) if n_quiz else 0.0
    st.markdown(
        f'<div class="pcard"><span class="muted">Quiz → Cart rate: <b>{quiz_to_cart:.0f}%</b><br>'
        f"FAQ opens per quiz: <b>{faq_assist:.0f}%</b></span></div>",
        unsafe_allow_html=True,
    )

    st.markdown("#### Event stream (latest first)")
    if not st.session_state.events:
        st.markdown('<div class="muted">No events yet. Interact with the app.</div>', unsafe_allow_html=True)
    else:
        for e in reversed(st.session_state.events[-12:]):
            params = ", ".join(f"{k}={v}" for k, v in e["params"].items())
            st.markdown(
                f'<div class="event-row"><b>{e["event_name"]}</b><br>{e["timestamp"]}<br>{params}</div>',
                unsafe_allow_html=True,
            )

    if st.button("Clear event log", key="btn_clear"):
        st.session_state.events = []
        st.session_state.regimen = None
        st.session_state.cart_added = False
        st.session_state.cart = {}
        st.rerun()

# ----------------------------------------------------------------------------
# BRAND PILLARS + EXECUTIVE SUMMARY FOOTER
# ----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div class="section-title">Why this diagnostic exists</div>
    <div class="pillars">
      <div class="pillar"><b>Transparency</b><span>Every active and its percentage is shown, with what it does and how to start.</span></div>
      <div class="pillar"><b>Efficacy</b><span>Strength is matched to your experience, so the routine works without overwhelming skin.</span></div>
      <div class="pillar"><b>Affordable</b><span>A budget check with a start-small fallback, so the cost never blocks the first step.</span></div>
      <div class="pillar"><b>Only the best</b><span>Safety-first logic: no stacked exfoliants, purging guidance and layering rules built in.</span></div>
    </div>
    <div class="exec">
      <div class="step-label">Executive summary</div>
      <p style="margin:0.4rem 0 0 0;">
      Visitors who read an ingredient page and leave are not low-intent. They are hesitating over what to buy,
      how strong it should be and whether it will clash with something they already use. This diagnostic answers
      those questions in one place and replaces choice overload with a single safe routine. Each step is captured
      as a GA4 micro-conversion (<code>routine_quiz_complete</code>, <code>ingredient_faq_expand</code>,
      <code>routine_add_to_cart</code>), so a hesitator who completes the quiz but does not add to cart becomes a
      measurable, retargetable audience instead of an anonymous PDP bounce. Safer first-time recommendations should
      also reduce mismatched orders and returns-to-origin.
      </p>
    </div>
    <div class="disclaimer">Student prototype for MBA561B CIA 1. Not an official Minimalist tool and not affiliated with the brand.
    "Site price" = seen on beminimalist.co (smallest size); "Indicative price" = estimate, verify before use.
    Orders on the Track Order page are simulated.</div>
    """,
    unsafe_allow_html=True,
)
