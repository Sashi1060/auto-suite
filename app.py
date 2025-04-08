import streamlit as st
from form import (
    create_a_file,
    add_columns_to_the_excel_file,
    delete_columns_from_excel_file,
    add_question_to_excel,
)
import pandas as pd

st.title("Quiz Excel Manager")

# 🔹 Step 1: User inputs Excel file name
input_file_name = st.text_input("Enter Excel file name:", "quiz.xlsx")

if input_file_name:
    if not input_file_name.endswith(".xlsx"):
        input_file_name += ".xlsx"

    file_path = create_a_file(input_file_name)
    st.success(f"Using file: {file_path.name}")

    # 🔹 Step 2: Column Management
    st.subheader("Manage Excel Columns")

    column_input = st.text_input(
        "Enter column names (excluding S.No):", "Question, OptionA, OptionB, Answer"
    )
    if st.button("Add Columns"):
        columns = [col.strip() for col in column_input.split(",")]
        df = add_columns_to_the_excel_file(file_path, columns)
        st.success("Columns added successfully!")
        st.dataframe(df)

    columns_to_delete = st.text_input("Columns to delete:", "OptionC, Notes")
    if st.button("Delete Columns"):
        col_list = [col.strip() for col in columns_to_delete.split(",")]
        updated_df = delete_columns_from_excel_file(file_path, col_list)
        st.success("Selected columns deleted.")
        st.dataframe(updated_df)

    # 🔹 Step 3: Add Questions
    st.subheader("Add a New Question")

    try:
        df_existing = pd.read_excel(file_path)
        editable_columns = [col for col in df_existing.columns if col != "S.No"]
    except Exception:
        editable_columns = []

    question_data = {}
    for col in editable_columns:
        question_data[col] = st.text_input(f"{col}:")

    if st.button("Add Question"):
        if question_data:
            df_updated = add_question_to_excel(file_path, question_data)
            st.success("Question added with S.No.")
            st.dataframe(df_updated)
        else:
            st.warning("No columns defined to add data.")
