import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as doc
import plotly.express as px
from dash.dependencies import Input,Output
import pandas as pd     #(version 1.0.0)
import numpy as np
import plotly           #(version 4.5.0)
import plotly.express as px
import numpy as numpy 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.io as pio
import plotly.graph_objects as go
import matplotlib.pyplot as plt
pio.templates.default = "plotly_dark"

#Importing Datasets
circuits=pd.read_csv('datasets/circuits.csv')
constructor_results=pd.read_csv('datasets/constructor_results.csv')
constructor_standings=pd.read_csv('datasets/constructor_standings.csv')
constructors=pd.read_csv('datasets/constructors.csv')
driver_standings=pd.read_csv('datasets/driver_standings.csv')
drivers=pd.read_csv('datasets/drivers.csv')
lap_times=pd.read_csv('datasets/lap_times.csv')
pit_stops=pd.read_csv('datasets/pit_stops.csv')
qualifying=pd.read_csv('datasets/qualifying.csv')
races=pd.read_csv('datasets/races.csv')
results=pd.read_csv('datasets/results.csv')
seasons=pd.read_csv('datasets/seasons.csv')
status=pd.read_csv('datasets/status.csv')

#Races after the year 2014
turbohybrid=races.loc[races['year']>=2014]
turbohybrid=turbohybrid.merge(results,left_on='raceId',right_on='raceId')
turbohybrid=turbohybrid.merge(drivers,left_on='driverId',right_on='driverId')
turbohybrid=turbohybrid.merge(constructors,left_on='constructorId',right_on='constructorId')

#Winner in the tubrohybridera
turbohybridwinner=turbohybrid.loc[turbohybrid['position']=='1']
turbohybridwinner=turbohybridwinner.sort_values(by='raceId')
turbohybridwinner.drop(columns=['date', 'time_x',
       'url_x','number_x','url_y','url'],inplace=True)

#Race laptimes
racelaptimes=races.merge(lap_times,left_on='raceId',right_on='raceId')
racelaptimes=racelaptimes.loc[racelaptimes['year']>=2014]
racelaptimes=racelaptimes.merge(drivers,left_on='driverId',right_on='driverId')
racelaptimes['min_time_lap']=racelaptimes['milliseconds']
racelaptimes_temp=racelaptimes.merge(racelaptimes.groupby(['raceId','lap']).aggregate({'min_time_lap':'min'}),left_on=['raceId','lap'],right_on=['raceId','lap'])
racelaptimes_temp.drop(columns=['min_time_lap_x'],inplace=True)
racelaptimes_temp.rename(columns={'min_time_lap_y':'minlaptime'},inplace=True)
racelaptimes_temp['lapdelta']=racelaptimes_temp['milliseconds']-racelaptimes_temp['minlaptime']
racelaptimes_temp['lapdeltaseconds']=racelaptimes_temp['lapdelta']*0.001
racelaptimes_temp['milliseconds']=racelaptimes_temp['milliseconds']*0.001

#Qualifying Information for the Table plot
qualytable = turbohybrid
qualytable['Driver Name'] = qualytable['forename'] + ' ' + qualytable['surname']
qualytable_f = qualytable[['raceId','name_x','grid','Driver Name','name_y','year']]

#Importing Dash Libs
import pandas as pd     
import plotly           
import plotly.express as px
import dash_bootstrap_components as dbc  
import jupyter_dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
df=racelaptimes_temp
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Input Card
card_1 =  dbc.Card([
    html.Div([   
    html.Div([

        html.Br(),
        html.Label(['Choose year and grandprix:'],style={'width':"25%",'font-weight': 'bold', "text-align": "center",'margin':"15px",'margin-top':"35px" }),
        dcc.Dropdown(id='year_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('year')['year'].unique()],
            value=2018,
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose year...',
            className='form-dropdown',
            style={'width':"95%",'margin':"15px",'color':'black'},
            persistence='string',
            persistence_type='memory'),
               
        dcc.Dropdown(id='gp name',
            options=[{'label':x, 'value':x} for x in df.sort_values('name')['name'].unique()],
            value='Australian Grand Prix',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose gp name...',
            className='form-dropdown',
            style={'width':"95%",'margin':"15px",'color':'black'},
            persistence='string',
            persistence_type='memory'),        
    ],className='two columns',style=dict(display='flex')),

])],color="dark",   # https://bootswatch.com/default/ for more card colors
    inverse=True,   # change color of text (black or white)
    outline=False, )


laptime = dbc.Card([
    html.Div([
        dcc.Graph(id='lap_graph')
    ],className='laptimes'),
])


laptime_dup = dbc.Card([
    html.Div([
        dcc.Graph(id='lap_graph_dup')
    ],className='laptimes_dup'),
])


lapdelta = dbc.Card([
    html.Div([
        dcc.Graph(id='lapdelta_graph')
    ],className='lapdeltas'),
])

lapdelta_dup = dbc.Card([
    html.Div([
        dcc.Graph(id='lapdelta_graph_dup')
    ],className='lapdeltas_dup'),
])


table = dbc.Card([
    html.Div([
        dcc.Graph(id='q_table')
    ],className='qtable'),
])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.layout = html.Div([
   dbc.Col([dbc.Col(card_1),
            dbc.Row([laptime,lapdelta],
                    style={
                        #'display': 'inline-block', 'horizontal-align': 'top',
                        'margin': '3vw'}, justify="around"),
            dbc.Row([laptime_dup,table],
                    style={
                        #'display': 'inline-block', 'horizontal-align': 'top',
                        'margin': '3vw'}, justify="around") 
            ])
])
@app.callback(
    Output('lap_graph','figure'),
    Output('lapdelta_graph','figure'),
    Output('lap_graph_dup','figure'),
    Output('q_table','figure'),
    [Input('year_one','value'),
    Input('gp name','value'),]
)

def build_graph(first_year,name):
    df2 = qualytable_f.loc[(qualytable_f['year']==first_year)&(qualytable_f['name_x']==name)]
    df2 = df2.sort_values(['grid'],ascending=[True])
    dff=df.loc[(df['year']==first_year)&(df['name']==name)]
    dff=dff.loc[dff['milliseconds']<200]    
    fig=px.scatter(dff,x='lap',y='milliseconds',color='surname')
    #fig.update_layout(title_text='Laptimes over the Grand Prix',y_label='seconds')
    fig1=px.box()
    fig1.add_trace(go.Box(x=dff['lap'],y=dff['lapdeltaseconds'],boxpoints=False))
    #fig1.update_layout(title_text='Box plot of race laps over the Grand Prix',y_label='seconds')
    for i in dff['driverId'].unique():
        z=dff.loc[dff['driverId']==i]
        fig2=px.line(dff,x='lap',y='position',color='surname')
        fig2.update_yaxes(autorange='reversed',range=[-1,24])
    fig3 = go.Figure(data=[go.Table(
    header=dict(values=list(df2.drop(columns=['raceId','name_x','year']).columns)
                ,
                align='left'),
    cells=dict(values=[df2['grid'], df2['Driver Name'], df2['name_y']]
               ,
               align='left'))
    ])
    #fig3.update_layout(title_text='Qualifying Grid')
    return fig,fig1,fig2,fig3


if __name__ == '__main__':
    app.run_server( port = 8020, threaded=True)