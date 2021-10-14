import altair as alt
import pandas as pd

def plot_heatmap(df, target): 
    """
    Plot a heatmap from the DMS data. 
    """
    plt = alt.Chart(df[df.target == target]).mark_rect().encode(
    x='position:O',
    y='mutant:O',
    color='delta_bind:Q'
    )

    return plt


