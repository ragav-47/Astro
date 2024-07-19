import streamlit as st
from streamlit_option_menu import option_menu
from Homepage import Home
from second_page import second
def main():
    st.set_page_config(layout="wide")
    selected = option_menu(
        None, 
        ["Home", "Second Page"],  
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal",
        styles={"container": {"padding": "0"},
    "icon": {"font-size": "20px"},  # Smaller icon size
    "nav-link": {
        "font-size": "16px",  # Smaller font size for compact look
        "padding": "5px 10px",  # Less padding for a compact appearance
        "margin": "0px"
    },}
        )
    if selected == "Home":
        Home()
    elif selected == "Second Page":
        second()


if __name__ == '__main__':
    main()
