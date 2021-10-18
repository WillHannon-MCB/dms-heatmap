import streamlit as st 
import itertools


def upload_widget():
    """ Widget for uploading a csv file into streamlit.

    This function is a wrapper around a series if streamlit elements.

    Returns
    -------
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


# TODO: Possibly move the scrolling widgets to the sidebar. 
def control_panel_widget(dataframe):
    """ Widget for configuring the heatmaps.

    This function is a wrapper around a handful of streamlit elements. 
    It determines the heatamps to look at as well as the center and size of those heatmaps. 

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataframe containing the DMS data from load_data()

    Returns 
    -------
    dict
       Containing the list of backgrounds, center, and window size 
    """
    # Multiselection of backgrounds 
    backgrounds = dataframe.target.unique().tolist()
    selection = st.multiselect("Select backgrounds for heatmap:", backgrounds)

    # Widgets for scanning the heatmaps   
    minpos = int(dataframe.position.min())
    maxpos = int(dataframe.position.max())
    # split into two columns below the main selection
    col1, col2, col3 = st.columns((3,1,3))
    with col1:
        center = st.slider("Select heatmap center:", min_value=minpos, max_value=maxpos, step=1)
    with col3:
        interval_size = st.slider("Select heatmap interval size:", min_value=10, max_value=50, step=2)

    return {
        'selection': selection,
        'center': center, 
        'interval_size': interval_size
    }


def scatterplot_panel_widget(backgrounds):
    """Widget for multiselect of scatter plot comparisons.

    Parameters
    ----------
    backgrounds: list
        A list of the backgrounds

    Returns
    -------
    list
        A list of the comparisons to make
    """
    # All possible non-redundant combinations of backgrounds.    
    comparisons = [c for c in itertools.combinations(backgrounds, 2)]

    return st.multiselect("Select backgrounds for scatterplots:", 
                          comparisons, 
                          format_func=lambda comp: f"{comp[0]} vs. {comp[1]}")
