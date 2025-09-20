import google.generativeai as genai
import os
import streamlit as st

# --- Configuration ---
# To get your free API key, go to Google AI Studio: https://aistudio.google.com/app/apikey
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except AttributeError:
    st.error("🚨 Gemini API key not found! Please set the GEMINI_API_KEY environment variable.")
    st.stop()

# --- App Title and Description ---
st.set_page_config(page_title="Patient Summarizer", page_icon="🩺", layout="wide")
st.title("🩺 Patient Pre-Consultation Summarizer")
st.markdown("Enter patient notes below to generate a concise, structured summary for clinicians using AI.")
st.markdown("---")


# --- Model and Prompt Configuration ---
def get_model():
    """Initializes and returns the Gemini Pro model."""
    return genai.GenerativeModel('gemini-1.5-flash-latest')

# This system instruction guides the model on its role and desired output format.
SYSTEM_PROMPT = """
You are a highly efficient medical assistant. Your task is to summarize a patient's free-text notes into a structured, concise summary for a clinician.
Summarise to 50 percent of the original character length.
Keep only key details.
Do not add information not present in the text.

Categorise into:

- Background (social, family history, work/lifestyle)
- Current Health Issues (symptoms, diagnoses, concerns)
- Current Management (medications, coping strategies, advice sought, what they are doing/not doing)

For each category, indicate how the summary was derived.
Use short paraphrased notes.
Provide the exact quote or fragment from the text that supports each point.
Do not invent, assume, or interpret beyond what is explicitly said.
"""

# --- Streamlit UI Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Patient's Notes")
    patient_input = st.text_area(
        "Enter the full, unedited notes from the patient here.",
        height=300,
        placeholder="e.g., 'I've had a sharp pain in my lower back for the last 3 days, especially when I wake up. It's a dull ache most of the day...'"
    )
    summarize_button = st.button("Generate Summary", type="primary", use_container_width=True)

with col2:
    st.subheader("Clinician's Summary")
    summary_output_box = st.empty() # Placeholder for the output
    summary_output_box.markdown(
        """
        <div style="background-color:#f0f2f6; padding: 20px; border-radius: 10px; height: 340px; display: flex; align-items: center; justify-content: center;">
            <p style="color: #555;">The generated summary will appear here.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Application Logic ---
if summarize_button:
    if not patient_input.strip():
        st.warning("Please enter some patient notes before generating a summary.")
    else:
        with st.spinner("AI is summarizing the notes..."):
            try:
                model = get_model()
                full_prompt = f"{SYSTEM_PROMPT}\n\nPlease summarize the following patient notes:\n\n---\n\n{patient_input}"
                
                response = model.generate_content(full_prompt)
                
                # Display the summary
                summary_output_box.info(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("This might be due to an invalid API key or a network issue. Please check your key and try again.")
