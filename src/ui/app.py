import streamlit as st
import sys, os, tempfile

# Ścieżka do src/, żeby działał import pipeline.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pipeline

st.set_page_config(
    page_title="AI Cartridge Identifier",
    page_icon="🖨️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark theme
st.markdown("""
<style>
body { background:#0e1117; color:#fafafa; }
.stApp { background:#0e1117; }
.block-container { padding-top:2rem; }
[data-baseweb="input"] input, textarea, .stFileUploader { background:#262730 !important; color:#fafafa !important; }
</style>
""", unsafe_allow_html=True)

st.title("🖨️ AI Cartridge Identifier")
st.caption("Upload an image or paste text. The app will extract the model (e.g., **Canon PG-545XL**).")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload image (JPG/PNG)", type=["jpg","jpeg","png"])
with col2:
    manual_text = st.text_area("Or paste product text")

if st.button("🔍 Identify"):
    # 1) Przygotuj tekst wejściowy
    extracted = ""
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        with st.spinner("Running OCR..."):
            extracted = pipeline.extract_text_from_image(tmp_path)
        os.remove(tmp_path)
    elif manual_text.strip():
        extracted = manual_text.strip()
    else:
        st.error("Provide an image or some text.")
        st.stop()

    st.markdown("### 📝 Extracted text")
    st.code(extracted or "(empty)")

    # 2) Predykcja modelu
    with st.spinner("Identifying model with AI..."):
        result = pipeline.process(text=extracted)

    # 3) Obsługa ewentualnych błędów
    if isinstance(result, dict) and result.get("error"):
        st.error(result["error"])
        st.stop()

    model = (result or {}).get("model")
    confidence = float((result or {}).get("confidence") or 0.0)
    candidates = (result or {}).get("candidates") or []

    st.markdown("### ✅ Result")
    if model:
        st.success(f"Model: **{model}**")
    else:
        st.warning("No model detected.")

    st.progress(min(max(confidence, 0.0), 1.0))
    st.caption(f"Confidence: {confidence*100:.1f}%")

    if candidates:
        st.markdown("**Other candidates:**")
        for c in candidates:
            st.markdown(f"- {c}")

