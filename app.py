import streamlit as st
import requests
import os

# ======================
# CONFIG
# ======================
API_URL = os.getenv("API_URL", "http://localhost:8000/generate")  # replace with deployed FastAPI URL

st.set_page_config(page_title="CareBuddy - Health Advice", page_icon="💊", layout="centered")

# ======================
# HEADER
# ======================
st.title("💊 CareBuddy")
st.caption("Upload your doctor’s prescription or describe your problem. Get home remedies + motivation instantly.")

with st.expander("ℹ️ How it works"):
    st.markdown(
        """
        1. 📝 Upload your doctor's prescription (TXT/PDF/Image) **or type your problem**.  
        2. 🤖 Our AI (LangChain + HuggingFace) processes it.  
        3. 💡 You'll receive **safe home remedies**, **health tips**, and **motivation**.  

        ⚠️ **Disclaimer:** This tool is **educational** only. Always follow your doctor’s advice for serious issues.
        """
    )

# ======================
# INPUT
# ======================
uploaded_file = st.file_uploader("Upload Prescription (txt/pdf/jpg/png)", type=["txt", "pdf", "jpg", "jpeg", "png"])
manual_text = st.text_area("Or type your problem here 👇", placeholder="e.g., Doctor told me about acidity, but I forgot the remedies...")

# ======================
# FUNCTION
# ======================
def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file depending on format"""
    import pdfplumber
    from PIL import Image
    import pytesseract

    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()

    elif file_type in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)
        return text.strip()

    else:
        return ""

# ======================
# SUBMIT
# ======================
if st.button("🚀 Get Health Advice", use_container_width=True):
    # decide input
    topic_text = ""

    if uploaded_file:
        with st.spinner("📑 Extracting text from file..."):
            topic_text = extract_text_from_file(uploaded_file)

    elif manual_text.strip():
        topic_text = manual_text.strip()

    if not topic_text:
        st.error("❌ Please upload a prescription or type your problem.")
    else:
        with st.spinner("🤖 Generating advice..."):
            try:
                response = requests.post(API_URL, json={"topic": topic_text}, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Advice generated!")
                    st.subheader("💡 Doctor-like Advice & Remedies")
                    st.write(data["advice"])
                else:
                    st.error(f"⚠️ API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"❌ Could not connect to backend: {e}")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("Built with ❤️ using FastAPI, LangChain, HuggingFace & Streamlit")
