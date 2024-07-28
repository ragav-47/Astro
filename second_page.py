import streamlit as st
import pandas as pd
from streamlit_utils import display_table
from calculations import calculate_and_display,process_and_calculate
from saps import cal_saps
import datetime
star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]
Rasi = ['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)', 'கும்பம் (சனி)', 'மீனம் (குரு)']

def second():
    # st.title('Second Page')
    col1, col2 = st.columns(2)
    
    with col1:
        if 'selected_date' in st.session_state:
            selected_date = st.session_state.selected_date
            selected_date_str = selected_date.strftime("%d/%m/%Y")
        else:
            selected_day = "No date selected"
        st.markdown(
            f"""
            <div style="padding: 5px; border: 1px solid #d3d3d3; border-radius: 5px; background-color: #f9f9f9; margin-top: 29px; margin-bottom: 20px">
                <div style="font-size: 16px; color: #333; font-weight: bold">{selected_date_str}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        if 'selected_date' in st.session_state:
            selected_date = st.session_state.selected_date
            selected_day = selected_date.strftime("%A")
        else:
            selected_day = "No date selected"
        st.markdown(
            f"""
            <div style="padding: 5px; border: 1px solid #d3d3d3; border-radius: 5px; background-color: #f9f9f9; margin-top: 29px;margin-bottom: 20px">
                <div style="font-size: 16px; color: #333; font-weight: bold">{selected_day}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if 'column1_data' in st.session_state and 'column2_data' in st.session_state:
        column1_data = st.session_state['column1_data']
        column2_data = st.session_state['column2_data']
        row_names = st.session_state['row_names']
        
        column1_processed, rasi1, star1 = process_and_calculate(column1_data, 10)
        column2_processed, rasi2, star2 = process_and_calculate(column2_data, 10)
        saps = []
        for i in range(len(row_names)):
            h1, m1, s1 = map(int, column1_processed[i].split(':'))
            h2, m2, s2 = map(int, column2_processed[i].split(':'))
            saps.append(cal_saps(h1, m1, s1,h2, m2, s2))

        stars_combined = []
        for i in range(len(row_names)):
            if star1[i] != star2[i]:
                stars_combined.append(f"{star1[i]} & {star2[i]}")
            else:
                stars_combined.append(star1[i])
        
        display_table(row_names, column1_processed, column2_processed, rasi2, stars_combined,saps)
        # st.write(column1_data[5])
        selected_row_col1 = st.selectbox('Select Row', row_names)
        if st.button('Start Calculation'):
            try:
                index_1 = row_names.index(selected_row_col1)
                if ':' in column1_processed[index_1] and ':' in column2_processed[index_1]:
                    col1, col2 = st.columns(2)
                    with col1:
                        calculate_and_display(index_1, column1_processed, row_names, col_number=1)
                    with col2:
                        calculate_and_display(index_1, column2_processed, row_names, col_number=2)
                else:
                    st.write("Invalid input format. Please enter valid time values in HH:MM:SS format.")
            except ValueError:
                st.write("Error: Please enter valid time values in HH:MM:SS format.")
    else:
        st.write("No data available. Please go back to the home page and update the table.")
