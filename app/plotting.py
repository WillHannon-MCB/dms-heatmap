import streamlit as st
import altair as alt
import pandas as pd


# Functions 
def plot_heatmap(dataframe, metric, background, interval_size, center):
    """Function to plot altair heatmaps for a given background.

    This funciton takes the main DMS dataframe used as input to the analysis. 
    Then, using the metric to color the plot with, selected background, and window it makes the plot. 

    Parameters
    ----------
    dataframe: pd.DataFrame
        DMS dataframe imported into the analysis from a CSV file. 
    metirc: str
        Name of numeric column used to color the heatmap. 
    background: str
        Name of the target to filter and plot. 
    interval_size: int 
        Integer specifying how large the heatmap should be. 
    center: int 
        Integer specifying the center of the heatmap. 

    Returns
    -------

    alt.Chart 
        Altair chart of the heatmap to be displayed. 
    """

    # Process the dataframe
    subset = dataframe[dataframe.target == background] # background to plot
    subset['wildtype_code'] = (subset[['wildtype', 'mutant']]
                               .apply(lambda x: 'x' if x[0] == x[1] else '', axis=1)) # text for WT cells
    data = subset.query(f"position > {center-(interval_size/2)} & position <= {center+(interval_size/2)}") # section to plot

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
            .properties(height = 350, title = ' '.join(metric.split('_'))))


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
