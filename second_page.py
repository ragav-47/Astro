import streamlit as st
import pandas as pd
from streamlit_utils import display_table
from calculations import calculate_and_display,process_and_calculate

star = ["அசுவினி", "பரணி", "கிருத்திகை", "ரோகிணி", "மிருகசீரிடம்", "திருவாதிரை", "புனர்பூசம்", "பூசம்", "ஆயில்யம்", "மகம்", "பூரம்", "உத்திரம்", "ஹஸ்தம்", "சித்திரை", "சுவாதி", "விசாகம்", "அனுஷம்", "கேட்டை", "மூலம்", "பூராடம்", "உத்திராடம்", "திருவோணம்", "அவிட்டம்", "சதயம்", "பூரட்டாதி", "உத்திரட்டாதி", "ரேவதி"]
Rasi = ['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)', 'கும்பம் (சனி)', 'மீனம் (குரு)']

def second():
    st.title('Second Page')
    if 'column1_data' in st.session_state and 'column2_data' in st.session_state:
        column1_data = st.session_state['column1_data']
        column2_data = st.session_state['column2_data']
        row_names = st.session_state['row_names']
        
        column1_processed, rasi1, star1 = process_and_calculate(column1_data, 10)
        column2_processed, rasi2, star2 = process_and_calculate(column2_data, 10)
        
        display_table(row_names, column1_processed, column2_processed, rasi2, star2)
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
