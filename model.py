import google.generativeai as genai
from prompts import SYSTEM_PROMPT

def get_model():
    """Initialize and return the Gemini model."""
    return genai.GenerativeModel("gemini-1.5-flash-latest")

def summarize_notes(notes: str) -> str:
    """Send patient notes to the model and return the summary text."""
    model = get_model()
    full_prompt = f"{SYSTEM_PROMPT}\n\nPatient Notes:\n---\n{notes}"
    response = model.generate_content(full_prompt)
    return response.text
