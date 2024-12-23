import streamlit as st
from streamlit_option_menu import option_menu
from Homepage import Home
from second_page import second
from third_page import third

def main():
    st.set_page_config(layout="wide")
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .center-title {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 70px;  
                font-size: 3rem;
                font-weight: bold;
            }
           
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    st.markdown('<div class="center-title">ASTROLOGY CALCULATION</div>', unsafe_allow_html=True)

    selected = option_menu(
        None, 
        ["Home", "Second Page","Third Page"],  
        menu_icon="cast", 
        default_index=0, 
        orientation="horizontal",
        styles={
            "container": {"padding": "0"},
            "icon": {"font-size": "20px"},  # Smaller icon size
            "nav-link": {
                "font-size": "16px",  # Smaller font size for compact look
                "padding": "5px 10px",  # Less padding for a compact appearance
                "margin": "0px"
            },
        }
        )
    if selected == "Home":
        Home()
    elif selected == "Second Page":
        second()
    elif selected == "Third Page":
        third()


if __name__ == '__main__':
    main()