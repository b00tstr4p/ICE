import os
import streamlit as st
import google.generativeai as genai

def configure_api():
    """Configure Gemini API with the environment variable."""
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    except AttributeError:
        st.error("🚨 Gemini API key not found! Please set GEMINI_API_KEY.")
        st.stop()

def page_setup():
    """Set Streamlit page config."""
    st.set_page_config(
        page_title="Patient Summarizer",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="collapsed",
    )