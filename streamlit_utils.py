import streamlit as st
import pandas as pd


def display_table(row_names, column1_data, column2_data, Rasi, star, saps):
    formatted_saps = [' , '.join(sublist) for sublist in saps]
    
    df = pd.DataFrame({
        'Column 1': column1_data,
        'Column 2': column2_data,
        'ராசி': Rasi,
        'நட்சத்திரம்': star,
        'சப்ஸ்': formatted_saps,
    }, index=row_names)
    
    # Display the DataFrame as a table
    st.table(df)

def edit_table(row_names, column1_data, column2_data):
    with st.expander("Edit Table"):
        col1, col2 = st.columns(2)
        with col1:
            for i in range(len(row_names)):
                value = st.text_input(f'{row_names[i]}', column1_data[i], key=f'col1_row{i+1}')
                column1_data[i] = value
        with col2:
            for i in range(len(row_names)):
                value = st.text_input(f'{row_names[i]}', column2_data[i], key=f'col2_row{i+1}')
                column2_data[i] = value
    return column1_data, column2_data
