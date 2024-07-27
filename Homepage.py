# main.py
import streamlit as st
from firebase_utils import initialize_firebase
from firebase_utils import save_data_to_firestore, load_data_from_firestore
from calculations import calculate_time, calculate_and_display,find_Rasi,calculate_star
from streamlit_utils import display_table, edit_table
from saps import cal_saps
import datetime

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

    row_names = ['சூரியன்', 'சந்திரன்', 'செவ்வாய்', 'ராகு', 'குரு', 'சனி', 'புதன்', 'கேது', 'சுக்கிரன்', 'Y', 'YY']
    Rasi = ['மேஷம் (செவ்வாய்)', 'ரிஷபம் (சுக்கிரன்)', 'மிதுனம் (புதன்)', 'கடகம் (சந்திரன்)', 'சிம்மம் (சூரியன்)', 'கன்னி (புதன்)', 'துலாம் (சுக்கிரன்)', 'விருச்சிகம் (செவ்வாய்)', 'தனுசு (குரு)', 'மகரம் (சனி)', 'கும்பம் (சனி)', 'மீனம் (குரு)']
    star = ["அசுவினி (கேது)", "பரணி (சுக்கிரன்)", "கிருத்திகை (சூரியன்)", "ரோகிணி (சந்திரன்)", "மிருகசீரிடம் (செவ்வாய்)", "திருவாதிரை (ராகு)", "புனர்பூசம் (குரு)", "பூசம் (சனி)", "ஆயில்யம் (புதன்)", "மகம் (கேது)", "பூரம் (சுக்கிரன்)", "உத்திரம் (சூரியன்)", "ஹஸ்தம் (சந்திரன்)", "சித்திரை (செவ்வாய்)", "சுவாதி (ராகு)", "விசாகம் (குரு)", "அனுஷம் (சனி)", "கேட்டை (புதன்)", "மூலம் (கேது)", "பூராடம் (சுக்கிரன்)", "உத்திராடம் (சூரியன்)", "திருவோணம் (சந்திரன்)", "அவிட்டம் (செவ்வாய்)", "சதயம் (ராகு)", "பூரட்டாதி (குரு)", "உத்திரட்டாதி (சனி)", "ரேவதி (புதன்)"]

    if selected_saved_date:
        column1_data, column2_data = load_data_from_firestore(db, selected_saved_date)
    else:
        column1_data, column2_data = ['00:00:00'] * len(row_names), ['00:00:00'] * len(row_names)

    column1_data, column2_data = edit_table(row_names, column1_data, column2_data)

    h, m, s = map(int, column1_data[0].split(':'))
    h1, m1, s1 = map(int, column1_data[1].split(':'))
    h2, m2, s2 = map(int, '93:20:00'.split(':'))
    column1_data[9] = calculate_time(h, m, s, h1, m1, s1, h2, m2, s2)

    h, m, s = map(int, column2_data[0].split(':'))
    h1, m1, s1 = map(int, column2_data[1].split(':'))
    h2, m2, s2 = map(int, '93:20:00'.split(':'))
    column2_data[9] = calculate_time(h, m, s, h1, m1, s1, h2, m2, s2)
    
    Rasi_1 = []
    for i in range(len(row_names)):
        h, m, s = map(int, column2_data[i].split(':'))
        part_size = 360 / 12
        x = (h // part_size) % 12
        x = int(x)
        Rasi_1.append(Rasi[x])
    
    star_1 = []
    for i in range(len(row_names)):
        h, m, s = map(int, column2_data[i].split(':'))
        total_seconds = h * 3600 + m * 60 + s
        part_size = (360 * 3600) / 27
        index = int(total_seconds // part_size) % 27
        index = int(index)
        star_1.append(star[index])
    saps = []
    for i in range(len(row_names)):
        h1, m1, s1 = map(int, column1_data[i].split(':'))
        h2, m2, s2 = map(int, column2_data[i].split(':'))
        saps.append(cal_saps(h1, m1, s1,h2, m2, s2))
        
    display_table(row_names, column1_data, column2_data, Rasi_1, star_1,saps)

    # Save data to session_state
    st.session_state['column1_data'] = column1_data
    st.session_state['column2_data'] = column2_data
    st.session_state['row_names'] = row_names
    
    if st.button('Save Data'):
        save_data_to_firestore(db, date_str, column1_data, column2_data)

    selected_row_col1 = st.selectbox('Select Row', row_names)

    if st.button('Start Calculation'):
        try:
            index_1 = row_names.index(selected_row_col1)
            if ':' in column1_data[index_1] and ':' in column2_data[index_1]:
                col1, col2 = st.columns(2)
                with col1:
                    calculate_and_display(index_1, column1_data, row_names, col_number=1)
                with col2:
                    calculate_and_display(index_1, column2_data, row_names, col_number=2)
            else:
                st.write("Invalid input format. Please enter valid time values in HH:MM:SS format.")
        except ValueError:
            st.write("Error: Please enter valid time values in HH:MM:SS format.")

    
