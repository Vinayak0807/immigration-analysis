
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_icon="🧊",
    page_title="Immigration Data Analysis",
    layout="wide")

years = list(range(1980, 2014))

@st.cache_data()
def load_data():
    df = pd.read_excel('Canada.xlsx', sheet_name=1, skiprows=20, skipfooter=2) 
    # add a column
    df['Total'] = df[years].sum(axis=1)
    # remove unnecessary columns
    cols_to_drop = ['AREA', 'REG', 'DEV', 'Type', 'Coverage',]
    df.drop(columns=cols_to_drop, inplace=True)
    # rename columns
    df.rename(columns={
        'OdName': 'Country',
        'AreaName': 'Continent',
        'RegName': 'Region',
        'DevName':'Status',
    }, inplace=True)
    # sort values by total
    df.sort_values(by='Total', ascending=False, inplace=True)
    # set index to country
    df.set_index('Country', inplace=True)
    return df

with st.spinner('Loading data...'):
    df = load_data()

c1,c2 = st.columns(2)
c1.title("Country wise immigration data analysis")
c1.info('''
    This is a data analysis of the immigration data of the world from 1980 to 2013.
''')
rows = df.shape[0]
c1.metric("Total countries", rows)
total_immgration = df['Total'].sum()
mean_immgration = df['Total'].mean()
c1.metric('Total Immigration', total_immgration, delta=round(mean_immgration))

c2.header("Our Country wise data")
c2.dataframe(df)

st.header("Country immigration trend")
c1, c2, c3 = st.columns(3)
countries = df.index.tolist()
country = c1.selectbox('Select a country', countries, help="Select a country from this list")
country_df = df.loc[country, years]
fig_1 = px.area(country_df, x=country_df.index, y= country_df.values)
c1.success(f"You selected {country}")
c3.dataframe(country_df, use_container_width=True)
c2.plotly_chart(fig_1, use_container_width=True)

st.header('Country immigration comparison')

graphs = ['Line', 'Bar', 'Area',]
c1, c2 = st.columns([1,3])
scs = c1.multiselect('Select countries', countries, help="Select countries from this list")
graph = c1.radio('Select a graph', graphs, help="Select a graph from this list")
countries_df = df.loc[scs, years]
c2.dataframe(countries_df, use_container_width=True)
cdft = countries_df.T
if graph == graphs[0]:
    fig_2 = px.line( cdft, x=cdft.index, y=cdft.columns )
elif graph == graphs[1]:
    fig_2 = px.bar( cdft, x=cdft.index, y=cdft.columns )
elif graph == graphs[2]:
    fig_2 = px.area( cdft, x=cdft.index, y=cdft.columns )
c2.plotly_chart(fig_2, use_container_width=True)
st.write('-----')
st.header('Conclusions:')

st.write('Users can explore and analyze immigration data for various countries and time periods using this Streamlit app. Here are some potential insights that can be drawn:')

st.write('Total Immigration: The app shows the total immigration count across all countries, which can help users understand the scale of immigration during the specified time frame.')

st.write('Country Trends: Users can select specific countries to explore how immigration to those countries has evolved over time. This can lead to insights into the factors driving immigration to particular nations.')

st.write('Country Comparisons: By selecting multiple countries and using different chart types, users can compare immigration trends between nations. This can help identify countries with similar immigration patterns or those with unique trends.')

st.write('Interactive: The interactive nature of the app allows users to explore data dynamically and gain a better understanding of immigration patterns over the years')
st.write('-----')
st.write('### DEVELOPED BY VINAYAK SHUKLA ')
