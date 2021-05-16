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

def clean(df):
    df = df.swapaxes("index", "columns").dropna(0)
    df['borough'] = df['borough'].replace('NEW YORK',value='MANHATTAN')
    return df

df = clean(original_df)

borough_stats = st.beta_container()
top_bot_5 = st.beta_container()



with borough_stats:

    st.title('Borough Stats')

    st.write(" Number of High Schools ")
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", x=df['borough'],marker_color=['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig)

    st.write('Average Sat Score')
    fig_2 = go.Figure()
    fig_2.add_trace(go.Histogram(histfunc="avg",  x=df['borough'],y=df['tot_sat_score'],marker_color = ['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_2)

    st.write('Average Graduation Rate')
    fig_3 = go.Figure()
    fig_3.add_trace(go.Histogram(histfunc="avg", x=df['borough'],y=df['graduation_rate'],marker_color= ['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_3)

with top_bot_5:

    sat_scores = df.sort_values('tot_sat_score',axis=0,ascending=False)[:5]
    grad_rates = df.sort_values('graduation_rate',axis=0,ascending=False)[:5]
    ars_english = df.sort_values('ars_english',axis=0,ascending=False)[:5]
    ars_algebra = df.sort_values('ars_algebra',axis=0,ascending=False)[:5]

    st.title('Top Five Highest ')

    st.write(" Sat Scores ")
    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="max",x=sat_scores['name'],y=sat_scores['tot_sat_score'],marker_color=['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig)

    st.write(" Graduation Rate % ")
    fig_2 = go.Figure()
    fig_2.add_trace(go.Histogram(histfunc="max", x=grad_rates['name'],y=grad_rates['graduation_rate'],marker_color=['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_2)

    st.write(" Regents: AVG Algebra ")
    fig_3 = go.Figure()
    fig_3.add_trace(go.Histogram(histfunc="max", x=ars_algebra['name'],y=ars_algebra['ars_algebra'],marker_color=['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_3)

    st.write(" Regents: AVG English ")
    fig_4 = go.Figure()
    fig_4.add_trace(go.Histogram(histfunc="max", x=ars_english['name'],y=ars_english['ars_english'],marker_color=['#6600FF','#FF0033','#CCFF00']))
    st.plotly_chart(fig_4)


def find_school(id):
    response = requests.get(f"http://127.0.0.1:5000/schools/{id}")
    return response.json()

school = st.sidebar.slider(min_value = 1, max_value = df.shape[0], step = 1)
school_search = find_school(id=school)