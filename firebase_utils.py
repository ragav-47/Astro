import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def initialize_firebase(firebase_creds):
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def save_data_to_firestore(db, date_str, column1_data, column2_data):
    try:
        doc_ref = db.collection('saved_data').document(date_str)
        doc_ref.set({
            'column1_data': column1_data,
            'column2_data': column2_data
        })
        st.success(f"Data saved for {date_str}")
    except Exception as e:
        st.error(f"Error saving data to Firestore: {e}")

def load_data_from_firestore(db, date_str):
    try:
        doc_ref = db.collection('saved_data').document(date_str)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            return data['column1_data'], data['column2_data']
        return ['00:00:00'] * 11, ['00:00:00'] * 11
    except Exception as e:
        st.error(f"Error loading data from Firestore: {e}")
        return ['00:00:00'] * 11, ['00:00:00'] * 11
