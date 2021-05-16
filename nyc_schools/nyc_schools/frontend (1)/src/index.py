from urllib.request import urlopen
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
from PIL import Image
import json
import seaborn as sns
from shapely import wkt
import geoplot

API_URL = "http://127.0.0.1:5000/schools"

response = requests.get(API_URL)
details = response.json()  
original_df = pd.DataFrame(details)
st.set_option('deprecation.showPyplotGlobalUse', False)


image = Image.open('/home/royalszachary/Documents/Dev/Python/my_project/test_project/frontend/src/subway.jpg')
st.image(image, caption='NYC SCHOOLS')

def filter_data(df):
    df = df.swapaxes("index", "columns").dropna(0)
    df['borough'] = df['borough'].replace('NEW YORK',value='MANHATTAN')
    df[['lat','lon']] = df['lat_lon'].str.split(',',expand=True)
    df[['lat','lon']] = df[['lat','lon']].apply(pd.to_numeric)
    df[['enrollment','avg_score_sat_math','avg_score_sat_reading_writing','tot_sat_score','graduation_rate']] = df[['enrollment','avg_score_sat_math','avg_score_sat_reading_writing','tot_sat_score','graduation_rate']].astype(float)
    df['borough'] = df['borough'].str.capitalize()
    return df

df = filter_data(original_df)

def merge_data(data=df):
    data = data[(data.tot_sat_score != 0) & (data.graduation_rate != 0)]
    borough_school_size = pd.Series.to_frame(data['borough'].value_counts()).reset_index().rename(columns={'index':'borough','borough':'school_count'})
    borough_average_scores = data.groupby('borough')[['tot_sat_score','graduation_rate']].mean().reset_index()
    nyc = gpd.read_file(gpd.datasets.get_path('nybb'))
    nyc.rename(columns={'BoroName':'borough'}, inplace=True)
    nyc = nyc.merge(borough_school_size,on='borough').merge(borough_average_scores,on='borough')
    return nyc

def borough_stats(y):
    global df
    nyc_data = merge_data(df)
    fig,ax = plt.subplots(1,1, figsize=(10,10))
    nyc_data.plot(column=y, cmap='viridis_r', alpha=.5, ax=ax, legend=True)
    nyc_data.apply(lambda x: ax.annotate(text=x.borough, color='black', xy=x.geometry.centroid.coords[0],ha='center'), axis=1)
    plt.axis('off')
    return st.pyplot()

if st.checkbox('View Borough Statistics'):
    with st.beta_container():

        st.write("Number of High Schools")
        borough_stats(y='school_count')

        st.write('Average Graduation Rate')
        borough_stats(y='graduation_rate')

        st.write('Average SAT Score')
        borough_stats(y='tot_sat_score')



def sort_df(sort_column):
    sorted_df = df.sort_values(sort_column,axis=0,ascending=False)[:5]
    return sorted_df

def top_bot_5(data,x_values,y_values,title,xlabel,ylabel):
    plt.style.use('fivethirtyeight')
    fig, ax1 = plt.subplots(1,1, figsize=(6,6)
                     )
    sns.barplot(x=x_values, y=y_values, data=data, ax=ax1,orient="h")
    ax1.set_title(title, fontsize=15)
    ax1.set_xlabel(xlabel, fontsize=6)
    ax1.set_ylabel(ylabel, fontsize=6)
    ax1.tick_params(axis='both', labelsize=10)
    return st.pyplot()


if st.checkbox('View Top 5 Highest Scores'):
    sat_scores = sort_df('tot_sat_score')
    grad_rates = sort_df('graduation_rate')
    ars_english = sort_df('ars_english')
    ars_algebra = sort_df('ars_algebra')

    st.title('Schools with Top Five Highest SAT Scores ')
    top_bot_5(data=sat_scores,x_values='tot_sat_score',y_values='name',title='Top Sat Scores',xlabel='Schools',ylabel=None)

    st.write("Schools with Highest Graduation Rate % ")
    top_bot_5(data=sat_scores,x_values='graduation_rate',y_values='name',title='Highest Graduation Rates',xlabel='Schools',ylabel=None)

    st.write("Schools with Highest Average Regents Algebra Score  % ")
    top_bot_5(data=sat_scores,x_values='graduation_rate',y_values='name',title='Highest AVG Regents Score',xlabel='Schools',ylabel=None)



#side bar selection
response = st.sidebar.checkbox(f'Would you like to see how compares with other schools?')

if response:
    selected_borough  = st.sidebar.selectbox('Select your borough:', (None,'Manhattan','Brooklyn','Bronx'))
    if selected_borough:
        selected_school = st.sidebar.selectbox('Select your school:', df['name'][df['borough'] == selected_borough])
        if selected_school:
            def compare_selected_school(title,metric='tot_sat_score'):
                values = clean_compute_data(column=metric)
                df = pd.DataFrame(data=values,index=['max_score','average_score',f'{selected_school}','min_score'])
                plt.style.use('fivethirtyeight')
                fig, ax2 = plt.subplots(1,1, figsize=(6,6))
                sns.barplot(x=df.index, y='values', data=df, ax=ax2)
                ax2.set_title(title, fontsize=15)
                ax2.tick_params(axis='both', labelsize=10)
                return st.pyplot()

            def clean_compute_data(data=df, column='tot_sat_score'):
                global selected_school
                data = data[(data[column] != 0)]
                selected_school_score = df.loc[df['name'] == selected_school][column][0]
                return {'values': [data[column].max(), data[column].mean(),selected_school_score,data[column].min()]}

            compare_selected_school(metric='tot_sat_score', title='Comparison of Sat Scores')
            compare_selected_school(metric='graduation_rate', title='Comparison of Graduation Rates')