import streamlit as st
import pandas as pd
from streamlit_utils import display_table
from saps import cal_saps3
from calculations import process_and_calculate

Rasi=['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)','கும்பம் (சனி)', 'மீனம் (குரு)']
star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]

def process(column_data):
    processed_data=[]
    Rasi_results=[]
    star_results=[]
    for i in range(len(column_data)):
        h,m,s= map(int, column_data[i].split(':'))
        h=(h//30)*3+(h%30)
        if h>36:
            h-=36
        result = f"{h:02}:{m:02}:{s:02}"
        processed_data.append(result)

        part_size = 36 / 12
        x = (h // part_size) %12
        x=int(x)
        Rasi_results.append(Rasi[x])

        total_seconds = h * 3600 + m * 60 + s
        part_size = (36 * 3600) / 27
        index = int(total_seconds // part_size) % 27
        index = int(index)
        star_results.append(star[index])
        
    return processed_data,Rasi_results,star_results

def third():
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
        
        column1_pro, rasi1, star1 = process(column1_processed)
        column2_pro, rasi2, star2 = process(column2_processed)
        
        saps = []
        for i in range(len(row_names)):
            h1, m1, s1 = map(int, column1_pro[i].split(':'))
            h2, m2, s2 = map(int, column2_pro[i].split(':'))
            saps.append(cal_saps3(h1, m1, s1,h2, m2, s2,36))

        Rasi_combined=[]
        for i in range(len(row_names)):
            if rasi1[i] != rasi2[i]:
                Rasi_combined.append(f"{rasi1[i]} & {rasi2[i]}")
            else:
                Rasi_combined.append(rasi1[i])

        stars_combined = []
        for i in range(len(row_names)):
            if star1[i] != star2[i]:
                idx1=star.index(star1[i])
                idx2=star.index(star2[i])
                if (idx2-idx1)==1:
                    stars_combined.append(f"{star1[i]} & {star2[i]}")
                else:
                    stars_combined.append(f"{star1[i]} & {star[idx1+1]} & {star2[i]}")
            else:
                stars_combined.append(star1[i])
        
        display_table(row_names, column1_pro, column2_pro, Rasi_combined, stars_combined,saps)
        # # st.write(column1_data[5])
        # selected_row_col1 = st.selectbox('Select Row', row_names)
        # if st.button('Start Calculation'):
        #     try:
        #         index_1 = row_names.index(selected_row_col1)
        #         if ':' in column1_pro[index_1] and ':' in column2_pro[index_1]:
        #             col1, col2 = st.columns(2)
        #             with col1:
        #                 calculate_and_display(index_1, column1_pro, row_names, col_number=1)
        #             with col2:
        #                 calculate_and_display(index_1, column2_pro, row_names, col_number=2)
        #         else:
        #             st.write("Invalid input format. Please enter valid time values in HH:MM:SS format.")
        #     except ValueError:
        #         st.write("Error: Please enter valid time values in HH:MM:SS format.")
    else:
        st.write("No data available. Please go back to the home page and update the table.")
