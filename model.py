import google.generativeai as genai
import json
import re
from prompts import SYSTEM_PROMPT

def get_model():
    """Initialize and return the Gemini model."""
    return genai.GenerativeModel("gemini-1.5-flash-latest")

def summarize_notes(notes: str) -> dict:
    """
    Sends patient notes to the model, requests a structured JSON response,
    parses it, and returns a dictionary of categorized summary points.
    """
    model = get_model()
    
    # We combine the system prompt and the user's notes into a single string.
    # This avoids the 'system_instruction' error and works across library versions.
    full_prompt = f"{SYSTEM_PROMPT}\n\nPatient Notes:\n---\n{notes}"

    try:
        # Request a JSON response from the model
        response = model.generate_content(
            full_prompt,
            generation_config={"response_mime_type": "application/json"},
        )
        
        # Clean the response to ensure it's valid JSON
        clean_json_str = re.sub(r'```json\s*|\s*```', '', response.text.strip(), flags=re.DOTALL)
        data = json.loads(clean_json_str)
        
        return data

    except json.JSONDecodeError:
        # Handle cases where the model doesn't return valid JSON
        raise ValueError("The AI returned an invalid format. Please try again.")
    except Exception as e:
        # Handle other potential API errors
        raise RuntimeError(f"An error occurred with the AI model: {e}")
