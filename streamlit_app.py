import streamlit as st

st.set_page_config(
    page_title="ESRS Fun Dashboard 🌟",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------
# Styling
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #E6E6FA;
}
.big-font {
    font-size:30px !important;
    color: #6A0DAD;
    font-weight: bold;
}
.medium-font {
    font-size:22px !important;
    color: #4B0082;
    font-weight: bold;
}
.fun-text {
    font-size:18px !important;
    color: #483D8B;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Functions
# ---------------------------
def read_text_file(txt_file):
    text = txt_file.read().decode("utf-8")
    return text.lower()

def calculate_score(text):
    score = 0
    missing = []

    checks = {
        "Baseline": ("baseline", 20),
        "Monitoring Period": ("week", 20),
        "Measurement Method": ("meter", 15),
        "Weather Normalization": ("weather", 15),
        "Regression Baseline": ("regression", 10),
        "Data Period": ("data", 10),
        "Operational Changes": ("operation", 10)
    }

    for item, (keyword, value) in checks.items():
        if keyword in text:
            score += value
        else:
            missing.append(item)

    return score, missing

def reliability_info(score):
    if score >= 80:
        return "Excellent", "green", "😁"
    elif score >= 60:
        return "Good", "orange", "😐"
    else:
        return "Poor", "red", "😢"

# ---------------------------
# UI Header
# ---------------------------
st.markdown("<h1 class='big-font'>Energy Savings Reliability Score (ESRS) ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p class='fun-text'>Upload your project text and evaluate credibility instantly!</p>", unsafe_allow_html=True)

txt_file = st.file_uploader("Upload TXT file 📂", type=["txt"])

if txt_file:
    text = read_text_file(txt_file)
    score, missing = calculate_score(text)

    category, color, emoji = reliability_info(score)

    # Score Section
    st.markdown("## 🌟 Reliability Score")
    st.progress(score)
    st.markdown(f"<h2 style='color:{color}'>{score}% {emoji}</h2>", unsafe_allow_html=True)

    # Category
    st.info(f"Reliability Category: **{category}**")

    # Joyful celebration
    if score >= 80:
        st.balloons()

    # Management Recommendation
    st.markdown("## 🎯 Management Recommendation")
    if score >= 80:
        st.success("Use this case study confidently for client presentation.")
    elif score >= 60:
        st.warning("Acceptable but consider improving documentation.")
    else:
        st.error("Not recommended for client presentation.")

    # Missing items
    if missing:
        st.markdown("## ⚠️ Missing Information")
        for m in missing:
            st.write(f"• {m}")

    # Useful Info Section
    st.markdown("## 📊 Why This Matters")
    st.write("""
    This score helps management:
    - Select strong case studies
    - Avoid overclaiming savings
    - Improve proposal credibility
    - Standardize project documentation
    """)

    # KPI Boxes
    col1, col2, col3 = st.columns(3)

    col1.metric("Reliability Score", f"{score}%")
    col2.metric("Missing Items", len(missing))
    col3.metric("Status", category)

    # Footer fun message
    st.markdown("---")
    st.markdown("💜 Built for Energy Engineers | ESRS AI Checker")
