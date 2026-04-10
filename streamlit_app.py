import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ESRS Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ---------------- AESTHETIC CLASSIC THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #2B1B3F, #3A2A55);
    font-family: 'Playfair Display', serif;
}

/* Title */
.main-title {
    font-size: 38px;
    color: #F1E9FF;
    text-align: center;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 40px;
    letter-spacing: 1px;
}

/* Sub text */
p, label, div {
    color: #E6E0F5;
}

/* File uploader spacing */
section[data-testid="stFileUploader"] {
    background-color: #4A3A6A;
    padding: 20px;
    border-radius: 12px;
    margin-top: 30px;
    margin-bottom: 25px;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #4A3A6A;
    border-radius: 12px;
    padding: 10px;
}

/* Buttons */
.stDownloadButton button {
    background-color: #7C5AC7;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
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
        return "Needs Improvement", "red", "😢"

# ---------------- HEADER ----------------
st.markdown("<div class='main-title'>Energy Savings Reliability Score (ESRS)</div>", unsafe_allow_html=True)

st.write("")  # extra spacing

# ---------------- UPLOAD ----------------
txt_file = st.file_uploader("Upload your project report (TXT file)", type=["txt"])

# ---------------- MAIN ----------------
if txt_file:
    text = read_text_file(txt_file)
    score, missing = calculate_score(text)

    category, color, emoji = reliability_info(score)

    # Score section
    st.subheader("Reliability Score")
    st.progress(score)
    st.markdown(f"<h2 style='color:#F1E9FF; text-align:center'>{score}% {emoji}</h2>", unsafe_allow_html=True)

    if score >= 80:
        st.balloons()
        st.success("Excellent case study — ready for client presentation.")
    elif score >= 60:
        st.info("Good quality — minor improvements recommended.")
    else:
        st.warning("Needs improvement before presentation.")

    # KPI
    st.subheader("Key Insights")
    col1, col2, col3 = st.columns(3)

    col1.metric("Score", f"{score}%")
    col2.metric("Missing Items", len(missing))
    col3.metric("Category", category)

    # Recommendation
    st.subheader("Management Recommendation")

    if score >= 80:
        st.success("Use confidently for client proposal.")
    elif score >= 60:
        st.warning("Acceptable but improve documentation.")
    else:
        st.error("Not recommended for presentation.")

    # Missing info
    if missing:
        st.subheader("Missing Information")
        for m in missing:
            st.write(f"• {m}")

    # Why it matters
    st.subheader("Why This Matters")
    st.write("""
    ✔ Improves proposal credibility  
    ✔ Standardizes reporting quality  
    ✔ Reduces overclaiming risk  
    ✔ Builds client trust  
    """)

    # Report download
    report = f"""
ESRS REPORT
Date: {datetime.now()}

Score: {score}%
Category: {category}
Missing: {", ".join(missing)}
"""

    st.download_button(
        label="Download ESRS Report",
        data=report,
        file_name="ESRS_Report.txt",
        mime="text/plain"
    )

st.markdown("---")
st.markdown("ESRS Dashboard | Energy Engineering Tool ⚡")
