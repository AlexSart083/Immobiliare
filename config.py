import streamlit as st
from i18n import get_text

def setup_page_config():
    st.set_page_config(
        page_title=get_text('page_title'),
        page_icon="🏠",
        layout="wide"
    )
