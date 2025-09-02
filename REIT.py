from config import setup_page_config
from ui import render_header, render_footer, render_real_estate_section
from i18n import get_current_language
import streamlit as st

def main():
    # Inizializza la lingua di default se non esiste
    if 'language' not in st.session_state:
        st.session_state.language = 'it'
    
    setup_page_config()
    render_header()
    render_real_estate_section()
    render_footer()

if __name__ == "__main__":
    main()
