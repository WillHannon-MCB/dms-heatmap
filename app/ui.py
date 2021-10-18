import streamlit as st 


def upload_widget():
    """ Widget for uploading a csv file into streamlit.

    This function is a wrapper around a series if streamlit elements.

    Returns
    ----------
    str | None
        URL or PATH to a file that can be read by Pandas.read_csv()

    """
    # Radio button for selecting download location.
    upload_format = st.radio(
        "Where is your data?",
        ("Local Repo", "Remote Repo")
    )

    if upload_format == "Local Repo":
        return st.file_uploader("Choose a local file", type = ["csv"])
    else:
        url = st.text_input("URL path to data")
        if url:
            return url
        else:
            return None
