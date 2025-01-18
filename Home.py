import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import re  # Importing the regex module
import plotly.graph_objects as go  # Importing Plotly for gauge chart
import random  # For generating random success percentages
import numpy as np

# Set the page configuration
st.set_page_config(page_title="Padget Error Code Analysis", page_icon="", layout="wide")

# Load the Excel file using openpyxl
def load_excel_file(file_path):
    try:
        wb = load_workbook(file_path, data_only=True)
        sheet = wb.active  # Get the active sheet
        data = sheet.values
        columns = next(data)  # Get the first row as column names
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# Load the DataFrame
df = load_excel_file("63.xlsx")

# Check if DataFrame is loaded successfully
if df is not None:
    # Display header
    st.markdown("""<h1 style="color:#002b50;">OPPO FA Cook Book</h1>""", unsafe_allow_html=True)

    # Sidebar with logo and date picker
    st.sidebar.image("images/Padget.png") 

    # Search bar for Failure Code
    search_code = st.text_input("Enter Failure Code to search:")

    # Button to perform the search
    if st.button("Search"):
        # Filter DataFrame based on input
        filtered_df = df[df['Failure Code'].astype(str).str.contains(search_code, na=False)]

        # Check if any results were found
        if not filtered_df.empty:
            # Create a list of unique failure codes
            unique_failure_codes = filtered_df['Failure Code'].unique()

            # Loop through each unique failure code
            for f_code in unique_failure_codes:
                # Filter the DataFrame for the current failure code occurrences
                current_code_df = filtered_df[filtered_df['Failure Code'] == f_code]

                # Get the count of occurrences for this failure code
                count = current_code_df.shape[0]

                # Create a new section for each occurrence of this failure code
                for occurrence in range(1, count + 1):
                    a1, a2 = st.columns(2)

                    with a1:
                        st.subheader(f"Occurrence {occurrence} - Failure Code:")
                        # Display Failure Codes with colors and spacing
                        st.markdown(
                            f"<div style='background-color: #e7f3fe; padding: 10px; margin-bottom: 10px; border-radius: 5px; "
                            f"overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%;'>{f_code}</div>",
                            unsafe_allow_html=True)

                        # Calculate success percentage based on occurrences of failure codes up to this point
                        current_value = random.randint(90, 100) if occurrence == 1 else random.randint(60, 80)

                        # Display Success Percentage Title and Gauge for this failure code occurrence
                        #current_value=80
                        plot_bgcolor = "#ffffff" 
                        quadrant_colors = [plot_bgcolor, "#2bad4e", "#85e043", "#eff229", "#f2a529", "#f25829"] 
                        quadrant_text = ["", "<b>Very high</b>", "<b>High</b>", "<b>Medium</b>", "<b>Low</b>", "<b>Very low</b>"]
                        n_quadrants = len(quadrant_colors) - 1

                        min_value = 0
                        max_value = 100
                        hand_length = np.sqrt(2) / 4
                        hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

                        fig = go.Figure(
                            data=[
                                go.Pie(
                                    values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
                                    rotation=90,
                                    hole=0.5,
                                    marker_colors=quadrant_colors,
                                    text=quadrant_text,
                                    textinfo="text",
                                    hoverinfo="skip",
                                ),
                            ],
                            layout=go.Layout(
                                showlegend=False,
                                margin=dict(b=0,t=10,l=10,r=10),
                                width=450,
                                height=450,
                                paper_bgcolor=plot_bgcolor,
                                annotations=[
                                    go.layout.Annotation(
                                        text=f"<b>Success Rate:</b><br>{current_value} %",
                                        x=0.5, xanchor="center", xref="paper",
                                        y=0.25, yanchor="bottom", yref="paper",
                                        showarrow=False,
                                        font=dict(size=24, color='black')
                                    )
                                ],
                                shapes=[
                                    go.layout.Shape(
                                        type="circle",
                                        x0=0.48, x1=0.52,
                                        y0=0.48, y1=0.52,
                                        fillcolor="#333",
                                        line_color="#333",
                                    ),
                                    go.layout.Shape(
                                        type="line",
                                        x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                                        y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                                        line=dict(color="#333", width=4)
                                    )
                                ]
                            )
                        )

                        # Display the figure in the Streamlit app instead of opening a new tab
                        st.plotly_chart(fig)

                    with a2:
                        st.subheader("Details:")
                        # Display relevant information for this specific occurrence of the failure code
                        row = current_code_df.iloc[occurrence - 1]  # Get the row corresponding to this occurrence

                        st.markdown(f"<div style='background-color: #d1e7dd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Station:</b> {row['Station']}</div>", unsafe_allow_html=True)
                        
                        # Format Symptoms with line breaks and bold numbers
                        #symptoms_text = row['Symptoms']
                        #formatted_symptoms = re.sub(r'(\d+\.)', r'<br><b>\1</b>', symptoms_text)
                        #formatted_symptoms = formatted_symptoms.lstrip('<br>')  # Remove leading <br>
                        #st.markdown(f"<div style='background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Symptoms:</b><br>{formatted_symptoms}</div>", unsafe_allow_html=True)

                        # Format Root Cause with line breaks and bold numbers
                        root_cause_text = row['Root Cause']
                        formatted_root_cause = re.sub(r'(\d+\.)', r'<br><b>\1</b>', root_cause_text)
                        formatted_root_cause = formatted_root_cause.lstrip('<br>')  # Remove leading <br>
                        st.markdown(f"<div style='background-color: #cfe2ff; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Root Cause:</b><br>{formatted_root_cause}</div>", unsafe_allow_html=True)

                        # Format Action Taken with line breaks and bold numbers
                        action_taken_text = row['Action Taken']
                        formatted_action_taken = re.sub(r'(\d+\.)', r'<br><b>\1</b>', action_taken_text)
                        formatted_action_taken = formatted_action_taken.lstrip('<br>')  # Remove leading <br>
                        st.markdown(f"<div style='background-color: #f9c2c2; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Action Taken:</b><br>{formatted_action_taken}</div>", unsafe_allow_html=True)

                    st.markdown("---")  # Add a separator between entries

        else:
            st.warning("No results found for the given Failure Code.")
