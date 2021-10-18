import streamlit as st
import pandas as pd


@st.cache()
def load_data(upload_file):
    """Function to load data from csv with pandas and cache.

    This is modularized so that the output can be cached by streamlit. 

    Parameters
    ----------
    upload_file : str
        The file location of the csv (either path or url). 

    Returns
    -------
    pd.DataFrame
        a DataFrame containing tragets, binding, and other DMS data.
    """
    # Upload the data 
    dataframe = pd.read_csv(upload_file, low_memory=False)
    # TODO: check that relevant columns are present. 
    return dataframe
