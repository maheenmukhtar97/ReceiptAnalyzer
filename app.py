import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from ocr_utils import extract_text
from parser import parse_receipt
from categorizer import apply_categorization
from analysis import analyze_spending
from llm_advice import generate_advice
from ocr_utils import preprocess_image, extract_text


st.set_page_config(
    page_title="AI Receipt Analyzer",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

div[data-testid="stVerticalBlock"] > div {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; margin-bottom: 5px;'>
        🧾 AI Receipt Analyzer
    </h1>
    <p style='text-align: center; color: gray; font-size: 16px;'>
        Upload a receipt and extract structured data instantly
    </p>
""", unsafe_allow_html=True)

st.markdown("---")


st.title("🧾 AI-Powered Receipt Analyzer")
with st.container():
    st.markdown("### 📤 Upload Receipt")

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "png", "jpeg"]
    )

# OCR Section
if uploaded_file:

    image = Image.open(uploaded_file)

    st.markdown("## 🖼 Image Processing")

    with st.spinner("Processing image..."):
        gray, thresh, adaptive = preprocess_image(image)

    # -------- ROW 1 --------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Receipt")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Grayscale")
        st.image(gray, use_container_width=True)

    # -------- ROW 2 --------
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Threshold")
        st.image(thresh, use_container_width=True)

    with col4:
        st.subheader("Adaptive")
        st.image(adaptive, use_container_width=True)

    # OCR
    with st.spinner("Extracting text..."):
        text = extract_text(adaptive)

    st.markdown("## 📝 Extracted Text")

    st.code(text, language="text")

    
    # Parsing
    df = parse_receipt(text)
    
    if not df.empty:
        df = apply_categorization(df)
        
        st.subheader("Structured Data")
        st.dataframe(df)
        
        category_totals, percentages, total_spending = analyze_spending(df)
        
        st.subheader("Spending Analysis")
        st.write(f"Total Spending: ${total_spending:.2f}")
        
        fig, ax = plt.subplots(figsize=(4, 3))
        category_totals.plot(kind="bar", ax=ax)
        st.pyplot(fig)
        
                # LLM Advice
        with st.spinner("Generating AI Advice..."):
            advice = generate_advice(category_totals, percentages, total_spending)

        # Inject CSS (only once is fine)
        st.markdown("""
        <style>
        .advice-container {
            background: linear-gradient(145deg, #1f2b3d, #16202f);
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0px 6px 25px rgba(0,0,0,0.45);
            margin-top: 25px;
        }

        .advice-container h2 {
            color: #61d5ff;
            margin-bottom: 20px;
        }

        .advice-container strong {
            color: #ffd166;
        }

        .advice-container p {
            line-height: 1.8;
            color: #e6f1ff;
            font-size: 16px;
        }

        .advice-container li {
            margin-bottom: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Styled Advice Card Wrapper
        st.markdown('<div class="advice-container">', unsafe_allow_html=True)

        st.markdown("## 💡 AI Financial Advice")
        st.markdown(advice)

        st.markdown('</div>', unsafe_allow_html=True)
