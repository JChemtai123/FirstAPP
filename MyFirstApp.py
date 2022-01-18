# import the required packages
import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import os.path
import datetime
#import glob
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from plotly.subplots import make_subplots

path2 = r'C:\Users\jackl\PycharmProjects\dashApp'  # use your path
mthly_files = glob.glob(path2 + "/*.csv")
counties = [x[64:-4] for x in all_files]
counties
li = []
for mthlyfile in mthly_files:
    mthly_df = pd.read_csv(mthlyfile.format(mthlyfile), index_col=None, header=0)
    mthly_df.rename(columns={'Unnamed: 0': 'Year'}, inplace=True)
    mthly_filename = mthlyfile[73:-4]
    mthly_df['County'] = mthly_filename
    li.append(mthly_df)

    frame = pd.concat(li, axis=0, ignore_index=True)

# Initialise the app
app = dash.Dash(__name__)
server = app.server

# Define the app
# app.layout = html.Div()
# Run the app
# fig2 = make_subplots(rows=1, cols=2)

app.layout = html.Div(children=[
    html.Div(className='row',  # Define the row element
             children=[
                 html.Div(className='four columns div-user-controls'),  # Define the left element
                 html.Div(className='eight columns div-for-charts bg-grey')  # Define the right element
             ])
    ,

    html.Div(children=[
        html.H2('Kenya Seasonal Explorer'),
        html.P('''Rainfall Visualization''')

    ]),
    html.Div(className='one columns', children=[
        html.Label('Select County'),
        dcc.Dropdown(
            id='input_county',
            #             options= [{'label': 'Bomet', 'value': 'Bomet- County'},
            #                       {'label':  'Bungoma', 'value': 'Bungoma- County'},
            #                       {'label': 'Nakuru', 'value': 'Nakuru- County'}
            #                      ],
            options=[
                {'label': j, 'value': j} for j in counties
            ],
            #
            value="Bomet-county",
            multi=False
        ),
    ]),

    html.Div(className='one columns', children=[
        html.Label('Select Year'),
        dcc.Dropdown(
            id='input_year',
            options=[
                {'label': i, 'value': i} for i in mthly_df['Year'].unique()
            ],
            value='All_Years',
            multi=True
        )

    ]),

    dcc.Graph(id='my-graph', figure='figure')
]
)


@app.callback(Output('my-graph', 'figure'),
              [Input('input_county', 'value'),
               Input('input_year', 'value')])
def update_figure(selected_county, selected_year_value):
    df_plot = frame[frame['County'] == selected_county]

    if 'All_Years' in selected_year_value:
        df_plot1 = df_plot.copy()
    else:
        df_plot1 = df_plot[df_plot['Year'].isin(selected_year_value)]

    fig2 = px.bar(df_plot1, x=df_plot1.Year,
                  y=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                  barmode="group", title=selected_county)

    return fig2


if __name__ == '__main__':
    app.run_server()

