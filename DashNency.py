import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.subplots as sp
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
st.set_page_config(page_title='Health Analysis', page_icon='bar_chart:', layout='wide')

st.write("Hello!")
st.title(" :bar_chart: Health Analysis")

dframe = pd.read_csv('Health.csv')

waste_categories = st.multiselect('Select waste categories:', dframe.columns[2:])
years = st.multiselect('Select years:', dframe['Year'].unique())
countries = st.multiselect('Select countries:', dframe['COUNTRIES'].unique())

chart_type = st.selectbox('Select chart type:', ['Bar chart', 'Line chart'])

filtered_data = dframe[(dframe['Year'].isin(years)) & (dframe['COUNTRIES'].isin(countries)) & (dframe[waste_categories].sum(axis=1) > 0)]

if chart_type == 'Bar chart':
    fig = px.bar(filtered_data, x='Year', y=waste_categories, color='COUNTRIES')
elif chart_type == 'Line chart':
    fig = px.line(filtered_data, x='Year', y=waste_categories, color='COUNTRIES')

fig.update_traces(hovertemplate='Country: %{x}<br>Waste category: %{y}<br>Year: %{text}')
st.plotly_chart(fig)
if st.checkbox('Show timeseries analysis'):
    st.markdown('### Timeseries analysis')
    timeseries_data = filtered_data.melt(id_vars=['COUNTRIES', 'Year'], var_name='waste_category', value_name='generation')
    fig = px.line(timeseries_data, x='Year', y='generation', color='COUNTRIES', line_group='waste_category')
    st.plotly_chart(fig)



