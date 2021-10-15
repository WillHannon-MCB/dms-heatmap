import pandas as pd
import streamlit as st
import altair as alt

# Functions 
def plot_heatmap(data, metric):

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

    selection = st.multiselect("Select backgrounds to compare:", backgrounds)
    
    for background in selection: 
        subset = dataframe[dataframe.target == background]
        subset['wildtype_code'] = (subset[['wildtype', 'mutant']].apply(lambda x: 'x' if x[0] == x[1] else '', axis=1))

        with st.expander(f"Background: {background}"):
            chart = plot_heatmap(subset, "delta_bind")
            st.altair_chart(chart)

else: 
    st.info("Please input your data from a local or remote repository.")



