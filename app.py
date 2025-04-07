from dotenv import load_dotenv
load_dotenv()  ## load all envirement variable

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure our api key

genai.configure(api_key= os.getenv("Google_api_key"))
# genai.configure(api_key="AIzaSyA_N4VwkboW9ZO7NU85I26pG2sE7lvGKvw")


## Function to load googlr gemini model and provide sql query as response
## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-1.5-pro-latest')
    response=model.generate_content([prompt[0],question])
    return response.text

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Streamlit App

st.set_page_config(page_title="Created By Nitish!")
st.header("Natural Language to SQL-QUERY")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
# if submit:
#     response=get_gemini_response(question,prompt)
#     print(response)
#     response=read_sql_query(response,"student.db")
#     st.subheader("The Response is")
#     for row in response:
#         print(row)
#         st.header(row)

if submit:
    while True:
        response = get_gemini_response(question, prompt)
        if response:
            response = response.replace('```', '')

            import pandas as pd
            import sqlite3 as sql
            conn = sql.connect("student.db")
            
            try:
                response_df = pd.read_sql_query(response, conn)
                st.subheader("Enjoy your Query:")
                st.write(response)
                st.subheader("Result")
                st.write(response_df)
                break  
            except Exception as e:
                print("Error:", e)
                continue 
