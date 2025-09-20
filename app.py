import streamlit as st
from config import configure_api, page_setup
from model import summarize_notes
from ui import render_input, render_output

# --- Setup ---
configure_api()
page_setup()

st.title("🩺 Patient Pre-Consultation Summarizer")
st.markdown(
    "This tool uses AI to transform patient notes into a structured summary for clinicians."
)
st.markdown("---")

# --- Layout ---
col1, col2 = st.columns([1, 1])
with col1:
    patient_input, summarize_button = render_input()

with col2:
    summary_box = render_output()

# --- Logic ---
if summarize_button:
    if not patient_input.strip():
        st.warning("⚠️ Please enter some patient notes first.")
    else:
        with st.spinner("⏳ Summarizing notes..."):
            try:
                summary = summarize_notes(patient_input)
                summary_box.success(summary)
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.info("Check your API key or network connection.")
