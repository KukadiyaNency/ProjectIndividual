import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.subplots as sp
import pandas as pd

st.set_page_config(page_title='Health Analysis', page_icon='bar_chart:', layout='wide')

st.write("Hello!")
st.title(" :bar_chart: Health Analysis")

dframe = pd.read_csv('Health.csv')

st.write("You can select, whichever categories you want to explore further!")
waste_categories = st.multiselect('Select waste categories:', dframe.columns[2:])
st.write("You can select, whichever year you want to explore further!")
years = st.multiselect('Select years:', dframe['Year'].unique())
st.write("You can select, whichever country you want to explore further!")
countries = st.multiselect('Select countries:', dframe['COUNTRIES'].unique())
st.write("You can select, whichever chart type you want to explore further!")
chart_type = st.selectbox('Select chart type:', ['Bar chart', 'Line chart'])

filtered_data = dframe[(dframe['Year'].isin(years)) & (dframe['COUNTRIES'].isin(countries)) & (dframe[waste_categories].sum(axis=1) > 0)]

if chart_type == 'Bar chart':
    fig = px.bar(filtered_data, x='Year', y=waste_categories, color='COUNTRIES')
elif chart_type == 'Line chart':
    fig = px.line(filtered_data, x='Year', y=waste_categories, color='COUNTRIES')

fig.update_traces(hovertemplate='Country: <br>Waste category: %{y}<br>Year: %{x}')

st.plotly_chart(fig)
if st.checkbox('Show timeseries analysis'):
    st.markdown('### Timeseries analysis')
    timeseries_data = filtered_data.melt(id_vars=['COUNTRIES', 'Year'], var_name='waste_category', value_name='generation')
    fig = px.line(timeseries_data, x='Year', y='generation', color='COUNTRIES', line_group='waste_category')
    st.plotly_chart(fig)

if st.checkbox('Additional Visualizations'):
    st.subheader('Box Plots for Distribution Analysis')
    boxplot_fig = px.box(timeseries_data, x='waste_category', y='generation', color='COUNTRIES',
                         title='Box Plot of Waste Generation Distribution by Waste Category',
                         labels={'generation': 'Waste Generation', 'waste_category': 'Waste Category'})
    st.plotly_chart(boxplot_fig)

    st.subheader('Pie Chart for Percentage Contribution')
    pie_chart_fig = px.pie(filtered_data, names='COUNTRIES', values=waste_categories[0], title='Percentage Contribution of Countries to Waste Generation')
    st.plotly_chart(pie_chart_fig)





