import streamlit as st
from config import configure_api, page_setup
from model import summarize_notes
from ui import render_input, render_output_layout
from disclaimer import show_disclaimer

# --- Setup ---
configure_api()
page_setup()

st.title("🩺 AI-Powered Clinical Summarizer")
st.markdown("This tool uses AI to summarize patient notes and highlights the source of each summary point in the original text.")
st.markdown("---")

show_disclaimer()   # 👈 call it here so it shows at the top

st.markdown("---")

# --- Input Section ---
patient_input, summarize_button = render_input()

st.markdown("---")

# Output columns will appear below
col1, col2 = st.columns(2)
# The ui.py function now returns two separate placeholders
with col1:
    highlighted_text_display, summary_display = render_output_layout()

# --- Logic ---
if summarize_button:
    if not patient_input.strip():
        st.warning("⚠️ Please enter some patient notes first.")
    else:
        with st.spinner("⏳ Analyzing and linking notes..."):
            try:
                # The model now returns a dictionary with categories
                summary_data = summarize_notes(patient_input)

                if not summary_data:
                    st.warning("The AI could not extract summary points. Try rephrasing.")
                    st.stop()
                
                # --- Highlighting and Display Logic ---
                colors = ["#FFADAD", "#FFD6A5", "#FDFFB6", "#CAFFBF", "#9BF6FF", "#A0C4FF", "#BDB2FF", "#FFC6FF"]
                highlighted_text = patient_input
                summary_html_parts = []
                color_index = 0
                
                # Define the order to display categories
                categories = ["ideas", "concerns", "expectations"]

                for category in categories:
                    # Check if the category exists in the AI's response
                    if category in summary_data and summary_data[category]:
                        # Add a styled header for the category
                        summary_html_parts.append(f'<h4 style="margin-bottom: 5px; margin-top: 15px; text-transform: capitalize; border-bottom: 2px solid #eee; padding-bottom: 5px;">{category}</h4>')
                        
                        # Loop through each point in the category
                        for item in summary_data[category]:
                            point = item.get("point")
                            quote = item.get("source_quote")
                            
                            # Use a cycling index for colors
                            color = colors[color_index % len(colors)]

                            if point and quote and quote in highlighted_text:
                                highlight = f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 4px;">{quote}</span>'
                                highlighted_text = highlighted_text.replace(quote, highlight, 1)
                                summary_html_parts.append(f'<div style="margin-bottom: 8px; border-left: 5px solid {color}; padding-left: 10px;">{point}</div>')
                                color_index += 1 # Ensure next point gets a new color

                # Display the final results in the placeholders
                highlighted_text_display.markdown(f'<div style="white-space: pre-wrap; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0;">{highlighted_text}</div>', unsafe_allow_html=True)
                summary_display.markdown("".join(summary_html_parts), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

