import streamlit as st
import psycopg2
import pandas as pd

# Cache the connection so it doesn't reconnect on every rerun
@st.cache_resource
def get_db_connection():
    # CHANGE THIS to your laptop's IP address if running remotely (e.g., "192.168.1.50")
    db_host = "localhost"
    
    return psycopg2.connect(
        dbname="real_estate_db",
        user="admin",
        password="admin",
        host=db_host,
        port=5432
    )

conn = get_db_connection()
cur = conn.cursor()

# fetch all data form data base
cur.execute("SELECT * FROM real_estate")
data = cur.fetchall()
# select image link
if data:
    image_link = data[0]
    st.write(image_link[60])
    st.markdown(f'''
    <a href="https://google.com">
        <img src="{image_link[60]}" width="300">
    </a>
''', unsafe_allow_html=True)
else:
    print("No data found") # Added print for consistency
    st.write("No data found")



# show all column name from database
column_names = [desc[0] for desc in cur.description]
st.write(column_names)

if data:
    df = pd.DataFrame(data, columns=column_names)
    
    st.header("Price vs Living Area")
    if set(['livingArea', 'price', 'homeType']).issubset(df.columns):
        st.scatter_chart(
            df,
            x='livingArea',
            y='price',
            color='homeType'
        )
    else:
        st.error("Required columns (livingArea, price, homeType) not found in the dataset.")
