import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

def main():
    st.title('ASTROLOGY CALCULATION')

    # Define fixed table dimensions
    num_rows = 9
    num_columns = 2

    # Define row names as 9 planets in Tamil
    row_names = ['சூரியன்', 'சந்திரன்', 'செவ்வாய்', 'ராகு', 'குரு', 'சனி','புதன்', 'கேது', 'சுக்கிரன்']

    # Initialize empty lists to store user input data
    column1_data = []
    column2_data = []

    with st.expander("Edit Table"):
        # User input: Input data for each cell in HH:MM:SS format, split into two columns
        col1, col2 = st.columns(2)

        with col1:
            for i in range(num_rows):
                value = st.text_input(f'{row_names[i]}', '00:00:00', key=f'col1_row{i+1}')
                column1_data.append(value)

        with col2:
            for i in range(num_rows):
                value = st.text_input(f'{row_names[i]}', '00:00:00', key=f'col2_row{i+1}')
                column2_data.append(value)

    # Display the table
    st.write('### Table Data')
    df = pd.DataFrame({
        'Column 1': column1_data,
        'Column 2': column2_data
    }, index=row_names)
    st.table(df)

    # Selection after input
    # st.write('### Select Rows for Calculation')
    selected_row_col1 = st.selectbox('Select from Column 1', row_names)
    selected_row_col2 = st.selectbox('Select from Column 2', row_names)

    # Button to start calculation
    # Button to start calculation
    if st.button('Start Calculation'):
        try:
            # Retrieve selected values from columns
            index_1 = row_names.index(selected_row_col1)
            index_2 = row_names.index(selected_row_col2)

            # Perform calculation using selected rows
            if ':' in column1_data[index_1] and ':' in column1_data[index_2] and ':' in column2_data[index_1] and ':' in column2_data[index_2]:
                h1, m1, s1 = map(int, column1_data[index_1].split(':'))
                h2, m2, s2 = map(int, column1_data[index_2].split(':'))
                
                # Calculate total time in seconds
                total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)
                
                # Calculate the first output: sum of two values
                total_hours = total_seconds // 3600
                total_minutes = (total_seconds % 3600) // 60
                total_seconds = total_seconds % 60
                
                first_column = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"
                
                # st.write(f"Added value for ({selected_row_col1} and {selected_row_col2}): {first_output}")
                st.markdown(f"<h3 style='font-weight: bold;'>Added value for 1 ({selected_row_col1} and {selected_row_col2}) - {first_column}</h3>", unsafe_allow_html=True)

                # Calculate the second output: divide first output by 2 from right to left
                # Divide total time by 2 from right to left
                h, m, s = map(int, first_column.split(':'))
                new_h=h//2
                m+=(h%2)*60
                new_m=m//2
                new_s=m%2*60 +s
                if new_s%2!=0:
                    new_s+=1
                new_s//=2
                column_1_div = f"{new_h:02}:{new_m:02}:{new_s:02}"
                
                # st.write(f"Divided by 2: {second_output}")
                st.markdown(f"<h3 style='font-weight: bold;'>Divided by 2 - {column_1_div}</h3>", unsafe_allow_html=True)

                # second_Column
                h1, m1, s1 = map(int, column2_data[index_1].split(':'))
                h2, m2, s2 = map(int, column2_data[index_2].split(':'))
                
                # Calculate total time in seconds
                total_seconds = (h1 + h2) * 3600 + (m1 + m2) * 60 + (s1 + s2)
                
                # Calculate the first output: sum of two values
                total_hours = total_seconds // 3600
                total_minutes = (total_seconds % 3600) // 60
                total_seconds = total_seconds % 60
                
                second_column = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"
                
                # st.write(f"Added value for ({selected_row_col1} and {selected_row_col2}): {first_output}")
                st.markdown(f"<h3 style='font-weight: bold;'>Added value for 2({selected_row_col1} and {selected_row_col2}) - {second_column}</h3>", unsafe_allow_html=True)

                # Calculate the second output: divide first output by 2 from right to left
                # Divide total time by 2 from right to left
                h, m, s = map(int, second_column.split(':'))
                new_h=h//2
                m+=(h%2)*60
                new_m=m//2
                new_s=m%2*60 +s
                if new_s%2!=0:
                    new_s+=1
                new_s//=2
                column_2_div = f"{new_h:02}:{new_m:02}:{new_s:02}"
                
                # st.write(f"Divided by 2: {second_output}")
                st.markdown(f"<h3 style='font-weight: bold;'>Divided by 2 - {column_2_div}</h3>", unsafe_allow_html=True)


            else:
                st.write("Invalid input format. Please enter valid time values in HH:MM:SS format.")

        except ValueError:
            st.write("Error: Please enter valid time values in HH:MM:SS format.")

if __name__ == '__main__':
    main()
