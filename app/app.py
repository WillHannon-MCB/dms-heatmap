import pandas as pd
import itertools
import streamlit as st
from PIL import Image

import utils
import ui

# Set the overall page configuration
icon = Image.open("./images/flavicon.jpeg")
st.set_page_config(layout="wide",
                   page_title="DMS-Heatmap",
                   page_icon=icon)


# Layout the header and about section
header_container = st.container()
with header_container:
    st.title("DMS-Heatmap")
    st.subheader("*Browser-based widget for DMS datasets with multiple backgrounds.*")
    st.markdown("""
        Welcome to `DMS-Heatmap`, the coolest way to analyze DMS data with multiple fixed backgrounds known to humankind :sunglasses:! It's as simple as uploading your data as a `*.csv` file from your computer or a remote repository. Generate heatmaps from each of the static backgrounds in your experiment and compare them using scatterplots. For more detailed instructions, click below.""")
    with st.expander("Instructions", expanded=False):
        # TODO: Add more detailed instructions where the application is mostly finished. 
        st.markdown("Here are some **details** about using the application.")
    st.markdown("---")


# File upload 
with st.sidebar:
    # widget to handle file upload
    uploaded_file = ui.upload_widget()
    if uploaded_file is not None:
        # cached function uploads the data into a pd.DataFrame
        dms_dataframe = utils.load_data(uploaded_file)
    else:
        with header_container:
            st.info("Please input your data from a local or remote repository.")
        st.stop()

# Process and display the data 
st.dataframe(dms_dataframe)
st.stop()

# -- Below is under active development -- ##
# Upload the data 
dataframe = pd.read_csv(uploaded_file, low_memory=False)
# Get the backgrounds
backgrounds = dataframe.target.unique().tolist()
# Selection for optional backgrounds
selection = st.multiselect("Select backgrounds for heatmap:", backgrounds)
# Widgets for scanning the heatmaps -- might be a slow option.. 
minpos = dataframe.position.min()
maxpos = dataframe.position.max()
center = st.sidebar.slider("Select center:", min_value=int(minpos), max_value=int(maxpos), step=1)
window = st.sidebar.slider("Slect window size:", min_value=10, max_value=50, step=2)
# Plot the heatmps 
for background in selection: 
    subset = dataframe[dataframe.target == background]
    subset['wildtype_code'] = (subset[['wildtype', 'mutant']]
                               .apply(lambda x: 'x' if x[0] == x[1] else '', axis=1))
    subset_to_plot = subset.query(f"position > {center-(window/2)} & position <= {center+(window/2)}")

    with st.expander(f"Background: {background}"):
        chart = plot_heatmap(subset_to_plot, "delta_bind")
        st.altair_chart(chart)

# Selection for scatterplots
comparisons = [c for c in itertools.combinations(backgrounds, 2)]
scatter_selection = st.multiselect("Select backgrounds to compare:", 
                                   comparisons,
                                   format_func=lambda comp: f"{comp[0]} vs. {comp[1]}")

pos = st.sidebar.text_input("Position to compare:")
if int(pos) in set(range(minpos, maxpos)):
    for scatterplot in scatter_selection: 
        st.write(f"Comparing {scatterplot[0]} to {scatterplot[1]} at position {pos}")
        scatter_chart = plot_scatter(dataframe, scatterplot[0], scatterplot[1], pos)
        st.altair_chart(scatter_chart)
else:
    st.warning(f"Make sure the position is an integer between {minpos} and {maxpos}.")
    






