import streamlit as st

def render_input():
    """Render patient notes input panel."""
    st.subheader("📝 Patient's Notes")
    notes = st.text_area(
        "Before your appointment, please tell us what’s on your mind. You can write about anything — your ideas, worries, or what you hope to get from the consultation. There are no right or wrong answers.:",
        height=320,
        placeholder="e.g., 'I've had sharp pain in my lower back for 3 days...'",
    )
    button = st.button("✨ Generate & Highlight Summary", type="primary", use_container_width=True)
    return notes, button

def render_output_layout():
    """Create the side-by-side layout for the summary and highlighted text."""
    col1, col2 = st.columns(2)

    # Column 1: Key Points (Summary) - on the LEFT
    with col1:
        st.subheader("Traceable Summary")
        summary_placeholder = st.empty()
        summary_placeholder.info("The summary, color-coded to match highlights, will appear here.")

    # Column 2: Highlighted Text - on the RIGHT
    with col2:
        st.subheader("Highlighted Patient Notes")
        highlighted_text_placeholder = st.empty()
        highlighted_text_placeholder.info("The original text with highlights will appear here.")
    
    # Return the two placeholder objects for the main app to use
    return summary_placeholder, highlighted_text_placeholder
