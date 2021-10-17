import pandas as pd
import itertools
import streamlit as st
import altair as alt
from PIL import Image

# Set the overall page configuration
icon = Image.open("./images/flavicon.jpeg")
st.set_page_config(layout="wide",
                   page_title="DMS-Heatmap",
                   page_icon=icon)
# Functions 
def plot_heatmap(data, metric):
    """
    Plot interactive heatmaps with Altair
    """

    # Select the cell in the heatmap
    cell_selector = alt.selection_single(on='mouseover',
                                         empty='none')

    
    # Default order of the y-axis
    aa_order = ['R', 'K', 'H', 'D', 'E', 'Q', 'N', 'S', 'T', 'Y',
                'W', 'F', 'A', 'I', 'L', 'M', 'V', 'G', 'P', 'C']
    
    # Tooltips
    tooltips = ['mutation', 'n_bc_bind', 'bind']
    

    # Base for the heatmap
    base = (alt.Chart(data)
            .encode(x=alt.X('position:O',
                             axis=alt.Axis(titleFontSize=15)),
                    y=alt.Y('mutant:O',
                            sort=aa_order,
                            axis=alt.Axis(labelFontSize=12,
                                          titleFontSize=15))
                   )
           )
    
    # Fill in the heatmap with color by `metric`
    heatmap = (base
               .mark_rect()
               .encode(color = alt.Color(metric,
                                       type = 'quantitative', 
                                       scale = alt.Scale(scheme = 'redblue',
                                                       domain = [data[metric].min(),
                                                                 data[metric].max()],
                                                       domainMid = 0),
                                       legend = alt.Legend(orient = 'left',
                                                           title = 'grey is n.d.',
                                                           gradientLength = 100)),
                       stroke = alt.value('black'),
                       strokeWidth = alt.condition(cell_selector,
                                                   alt.value(2),
                                                   alt.value(0)),
                       tooltip = tooltips
                      )
              )
    
    # Add the X to the wildtype cells
    wildtype = (base
                .mark_text(color='black')
                .encode(text=alt.Text('wildtype_code:N')
                       )
               )
    
    # Add grey to the empty cells
    nulls = (base
             .mark_rect()
             .transform_filter(f"!isValid(datum.{metric})")
             .mark_rect(opacity = 0.5)
             .encode(alt.Color(f'{metric}:N',
                               scale = alt.Scale(scheme = 'greys'),
                               legend = None)
                    )
            )
    
    return ((heatmap + nulls + wildtype)
            .interactive()
            .add_selection(cell_selector)  # mouse over highlighting
            .properties(height = 250, title = ' '.join(metric.split('_'))))


def plot_scatter(df, bkgr_1, bkgr_2, position): 
    """
    Plot interactive scatter plots of binding affinity.
    """
    
    # Subset df by first background 
    bkgr_1_df = df[df.target == bkgr_1][["mutant", "position", "bind"]].rename(
    columns = {"bind" : f"{bkgr_1}_binding"}
    )
    
    # Subset df by second background
    bkgr_2_df = df[df.target == bkgr_2][["mutant", "position", "bind"]].rename(
    columns = {"bind" : f"{bkgr_2}_binding"}
    )
    
    # Merge to make the df for plotting
    plot_df = pd.merge(bkgr_1_df, bkgr_2_df, on=["mutant", "position"]).rename(
    columns = {"mutant" : "Residue"}
    )

    # Make the interactive chart 
    return alt.Chart(plot_df[plot_df.position == 500]).mark_circle(size=60).encode(
    x=f"{bkgr_1}_binding",
    y=f"{bkgr_2}_binding",
    tooltip=['Residue']
    ).interactive()
     

# Page Header 
st.title("DMS-Heatmap")
st.subheader("Browser-based widget for DMS datasets with multiple backgrounds.")

# Handle file uploading
with st.sidebar: 

    upload_format = st.radio(
        "Where is your data?",
        ("Local Repo", "Remote Repo")
    )

    if upload_format == "Local Repo":
        uploaded_file = st.file_uploader("Choose a local file", type = ["csv"])
    else:
        url = st.text_input("URL path to data")
        if url:
            uploaded_file = url
        else:
            uploaded_file = None

# If the data is imported, run the app. 
if uploaded_file is not None:
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
        




else: 
    st.info("Please input your data from a local or remote repository.")



