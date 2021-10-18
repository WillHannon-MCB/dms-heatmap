## DMS-Heatmap 

__author__ : Will Hannon

**`DMS-Heatmap`** is a small prototype application built with [Steamlit](https://streamlit.io/) and [Altair](https://altair-viz.github.io/) for comparing DMS single mutatant experiments between different fixed backgrounds. 

### Running the App

To use this application locally, first clone it from GitHub:
```
git clone https://github.com/WillHannon-MCB/dms-heatmap.git
```

Then, using [`conda`](https://docs.conda.io/en/latest/), make a virtual environment with all the requirements: 
```
conda env create --file environment.yml
conda activate dms-heatmap
```

Finally, run the application using [`Streamlit`](https://streamlit.io/):
```
streamlit run app/app.py
```


