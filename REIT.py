from config import setup_page_config
from ui import render_header, render_footer, render_real_estate_section

def main():
    setup_page_config()
    render_header()
    render_real_estate_section()
    render_footer()

if __name__ == "__main__":
    main()
