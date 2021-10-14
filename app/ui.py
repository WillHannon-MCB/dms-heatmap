import streamlit as st 
import pandas as pd

def select_target(df):
    """
    Define the menu to select target for the heatmap.
    """
    
    targets = df.target.unique().tolist()

    option = st.sidebar.selectbox("Select a target", targets)

    return option
   
