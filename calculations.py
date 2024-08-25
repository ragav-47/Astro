import streamlit as st
from saps import cal_saps
from streamlit_utils import display_table
Rasi=['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)','கும்பம் (சனி)', 'மீனம் (குரு)']
star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]


def find_Rasi(h):
    part_size = 360 / 12
    x = (h // part_size) %12
    x=int(x)
    st.markdown(f"<p style='font-weight: bold;'> ராசி : {Rasi[x]} </p>", unsafe_allow_html=True)

def calculate_star(h, m, s):
    total_seconds = h * 3600 + m * 60 + s
    part_size = (360 * 3600) / 27
    index = int(total_seconds // part_size) % 27
    index = int(index)
    st.markdown(f"<p style='font-weight: bold;'> நட்சத்திரம் : {star[index]} </p>", unsafe_allow_html=True)


def calculate_time(h, m, s, h1, m1, s1, h2, m2, s2):
    total_seconds = (h + h1 + h2) * 3600 + (m + m1 + m2) * 60 + (s + s1 + s2)
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    total_seconds = total_seconds % 60
    if total_hours > 360:
        total_hours -= 360
    return f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

def calculate_and_display(selected_row_col, column_data, row_names, col_number):

    h1, m1, s1 = map(int, column_data[selected_row_col].split(':'))
    for i in range(len(row_names)):
        h2, m2, s2 = map(int, column_data[i].split(':'))

        # Calculate total time in seconds
        total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)

        # Calculate the output: sum of two values
        total_hours = total_seconds // 3600
        total_minutes = (total_seconds % 3600) // 60
        total_seconds = total_seconds % 60

        result = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

        st.markdown(f"<p style='font-weight: bold;'>Added value for {col_number} ({row_names[selected_row_col]} and {row_names[i]}) - {result}</p>", unsafe_allow_html=True)

        h, m, s = map(int, result.split(':'))
        new_h = h // 2
        m += (h % 2) * 60
        new_m = m // 2
        new_s = m % 2 * 60 + s
        if new_s % 2 != 0:
            new_s += 1
        new_s //= 2
        divided_result = f"{new_h:02}:{new_m:02}:{new_s:02}"

        st.markdown(f"<p style='font-weight: bold;'>Divided by 2 - {divided_result}</p>", unsafe_allow_html=True)
        find_Rasi(new_h)
        calculate_star(new_h, new_m, new_s)
        # st.markdown(f"<p style='font-weight: bold;'>SAPS - {cal_saps(new_h, new_m, new_s,360)}</p>", unsafe_allow_html=True)
        st.write("\n\n\n")

def find_column(h1,m1,s1,column_data,length):
    column=[]
    for i in range(length):
        h2, m2, s2 = map(int, column_data[i].split(':'))

        total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)

        total_hours = total_seconds // 3600
        total_minutes = (total_seconds % 3600) // 60
        total_seconds = total_seconds % 60

        result = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

        h, m, s = map(int, result.split(':'))
        new_h = h // 2
        m += (h % 2) * 60
        new_m = m // 2
        new_s = m % 2 * 60 + s
        if new_s % 2 != 0:
            new_s += 1
        new_s //= 2
        divided_result = f"{new_h:02}:{new_m:02}:{new_s:02}"
        column.append(divided_result)
    return column

def calculate_and_table(selected_row_col, column1_data,column2_data, row_names):
    h1, m1, s1 = map(int, column1_data[selected_row_col].split(':'))
    h2,m2,s2 = map(int, column2_data[selected_row_col].split(':'))
    column1=find_column(h1,m1,s1,column1_data,len(row_names))
    column2=find_column(h2,m2,s2,column2_data,len(row_names))  
    Rasi_1 = []
    for i in range(len(row_names)):
        h, m, s = map(int, column2[i].split(':'))
        part_size = 360 / 12
        x = (h // part_size) % 12
        x = int(x)
        Rasi_1.append(Rasi[x])
    
    star_1 = []
    for i in range(len(row_names)):
        h1, m1, s1 = map(int, column1[i].split(':'))
        h2, m2, s2 = map(int, column2[i].split(':'))

        total_seconds_1 = h1 * 3600 + m1 * 60 + s1
        total_seconds_2 = h2 * 3600 + m2 * 60 + s2

        part_size = (360 * 3600) / 27
        index_1 = int(total_seconds_1 // part_size) % 27
        index_2 = int(total_seconds_2 // part_size) % 27

        # Use a list to store stars for each row
        temp = [star[index_1]]
        if index_1 != index_2:
            temp.append(star[index_2])
        star_1.append(temp)
    # Flatten star_1 for DataFrame creation
    star_1_flat = ["  &  ".join(stars) for stars in star_1]

    
    saps = []
    for i in range(len(row_names)):
        h1, m1, s1 = map(int, column1[i].split(':'))
        h2, m2, s2 = map(int, column2[i].split(':'))
        saps.append(cal_saps(h1, m1, s1,h2, m2, s2,360))
    
    display_table(row_names, column1, column2, Rasi_1, star_1_flat,saps)


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
