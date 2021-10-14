import streamlit as st 
import pandas as pd
import numpy as np
import altair as alt


st.markdown("""
    # DMS-Heatmap
    **Prototype!**

    This is an interactive application for analyzing DMS data with multiple backgrounds. It's well suited to looking for epistatic effects. 

""")

upload_format = st.sidebar.radio(
    "Where is your data?",
    ("Local Repo", "Remote Repo")
)

if upload_format == "Local Repo":

    uploaded_file = st.sidebar.file_uploader("Choose a file")
    
    if uploaded_file is not None: 

        dataframe = pd.read(uploaded_file, low_memory = False)
        st.write(dataframe)
 
else:

    upload_url = st.sidebar.text_input("URL to a Remote Repo")
    if upload_url:
        dataframe = pd.read_csv(upload_url, low_memory = False)
        st.write(dataframe)
