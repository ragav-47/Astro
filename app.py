import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

st.set_page_config(layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
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
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

# Now you can use Firestore or other Firebase services
db = firestore.client()

# Function to save data to Firestore
def save_data_to_firestore(date_str, column1_data, column2_data):
    try:
        doc_ref = db.collection('saved_data').document(date_str)
        doc_ref.set({
            'column1_data': column1_data,
            'column2_data': column2_data
        })
        st.success(f"Data saved for {date_str}")
    except Exception as e:
        st.error(f"Error saving data to Firestore: {e}")

# Function to load data from Firestore
def load_data_from_firestore(date_str):
    try:
        doc_ref = db.collection('saved_data').document(date_str)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return data['column1_data'], data['column2_data']
        return ['00:00:00'] * 9, ['00:00:00'] * 9
    except Exception as e:
        st.error(f"Error loading data from Firestore: {e}")
        return ['00:00:00'] * 9, ['00:00:00'] * 9

# Main function for Streamlit application
def main():
    # Sidebar for date selection and saved data
    with st.sidebar:
        selected_date = st.date_input("Select a date", format="DD/MM/YYYY")
        date_str = selected_date.strftime("%d %B %Y")

        try:
            saved_files = [doc.id for doc in db.collection('saved_data').stream()]
        except Exception as e:
            st.error(f"Error retrieving saved files: {e}")
            saved_files = []
        
        selected_saved_date = st.selectbox("Load saved data", [""] + saved_files)

    st.title('ASTROLOGY CALCULATION')

    # Define fixed table dimensions
    num_rows = 11
    num_columns = 2

    # Define row names as 9 planets in Tamil
    row_names = ['சூரியன்', 'சந்திரன்', 'செவ்வாய்', 'ராகு', 'குரு', 'சனி', 'புதன்', 'கேது', 'சுக்கிரன்','Y','YY']

    # Load saved data if a date is selected from the sidebar
    if selected_saved_date:
        column1_data, column2_data = load_data_from_firestore(selected_saved_date)
    else:
        column1_data, column2_data = ['00:00:00'] * num_rows, ['00:00:00'] * num_rows

    with st.expander("Edit Table"):
        # User input: Input data for each cell in HH:MM:SS format, split into two columns
        col1, col2 = st.columns(2)

        with col1:
            for i in range(num_rows):
                value = st.text_input(f'{row_names[i]}', column1_data[i], key=f'col1_row{i+1}')
                column1_data[i] = value

        with col2:
            for i in range(num_rows):
                value = st.text_input(f'{row_names[i]}', column2_data[i], key=f'col2_row{i+1}')
                column2_data[i] = value
    h, m, s = map(int, column1_data[0].split(':'))
    h1,m1,s1= map(int, column1_data[1].split(':'))
    h2,m2,s2=map(int,'93:20:00'.split(':'))
    # Calculate total time in seconds
    total_seconds = (h+h1 + h2) * 3600 + (m+m1 + m2) * 60 + (s+s1 + s2)

    # Calculate the Y sum of two values
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    total_seconds = total_seconds % 60
    if total_hours>360:
        total_hours-=360
    column1_data[9] = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

    h, m, s = map(int, column2_data[0].split(':'))
    h1,m1,s1= map(int, column2_data[1].split(':'))
    h2,m2,s2=map(int,'93:20:00'.split(':'))
    # Calculate total time in seconds
    total_seconds = (h+h1 + h2) * 3600 + (m+m1 + m2) * 60 + (s+s1 + s2)

    # Calculate the Y sum of two values
    total_hours = total_seconds // 3600
    total_minutes = (total_seconds % 3600) // 60
    total_seconds = total_seconds % 60
    if total_hours>360:
        total_hours-=360
    column2_data[9] = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"
    # Display the table
    st.write('### Table Data')
    df = pd.DataFrame({
        'Column 1': column1_data,
        'Column 2': column2_data
    }, index=row_names)
    st.table(df)

    # Save button
    if st.button('Save Data'):
        save_data_to_firestore(date_str, column1_data, column2_data)

    # Selection after input
    selected_row_col1 = st.selectbox('Select from Column 1', row_names)

    # Button to start calculation
    if st.button('Start Calculation'):
        try:
            # Retrieve selected values from columns
            index_1 = row_names.index(selected_row_col1)
            col3, col4 = st.columns(2)
            
            if ':' in column1_data[index_1] and ':' in column2_data[index_1]:
                with col3:
                    h1, m1, s1 = map(int, column1_data[index_1].split(':'))
                    for i in range(9):
                        h2, m2, s2 = map(int, column1_data[i].split(':'))

                        # Calculate total time in seconds
                        total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)

                        # Calculate the first output: sum of two values
                        total_hours = total_seconds // 3600
                        total_minutes = (total_seconds % 3600) // 60
                        total_seconds = total_seconds % 60

                        first_column = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                        st.markdown(f"<p style='font-weight: bold;'>Added value for 1 ({selected_row_col1} and {row_names[i]}) - {first_column}</p>", unsafe_allow_html=True)

                        h, m, s = map(int, first_column.split(':'))
                        new_h = h // 2
                        m += (h % 2) * 60
                        new_m = m // 2
                        new_s = m % 2 * 60 + s
                        if new_s % 2 != 0:
                            new_s += 1
                        new_s //= 2
                        column_1_div = f"{new_h:02}:{new_m:02}:{new_s:02}"

                        st.markdown(f"<p style='font-weight: bold;'>Divided by 2 - {column_1_div}</p>", unsafe_allow_html=True)
                        st.write("\n\n\n")

                with col4:
                    h1, m1, s1 = map(int, column2_data[index_1].split(':'))
                    for i in range(9):
                        h2, m2, s2 = map(int, column1_data[i].split(':'))

                        total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)

                        total_hours = total_seconds // 3600
                        total_minutes = (total_seconds % 3600) // 60
                        total_seconds = total_seconds % 60

                        second_column = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                        st.markdown(f"<p style='font-weight: bold;'>Added value for 2 ({selected_row_col1} and {row_names[i]}) - {second_column}</p>", unsafe_allow_html=True)

                        h, m, s = map(int, second_column.split(':'))
                        new_h = h // 2
                        m += (h % 2) * 60
                        new_m = m // 2
                        new_s = m % 2 * 60 + s
                        if new_s % 2 != 0:
                            new_s += 1
                        new_s //= 2
                        column_2_div = f"{new_h:02}:{new_m:02}:{new_s:02}"

                        st.markdown(f"<p style='font-weight: bold;'>Divided by 2 - {column_2_div}</p>", unsafe_allow_html=True)
                        st.write("\n\n\n")
            else:
                st.write("Invalid input format. Please enter valid time values in HH:MM:SS format.")

        except ValueError:
            st.write("Error: Please enter valid time values in HH:MM:SS format.")

if __name__ == '__main__':
    main()
