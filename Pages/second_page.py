import streamlit as st
import pandas as pd
from streamlit_utils import display_table
from calculations import calculate_and_display

star = ["அசுவினி", "பரணி", "கிருத்திகை", "ரோகிணி", "மிருகசீரிடம்", "திருவாதிரை", "புனர்பூசம்", "பூசம்", "ஆயில்யம்", "மகம்", "பூரம்", "உத்திரம்", "ஹஸ்தம்", "சித்திரை", "சுவாதி", "விசாகம்", "அனுஷம்", "கேட்டை", "மூலம்", "பூராடம்", "உத்திராடம்", "திருவோணம்", "அவிட்டம்", "சதயம்", "பூரட்டாதி", "உத்திரட்டாதி", "ரேவதி"]
Rasi = ['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)', 'கும்பம் (சனி)', 'மீனம் (குரு)']

st.title('Second Page')

def process_and_calculate(column_data, reference_index):
    processed_data = []
    h_ref, m_ref, s_ref = map(int, column_data[reference_index].split(':'))

    for time_str in column_data:
        h, m, s = map(int, time_str.split(':'))
        total_seconds = (h_ref + h) * 3600 + (m_ref + m) * 60 + (s_ref + s)
        result_time = f"{total_seconds // 3600:02}:{(total_seconds % 3600) // 60:02}:{total_seconds % 60:02}"

        h, m, s = map(int, result_time.split(':'))
        new_h = h // 2
        m += (h % 2) * 60
        new_m = m // 2
        new_s = (m % 2) * 60 + s
        if new_s % 2 != 0:
            new_s += 1
        new_s //= 2
        divided_result = f"{new_h:02}:{new_m:02}:{new_s:02}"
        processed_data.append(divided_result)
    
    rasi_results = []
    star_results = []
    for time_str in processed_data:
        h, m, s = map(int, time_str.split(':'))
        total_seconds = h * 3600 + m * 60 + s
        rasi_index = int(h // (360 / 12)) % 12
        star_index = int(total_seconds // ((360 * 3600) / 27)) % 27
        rasi_results.append(Rasi[rasi_index])
        star_results.append(star[star_index])
    
    return processed_data, rasi_results, star_results

if 'column1_data' in st.session_state and 'column2_data' in st.session_state:
    column1_data = st.session_state['column1_data']
    column2_data = st.session_state['column2_data']
    row_names = st.session_state['row_names']
    
    column1_processed, rasi1, star1 = process_and_calculate(column1_data, 10)
    column2_processed, rasi2, star2 = process_and_calculate(column2_data, 10)
    
    st.write("### Data from Home Page")
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
