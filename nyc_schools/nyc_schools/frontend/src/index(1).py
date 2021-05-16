from urllib.request import urlopen
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://127.0.0.1:5000/schools"


response = requests.get(API_URL)
details = response.json()  
original_df = pd.DataFrame(details)

def filter_data(df):
    df = df.swapaxes("index", "columns").dropna(0)
    df['borough'] = df['borough'].replace('NEW YORK',value='MANHATTAN')
    return df

df = filter_data(original_df)

def borough_stats(y_values=0,func="count",x_values=df['borough'],colors=['#6600FF','#FF0033','#CCFF00']):
    fig = go.Figure()
    if isinstance(y_values, pd.Series):
        fig.add_trace(go.Histogram(histfunc=func, x=x_values,y=y_values,marker_color=colors))
        return st.plotly_chart(fig)
    else:
        fig.add_trace(go.Histogram(histfunc=func, x=x_values,marker_color=colors))
        return st.plotly_chart(fig)

with st.beta_container():

    st.title('Borough Stats')

    st.write(" Number of High Schools ")
    borough_stats()

    st.write('Average Sat Score')
    borough_stats(y_values=df['tot_sat_score'],func='avg')

    st.write('Average Graduation Rate')
    borough_stats(y_values=df['graduation_rate'],func='avg')



def sort_df(sort_column):
    sorted_df = df.sort_values(sort_column,axis=0,ascending=False)[:5]
    return sorted_df

def top_bot_5(y_values,x_values,func="max",colors=['#6600FF','#FF0033','#CCFF00']):
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc=func, x=x_values,y=y_values,marker_color=colors))
    return st.plotly_chart(fig)


with st.beta_container():

    sat_scores = sort_df('tot_sat_score')
    grad_rates = sort_df('graduation_rate')
    ars_english = sort_df('ars_english')
    ars_algebra = sort_df('ars_algebra')

    st.title('Top Five Highest ')

    st.write(" Sat Scores ")
    top_bot_5(x_values=sat_scores['name'],y_values=sat_scores['tot_sat_score'])

    st.write(" Graduation Rate % ")
    top_bot_5(x_values=grad_rates['name'],y_values=grad_rates['graduation_rate'])

    st.write(" Regents: AVG Algebra ")
    top_bot_5(x_values=ars_algebra['name'],y_values=ars_algebra['ars_algebra'])

    st.write(" Regents: AVG English ")
    top_bot_5(x_values=ars_english['name'],y_values=ars_english['ars_english'])



def find_school(id):
    response = requests.get(f"http://127.0.0.1:5000/schools/{id}")
    return response.json()

school = st.sidebar.slider(min_value = 1, max_value = df.shape[0], step = 1,label='schools')
school_search = find_school(id=school)