import streamlit as st
from PIL import Image

import utils
import ui
import plotting

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


# Get the parameters to condifure the heatmaps. 
control_container = st.container()
with control_container: 
    parameters = ui.control_panel_widget(dms_dataframe)


# Plot the heatmaps
for background in parameters['selection']: 
    with st.expander(f"Background: {background}"):
        st.altair_chart(plotting.plot_heatmap(dms_dataframe, 
                                              metric="delta_bind", 
                                              background=background, 
                                              interval_size=parameters['interval_size'], 
                                              center=parameters['center']))
    

# Plot the scatterplots
scatter_selection = ui.scatterplot_panel_widget(parameters['selection'])

if scatter_selection:
    with st.sidebar:
        position = st.number_input("Position to compare", 
                                   min_value=int(dms_dataframe.position.min()), 
                                   max_value=int(dms_dataframe.position.max()),
                                   value=int(dms_dataframe.position.min()))

    # dynamically determines the placement of the scatter plots
    scatter_columns = st.columns(2)
    for i, comparions in enumerate(scatter_selection): 
        if (i + 1) % 2 != 0:
           with scatter_columns[0] : 
               st.altair_chart(plotting.plot_scatter(dms_dataframe,
                                          metric="bind", 
                                          backgrounds=comparions, 
                                          position=position))
        else:
           with scatter_columns[1] : 
               st.altair_chart(plotting.plot_scatter(dms_dataframe,
                                          metric="bind", 
                                          backgrounds=comparions, 
                                          position=position))

else:
    st.stop()












