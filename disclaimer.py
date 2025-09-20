import streamlit as st

def show_disclaimer():
    """Render collapsible disclaimer box."""
    with st.expander("⚠️ Disclaimer"):
        st.markdown(
            """
            Your responses will be seen by your healthcare team to help guide your consultation.  

            This is **not an emergency service** — if you have urgent concerns or worsening symptoms,  
            please contact **NHS 111** or call **999** immediately.
            """
        )