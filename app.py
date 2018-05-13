# Import required libraries
import os
from random import randint

import plotly.plotly as py
from plotly.graph_objs import *

import flask
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re
from collections import Counter as C

# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
app.title = "Caltech Core Mapping"
# app = dash.Dash(__name__)
# server = app.server


# app = dash.Dash()
# app.scripts.config.serve_locally = True

vertical = True

if not vertical:
    app.layout = html.Div([

        dcc.Tabs(
            tabs=[
                {'label': 'Computer Science', 'value': 1},
                {'label': 'Mechanical Engineering', 'value': 2},
                {'label': 'Physics and Astrophysics', 'value': 3},
                {'label': 'Electrical Engineering', 'value': 4},
                {'label': 'Chemistry', 'value': 5},
                {'label': 'Chemistry Engineering', 'value': 6},
                {'label': 'Biology and Bioengineering', 'value': 7},
                {'label': 'Geological and Planetary Sciences', 'value': 8},
                # {'label': 'Pseudocore', 'value': 9},

            ],
            value='ui_form_tab',
            id='tabs',
            vertical=vertical
        ),


        html.Div([
            html.Hr(),
            html.Div(id='dropdown'),
            dcc.Dropdown(id='c-dropdown')],
            style={'width': '80%', 'float': 'right', 'vertical-align': 'top'}
        ),

        html.Div([
            html.Hr(), id='tab-output'])
    ], style={
        'width': '80%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'
    })

else:
    app.layout = html.Div([
        html.Div(
            dcc.Tabs(
                tabs=[
                {'label': 'Computer Science', 'value': 1},
                {'label': 'Mechanical Engineering', 'value': 2},
                {'label': 'Physics and Astrophysics', 'value': 3},
                {'label': 'Electrical Engineering', 'value': 4},
                {'label': 'Chemistry', 'value': 5},
                {'label': 'Chemistry Engineering', 'value': 6},
                {'label': 'Biology and Bioengineering', 'value': 7},
                {'label': 'Geological and Planetary Sciences', 'value': 8},
                # {'label': 'Pseudocore', 'value': 9},
                ],
                value=1,
                id='tabs',
                vertical=vertical,
                style={
                    'height': '100vh',
                    'borderRight': 'thin lightgrey solid',
                    'textAlign': 'left'
                }
            ),
            style={'width': '20%', 'float': 'left'}
        ),
            

        html.Div([
            html.Hr(),
            html.Div(id='dropdown'),
            dcc.Dropdown(id='c-dropdown')],
            style={'width': '80%', 'float': 'right', 'vertical-align': 'top'}
        ),

        html.Div([
            html.Hr(),
            html.Div(id='tab-output'),
            ],
            style={'width': '80%', 'float': 'right'}
        ),

    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })



df = pd.read_csv('response.csv')

majors = df['option'].unique()
# all_classes = list(df)


# @app.route('/', methods=['GET'])
@app.callback(
    dash.dependencies.Output('c-dropdown', 'options'),
    [dash.dependencies.Input('tabs', 'value')])
def set_class_options(value):
    val_dict =  {1: 'Computer Science',
                 2: 'Mechanical Engineering',
                 3: 'Physics/Astrophysics',
                 4: 'Electrical Engineering',
                 5: 'Chemistry',
                6: 'Chemical Engineering',
                7: 'Biology',
                8: 'GPS'}
    #             # 9: 'pseudo'}
    df_major = df[df['option'] == val_dict[value]]

    df_major.drop(df_major.columns[[0, 1, 2]], axis=1, inplace=True)

    df_major = df_major.dropna(axis=1, how='all')
    class_list = list(df_major)
    clean_class = []

    for i in range(len(class_list)):
        curr = class_list[i]
        if (curr[-2] == "."):
            print(curr)
            clean_class.append(curr[:-2])
        else:
            clean_class.append(curr)

    return [{'label': clean_class[i], 
            'value': class_list[i]} for i in range(len(class_list))]

# @app.route('/', methods=['GET'])
@app.callback(
    dash.dependencies.Output('c-dropdown', 'value'),
    [dash.dependencies.Input('c-dropdown', 'options')])
def set_value(available_options):
    return available_options[0]['value']


# @app.route('/', methods=['GET'])
@app.callback(Output('tab-output', 'children'), 
    [Input('tabs', 'value'), 
    dash.dependencies.Input('c-dropdown', 'value')])
def display_content(value, selected_class):
    val_dict =  {1: 'Computer Science',
                 2: 'Mechanical Engineering',
                 3: 'Physics/Astrophysics',
                 4: 'Electrical Engineering',
                 5: 'Chemistry',
                6: 'Chemical Engineering',
                7: 'Biology',
                8: 'GPS'}
    #             # 9: 'pseudo'}


    df_major = df[df['option'] == val_dict[value]]

    df_major.drop(df_major.columns[[0, 1, 2]], axis=1, inplace=True)

    df_major = df_major.dropna(axis=1, how='all')

    framelist = []
    data = []
    layout_dict = []
    num_classes = len(list(df_major))

    classes = list(df_major)
    # for i in classes:
    cs_class = df_major[selected_class].tolist()
    cs_class = [x for x in cs_class if str(x) != 'nan']
    cs_clean = []
    for word in cs_class:
        word = re.split(' ,|, | , ', word)
        cs_clean.extend(word)

    c = C(cs_clean)
    cs_final = dict(c)
    cs_df = pd.DataFrame(list(cs_final.items()))
    cs_df.columns = ["class", "data"]
    if (selected_class[-2] == "."):
        selected_class = selected_class[:-2]
    temp_dict = {
            "values": cs_df["data"].tolist(),
            "labels": cs_df["class"].tolist(),
            # "domain": domain[j],
            "hoverinfo":"label+percent",
            'textinfo':'none',
            'name' : selected_class,
            "hole": .4,
            "type": "pie",

        }



    layout_dict.append(

                {
                "font": {
                    "size": 20
                },
                    "showarrow": False,
                    "text": selected_class,
                   
                }
                
        )
    framelist.append(cs_df)
    data.append(temp_dict)

    


    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,

                "layout": {
                    'annotations' : layout_dict,
                     'height': 600
                    }

               })])



# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)







