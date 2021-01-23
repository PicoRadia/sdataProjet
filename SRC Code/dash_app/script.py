import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import datetime
import io
import dash_table
import feather

import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
pio.templates.default = 'plotly_white'






# *******************************************************************************************

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

url1 = "https://raw.githubusercontent.com/PicoRadia/sdataProjet/main/dataset/Spotify_train_dataset.csv"

df = pd.read_csv(url1)#31728 rows x 20 columns

# for fig 1 & 2
genres = df.genre.unique()
genre_count = df.genre.value_counts()
genredf = pd.DataFrame({"genre" : genres , "count" :genre_count })

# for fig 3
keys = [x for x in range(12)]
kk = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
kdf = pd.DataFrame({"key":kk , "count" : df.groupby("key")["key"].count().count()})

# for fig 4
mdf = pd.DataFrame({"mode":["minor","major"] , "count" :df.groupby("mode")['mode'].count()})
modes = [0,1]

# for fig 5
tsf = pd.DataFrame({"ts":[4, 5, 3, 1], "count" :df.groupby("time_signature")["time_signature"].count()})
ts = [1, 3, 4, 5]



# all genres
genre_all = [g for g in genres]
genre_all.append('all')

app.layout = html.Div([
    html.Br(), html.Br(), html.Br(),  
    html.Center(html.H1('Exploratory Data Analysis')),
    html.Center(html.H2('Spotify Genres Classifier')),

    html.Br(),
    html.Br(),
    html.Center(html.H4("The genres present in the training dataset")),
    # html.Div(children = (html.Center(dcc.Graph(id='graph1',figure= px.pie( genredf, values='count', names='genre' , color_discrete_sequence=px.colors.sequential.Plasma_r,))),
    dbc.Row(
            [
                dbc.Col(dcc.Graph(id="graph1",figure= px.pie( genredf, values='count', names='genre' , color_discrete_sequence=px.colors.sequential.Plasma_r,)), md=6),
                dbc.Col(dcc.Graph(id="graph2",figure=px.bar(genre_count,color_discrete_sequence = px.colors.qualitative.Antique)), md=6),
            ],
            align="center",
        ),

    html.Br(),html.Br(),html.Br(),
    html.Center(html.H4("Pie charts for the key, the mode and time signature")),
    html.Br(),html.Br(),
    dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(dbc.Col([dcc.Dropdown(
                        id='dropdown1', clearable=False,
                        value= 'Rap', options=[
                            {'label': c, 'value': c}
                            for c in genre_all
                        ]
                        )],md=5)),
                        dcc.Graph(id="graph3"),

                    ], md=4),
                dbc.Col(dcc.Graph(id="graph4"), md=4),
                dbc.Col(dcc.Graph(id="graph5"), md=4),

            ],
            align="center",
        ),
    html.Br(),html.Br(),html.Br(),
    html.Center(html.H4("Pie charts for the key, the mode and time signature")),


])

# *********************** Callbacks ***********************************

@app.callback([Output("graph3","figure"),Output("graph4","figure"),Output("graph5","figure")],[Input("dropdown1","value")])
def impact1(val1):
    if val1==None : 
        pass
    else:
        if val1 == "all" :
            kdf = pd.DataFrame({"key":kk , "count" : df.groupby("key")["key"].count().count()})
            mdf = pd.DataFrame({"mode":["minor","major"] , "count" :df.groupby("mode")['mode'].count()})
            tsf = pd.DataFrame({"ts":[4, 5, 3, 1], "count" :df.groupby("time_signature")["time_signature"].count()})
            fig3 =  px.pie(kdf,values='count', names='key',color_discrete_sequence = px.colors.sequential.tempo)
            fig4 = px.pie(mdf,values='count', names='mode',color_discrete_sequence = px.colors.sequential.RdBu)
            fig5 = px.pie(tsf,values='count', names='ts', color_discrete_sequence = px.colors.sequential.Viridis)
            return fig3 , fig4 , fig5
            
        else: 
            l = []
            for k in keys:
                l.append(df.query("key == "+ str(k))[df['genre']== str(val1)].key.count())
            mdf = pd.DataFrame({"key":kk , "count" : l})
            fig3 = px.pie(mdf,values='count', names='key',color_discrete_sequence = px.colors.sequential.Viridis)
            l1 = []
            for m in [0,1]:
                l1.append(df.query("mode == "+ str(m))[df['genre']== str(val1)].key.count())
            pdf = pd.DataFrame({"mode":['major','minor'] , "count" : l1})
            fig4 = px.pie(pdf,values='count', names='mode',color_discrete_sequence = px.colors.sequential.RdBu)
            l2 = []
            for t in ts:
                l2.append(df.query("time_signature == "+ str(t))[df['genre']== str(val1)].key.count())
            tsf1 = pd.DataFrame({"ts": ts , "count" : l2})
            fig5 = px.pie(tsf1, values='count', names='ts',color_discrete_sequence = px.colors.sequential.Emrld)
         
            return fig3, fig4,fig5



# Run app
if __name__ == '__main__':
    app.run_server(debug=True,port=5000)

