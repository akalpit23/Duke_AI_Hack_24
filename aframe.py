import streamlit as st
from openai import OpenAI
import plotly.graph_objects as go
import numpy as np
import json
import pandas as pd

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)

st.title("Plot Generator with OpenAI and Blender")

# Step 1: Upload CSV File
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

df = pd.read_csv(uploaded_file)
st.write("Preview of the data:")
st.write(df.head())


user_input = st.text_input("Enter a description of the plot you want to create:")


def generate_plotly_code(description, df):
    # Extract column names from the DataFrame for context
    column_names = df.columns.tolist()
    columns_info = ", ".join(column_names)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that generates Plotly code based on user descriptions and data.",
            },
            {
                "role": "user",
                "content": (
                    f"Write Python code using Plotly to create the following plot:\n\n"
                    f"{description}\n\n"
                    f"The available data columns are: {columns_info}.\n"
                    f"Ensure the figure is saved as 'fig'."
                ),
            },
        ],
        model="gpt-3.5-turbo",
        max_tokens=500,
        temperature=0,
    )

    code = chat_completion.choices[0].message.content.strip()
    return code


def update_plotly_code(generated_code, adjustment_prompt):
    """
    Update the Plotly code based on the user-provided adjustment prompt.

    Parameters:
    - generated_code (str): The original Plotly code to be modified.
    - adjustment_prompt (str): The user's request for modifications.

    Returns:
    - str: The updated Plotly code.
    """
    # Generate Updated Plot Code
    update_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that modifies Plotly code based on user requests.",
            },
            {
                "role": "user",
                "content": f"Modify the following code to {adjustment_prompt}.\n\n"
                f"Original code:\n{generated_code}",
            },
        ],
        max_tokens=500,
        temperature=0,
    )
    updated_code = update_response.choices[0].message.content.strip()
    return updated_code


if user_input:
    code = generate_plotly_code(user_input, df)
    st.subheader("Generated Plotly Code")
    st.code(code, language="python")
    adjustment_prompt = st.text_input("Tell what changes you want to make to the plot:")
    print(adjustment_prompt)
    updated_code = update_plotly_code(code, adjustment_prompt)
    st.subheader("Updated Plotly Code")
    st.code(updated_code, language="python")
