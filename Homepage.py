# main.py
import streamlit as st
from firebase_utils import initialize_firebase
from firebase_utils import save_data_to_firestore, load_data_from_firestore
from calculations import calculate_time, calculate_and_table
from streamlit_utils import display_table, edit_table
from saps import cal_saps
import datetime
import pandas as pd

# Load Firebase credentials from Streamlit secrets
firebase_creds = {
    "type": st.secrets["TYPE"],
    "project_id": st.secrets["PROJECT_ID"],
    "private_key_id": st.secrets["PRIVATE_KEY_ID"],
    "private_key": st.secrets["PRIVATE_KEY"].replace("\\n", "\n"),
    "client_email": st.secrets["CLIENT_EMAIL"],
    "client_id": st.secrets["CLIENT_ID"],
    "auth_uri": st.secrets["AUTH_URI"],
    "token_uri": st.secrets["TOKEN_URI"],
    "auth_provider_x509_cert_url": st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
    "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"],
}

# Initialize the Firebase app with the credentials
db = initialize_firebase(firebase_creds)
row_names = ['சூரியன்', 'சந்திரன்', 'செவ்வாய்', 'ராகு', 'குரு', 'சனி', 'புதன்', 'கேது', 'சுக்கிரன்', 'Y', 'YY']
Rasi = ['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)', 'கும்பம் (சனி)', 'மீனம் (குரு)']
star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]

def cal_div(column1,column2):
    h1, m1, s1 = map(int, column1.split(':'))
    h2,m2,s2 = map(int, column2.split(':'))
    total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)

    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    total_seconds = total_seconds % 60

    result = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

    h, m, s = map(int, result.split(':'))
    if h>360:
        h-=360
    new_h = h // 2
    m += (h % 2) * 60
    new_m = m // 2
    new_s = m % 2 * 60 + s
    if new_s % 2 != 0:
        new_s += 1
    new_s //= 2
    divided_result = f"{new_h:02}:{new_m:02}:{new_s:02}"
    return divided_result
# def calculate_company(number,selected_company,column1_data,column2_data):
#     if number>10:
#         num1,num2=number//10,number%10
#         column1 = cal_div(column1_data[num1-1],column1_data[num2-1])
#         column2 = cal_div(column2_data[num1-1],column2_data[num2-1])
#     else:
#         column1 = column1_data[number-1]
#         column2 = column2_data[number-1]
    
#     Rasi_1 = []
#     h, m, s = map(int, column2.split(':'))
#     part_size = 360 / 12
#     x = (h // part_size) % 12
#     x = int(x)
#     Rasi_1.append(Rasi[x])
    
#     star_1 = []
#     h1, m1, s1 = map(int, column1.split(':'))
#     h2, m2, s2 = map(int, column2.split(':'))

#     total_seconds_1 = h1 * 3600 + m1 * 60 + s1
#     total_seconds_2 = h2 * 3600 + m2 * 60 + s2

#     part_size = (360 * 3600) / 27
#     index_1 = int(total_seconds_1 // part_size) % 27
#     index_2 = int(total_seconds_2 // part_size) % 27

#     # Use a list to store stars for each row
#     temp = [star[index_1]]
#     if index_1 != index_2:
#         temp.append(star[index_2])
#     star_1.append(temp)
#     # Flatten star_1 for DataFrame creation
#     star_1_flat = ["  &  ".join(stars) for stars in star_1]
    
#     saps = []
#     h1, m1, s1 = map(int, column1.split(':'))
#     h2, m2, s2 = map(int, column2.split(':'))
#     saps.append(cal_saps(h1, m1, s1,h2, m2, s2,360))
#     formatted_saps = [' , '.join(sublist) for sublist in saps]
    
#     df = pd.DataFrame({
#         'Column 1': column1,
#         'Column 2': column2,
#         'ராசி': Rasi_1,
#         'நட்சத்திரம்': star_1_flat,
#         'சப்ஸ்': formatted_saps,
#     }, index=[selected_company])
    
#     # Display the DataFrame as a table
#     st.table(df)
def calculate_companies(column1_data, column2_data,company):
    results = []

    for selected_company,number in company.items():
        
        if number > 10:
            num1, num2 = number // 10, number % 10
            column1 = cal_div(column1_data[num1-1], column1_data[num2-1])
            column2 = cal_div(column2_data[num1-1], column2_data[num2-1])
        else:
            column1 = column1_data[number-1]
            column2 = column2_data[number-1]

        Rasi_1 = []
        h, m, s = map(int, column2.split(':'))
        part_size = 360 / 12
        x = (h // part_size) % 12
        x = int(x)
        Rasi_1.append(Rasi[x])

        star_1 = []
        h1, m1, s1 = map(int, column1.split(':'))
        h2, m2, s2 = map(int, column2.split(':'))

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
        h1, m1, s1 = map(int, column1.split(':'))
        h2, m2, s2 = map(int, column2.split(':'))
        saps.append(cal_saps(h1, m1, s1, h2, m2, s2, 360))
        formatted_saps = [' , '.join(sublist) for sublist in saps]

        results.append({
            'Company': selected_company,
            'Column 1': column1,
            'Column 2': column2,
            'ராசி': Rasi_1,
            'நட்சத்திரம்': star_1_flat,
            'சப்ஸ்': formatted_saps,
        })
    
    return results
def Home():
    
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("Select a date", format="DD/MM/YYYY")
        date_str = selected_date.strftime("%d %B %Y")
        st.session_state.selected_date = selected_date
    with col2:
        if 'selected_date' in st.session_state:
            selected_date = st.session_state.selected_date
            selected_day = selected_date.strftime("%A")
        else:
            selected_day = "No date selected"
        st.markdown(
            f"""
            <div style="padding: 5px; border: 1px solid #d3d3d3; border-radius: 5px; background-color: #f9f9f9; margin-top: 29px;">
                <div style="font-size: 16px; color: #333;font-weight: bold">{selected_day}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    try:
        saved_files = [doc.id for doc in db.collection('saved_data').stream()]
    except Exception as e:
        st.error(f"Error retrieving saved files: {e}")
        saved_files = []

    if date_str in saved_files:
        selected_saved_date = date_str
    else:
        selected_saved_date = ""

    if selected_saved_date:
        column1_data, column2_data = load_data_from_firestore(db, selected_saved_date)
    else:
        column1_data, column2_data = ['00:00:00'] * len(row_names), ['00:00:00'] * len(row_names)

    column1_data, column2_data = edit_table(row_names, column1_data, column2_data)
    
    # Y calculation
    h, m, s = map(int, column1_data[0].split(':'))
    h1, m1, s1 = map(int, column1_data[1].split(':'))
    h2, m2, s2 = map(int, '93:20:00'.split(':'))
    column1_data[9] = calculate_time(h, m, s, h1, m1, s1, h2, m2, s2)

    h, m, s = map(int, column2_data[0].split(':'))
    h1, m1, s1 = map(int, column2_data[1].split(':'))
    h2, m2, s2 = map(int, '93:20:00'.split(':'))
    column2_data[9] = calculate_time(h, m, s, h1, m1, s1, h2, m2, s2)
    # YY Calculation
    
    Rasi_1 = []
    for i in range(len(row_names)):
        h, m, s = map(int, column2_data[i].split(':'))
        part_size = 360 / 12
        x = (h // part_size) % 12
        x = int(x)
        Rasi_1.append(Rasi[x])
    
    star_1 = []
    for i in range(len(row_names)):
        h1, m1, s1 = map(int, column1_data[i].split(':'))
        h2, m2, s2 = map(int, column2_data[i].split(':'))

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
        h1, m1, s1 = map(int, column1_data[i].split(':'))
        h2, m2, s2 = map(int, column2_data[i].split(':'))
        saps.append(cal_saps(h1, m1, s1,h2, m2, s2,360))
    
    display_table(row_names, column1_data, column2_data, Rasi_1, star_1_flat,saps)

    # Save data to session_state
    st.session_state['column1_data'] = column1_data
    st.session_state['column2_data'] = column2_data
    st.session_state['row_names'] = row_names
    
    if st.button('Save Data'):
        save_data_to_firestore(db, date_str, column1_data, column2_data)
    
    company={
        "ACC": 1,
        "TITAN" : 1,
        "ONGC" : 1,
        "L&T":1,
        "BAJAJ FINANCE": 12,
        "DR.REDDY'S":12,
        "EICHER MOTORS":12,"M&M":12,"HCL":12,"NESTLE":12,"SUN PHARMA":12,"SOUTH INDIAN BANK":12,
        "TATA consumer":15,"WIPRO":15,"TRENT":15,
        "HDFC BANK":14,"LT MIND TREE":14,
        "ASIAN PAINTS":17,"MARUTI":17,"RIL":17,
        "HERO":19,"INFOSYS":19,"TATA STEELS":19,
        "TATA ELXI":18,"TATA MOTORS":18,"JSW STEEL":18,
        "AXIS BANK":16,"KOTAK BANK":16,
        "ICICI BANK":2,"CHIPLA":2,"TATA COMMUNICATIONS":2,
        "BAJAJ AUTO":5,
        "BAJAJ FINSERV":54,
        "POWER GRID":57,
        "APOLLO HOSPITAL":59,
        "BHARATI AIRTEL":25,"KARNATAKA BANK":25,"TATA TECHNOLOGIES":25,
        "ITC":27,"NTPL":27,
        "HUL":29,"INDUSIND BANK":29,"ULTRA CEMENTS":29,
        "TECH MAHINDRA":28,
        "SBI BANK":3,"TATA POWER":3,
        "GRASSIM":6
        }
    # Calculate for all companies
    results = calculate_companies(column1_data, column2_data,company)

    # Display the results in a DataFrame
    if results:
        df = pd.DataFrame(results)
        df.index = range(1,len(df)+1)
        df.index.name = 'S.No'
        st.table(df)


    # selected_company = st.selectbox('Select Row', company.keys())

    # # if st.button('Start Calculation'):
    # #     try:
    # #         index_1 = row_names.index(selected_row_col1)
    # #         if ':' in column1_data[index_1] and ':' in column2_data[index_1]:
    # #             # calculate_and_table(index_1,column1_data,column2_data,row_names)
    # #             calculate_company()
    # #         else:
    # #             st.write("Invalid input format. Please enter valid time values in HH:MM:SS format.")
    # #     except ValueError:
    # #         st.write("Error: Please enter valid time values in HH:MM:SS format.")
    # if st.button('Start Calculation'):
    #     calculate_company(company[selected_company],selected_company,column1_data,column2_data)
    #     # try:
    #     #     calculate_company(company[selected_company],selected_company,column1_data,column2_data)
    #     # except ValueError:
        #     st.write("Error: Please enter valid time values in HH:MM:SS format.")

