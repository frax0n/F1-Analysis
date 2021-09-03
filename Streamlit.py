import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_dark"
from urllib.error import URLError

#st.set_page_config(layout="wide")  

@st.cache
def get_lapdata():    
    df=pd.read_csv('https://raw.githubusercontent.com/frax0n/F1-Analysis/Frax/datasets/Graphing.csv',dtype={
    'raceId': 'int64',
    'year': 'int64',
    'name': 'string',
    'driverId': 'int64',
    'lap': 'int64',
    'position': 'int64',
    'time_y': 'object',
    'milliseconds': 'int64',
    'driverRef': 'object',
    'number': 'object',
    'code': 'object',
    'forename': 'object',
    'surname': 'object',
    'dob': 'object',
    'nationality': 'object',
    'minlaptime': 'int64',
    'lapdelta': 'int64',
    'lapdeltaseconds': 'float64',
    'Seconds': 'float64'
    })
    
    return df

def constructor_data():
    df=pd.read_csv('https://raw.githubusercontent.com/frax0n/F1-Analysis/Frax/datasets/constructors_seasonGraphing.csv',dtype={
        'constructorStandingsId': 'int64',
        'raceId': 'int64',
        'constructorId': 'int64',
        'points': 'float64',
        'position': 'int64',
        'positionText': 'object',
        'wins': 'int64',
        'year': 'int64',
        'round': 'int64',
        'circuitId': 'int64',
        'name_x': 'object',
        'date': 'object',
        'time': 'object',
        'url_x': 'object',
        'constructorRef': 'object',
        'name_y': 'object',
        'nationality': 'object',
        'url_y': 'object'
    })
    return df   
df=get_lapdata()
constructor_standings = constructor_data()
try: 
    
    st.title("Choose Year and Grand Prix")
    year = st.selectbox(
        "Choose Year", list(df.sort_values('year')['year'].unique()),4
    )
    grandprix = st.selectbox(
        "Choose GrandPrix", list(df.sort_values('name')['name'].unique()),4

    )
    df2 = df.loc[(df['year']==year) & (df['name']==grandprix)]
    
    if len(df2.index)==0 :
         st.error("This Year doesn't have this particular GrandPrix")
    
    else:


        lapscatterplot=px.scatter(df2,x='lap',y='Seconds',color='surname')
        st.header("Laptimes over the course of the grandprix")
        st.plotly_chart(lapscatterplot) 


        positions_race=px.line(df2,x='lap',y='position',color='surname')
        positions_race.update_yaxes(autorange='reversed',range=[-1,24])
        st.header("Positions over the course of the grandprix")
        st.plotly_chart(positions_race)


        lapdelta=px.box()
        lapdelta.add_trace(go.Box(x=df2['lap'],y=df2['lapdeltaseconds'],boxpoints=False))
        st.header("Box plots for deltas during the course of whole Grandprix")
        st.plotly_chart(lapdelta)

        
        constructor_standings_year_1 = constructor_standings.loc[constructor_standings['year']==year]
        constructor_points_season=px.scatter()
        for i in constructor_standings_year_1['name_y'].unique():
            z=constructor_standings_year_1.loc[constructor_standings_year_1['name_y']==i]
            z = z.sort_values(by=['round'])
            s=z.iloc[0,16]
            print(s)
            constructor_points_season.add_trace(go.Scatter(x=z['round'],y=z['points'],name=s,mode='lines'))
        st.header("Points of the constructors over the season")
        st.plotly_chart(constructor_points_season)

        constructor_position_season=px.scatter()
        for i in constructor_standings_year_1['name_y'].unique():
            z=constructor_standings_year_1.loc[constructor_standings_year_1['name_y']==i]
            z = z.sort_values(by=['round'])
            s=z.iloc[0,16]
            print(s)
            constructor_position_season.add_trace(go.Scatter(x=z['round'],y=z['position'],name=s,mode='lines'))
        constructor_position_season.update_yaxes(autorange='reversed',range=[-1,12])
        st.header("Points of the constructors over the season")
        st.plotly_chart(constructor_position_season)


 
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )