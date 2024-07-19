import streamlit as st
Rasi=['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)','கும்பம் (சனி)', 'மீனம் (குரு)']
star = ["அசுவினி","பரணி","கிருத்திகை","ரோகிணி","மிருகசீரிடம்","திருவாதிரை","புனர்பூசம்","பூசம்","ஆயில்யம்","மகம்","பூரம்","உத்திரம்","ஹஸ்தம்","சித்திரை","சுவாதி","விசாகம்","அனுஷம்","கேட்டை","மூலம்","பூராடம்","உத்திராடம்","திருவோணம்","அவிட்டம்","சதயம்","பூரட்டாதி","உத்திரட்டாதி","ரேவதி"]


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
        st.write("\n\n\n")

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
