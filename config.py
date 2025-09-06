import streamlit as st
from i18n import get_text

def setup_page_config():
    # Inizializza la lingua di default se non esiste
    if 'language' not in st.session_state:
        st.session_state.language = 'it'
    
    st.set_page_config(
        page_title=get_text('page_title'),
        page_icon="🏠",
        layout="wide"
    )
