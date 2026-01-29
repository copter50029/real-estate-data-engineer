import streamlit as st
import psycopg2
import pandas as pd

# Cache the connection so it doesn't reconnect on every rerun
@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        dbname="real_estate_db",
        user="admin",
        password="admin",
        host="localhost",
        port=5432
    )

conn = get_db_connection()
cur = conn.cursor()

# fetch all data form data base
cur.execute("SELECT * FROM real_estate")
st.write(cur)



# show all column name from database
# column_names = [desc[0] for desc in cur.description]
# st.write(column_names)

