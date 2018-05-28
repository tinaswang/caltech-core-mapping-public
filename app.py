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
import random

# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'

# TO RUN ON HEROKU: UNCOMMENT NEXT THREE LINES
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
# -----------------------------------------------------


# TO RUN Locally: uncomment the next line
# app = dash.Dash()
# -------------------------------------------

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.title = "Caltech Core Mapping"
vertical = True

if not vertical:
    app.layout = html.Div([

        dcc.Tabs(
            tabs=[
                {'label': 'Home (Pseudocore)', 'value': 10},
                {'label': 'Computer Science', 'value': 1},
                {'label': 'Mechanical Engineering', 'value': 2},
                {'label': 'Physics and Astrophysics', 'value': 3},
                {'label': 'Electrical Engineering', 'value': 4},
                {'label': 'Chemistry', 'value': 5},
                {'label': 'Chemistry Engineering', 'value': 6},
                {'label': 'Biology and Bioengineering', 'value': 7},
                {'label': 'Geological and Planetary Sciences', 'value': 8},
                {'label': 'Math', 'value': 9},
                # {'label': 'Pseudocore', 'value': 10},

            ],
            value='ui_form_tab',
            id='tabs',
            vertical=vertical
        ),


        html.Div([
            html.H1('Caltech Core Curriculum Mapping'),
            html.Hr(),
            html.Div(id='dropdown'),
            dcc.Dropdown(id='c-dropdown')],
            style={'width': '80%', 'float': 'right', 'vertical-align': 'top'}
        ),

        html.Div(
            id='tab-output')
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
                {'label': 'Home (Pseudocore)', 'value': 10},
                {'label': 'Computer Science', 'value': 1},
                {'label': 'Mechanical Engineering', 'value': 2},
                {'label': 'Physics and Astrophysics', 'value': 3},
                {'label': 'Electrical Engineering', 'value': 4},
                {'label': 'Chemistry', 'value': 5},
                {'label': 'Chemical Engineering', 'value': 6},
                {'label': 'Biology and Bioengineering', 'value': 7},
                {'label': 'Geological and Planetary Sciences', 'value': 8},
                {'label': 'Math', 'value': 9},
                
                ],
                value=10,
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
            html.H1('Caltech Core Curriculum Mapping'),
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

# Set the value of the dropdown list based on the tab
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
                8: 'GPS',
                9: 'Math'}


    if value != 10:
        df_major = df[df['option'] == val_dict[value]]
        # Remove ma 2, ma 3 acm 95ab
        df_major.drop(df_major.columns[[0, 1, 2]], axis=1, inplace=True)

        df_major = df_major.dropna(axis=1, how='all')
        class_list = list(df_major)
        clean_class = []

        for i in range(len(class_list)):
            curr = class_list[i]
            if (curr[-2] == "."):
                clean_class.append(curr[:-2])
            else:
                clean_class.append(curr)
    else:
        class_list = ["Ma 2", "Ma 3", "ACM 95ab"]
        clean_class = class_list
    
    return [{'label': clean_class[i], 
            'value': class_list[i]} for i in range(len(class_list))]


# Return value of the dropdown
@app.callback(
    dash.dependencies.Output('c-dropdown', 'value'),
    [dash.dependencies.Input('c-dropdown', 'options')])
def set_value(available_options):
    return available_options[0]['value']


# Display the completed graph
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
                8: 'GPS', 
                9: 'Math'}



    framelist = []
    data = []
    layout_dict = []
    labels = []

    if value == 10:
        if selected_class == "ACM 95ab":
            labels = [
                    "Ma 1a",
                    "Ma 1b",
                    "Ma 1c",
                    "Ph 1a",
                    "Ph 1b",
                    "Ph 1c",
                    "Ma 2",
                    "Ma 2", 
                    "CS 1",
                    "Ph 2a", 
                    "Ph 2b", 
                    "EE 44", 
                    "ACM 11"
                  ]
            data.append({
                  #"title":"Global Emissions 1990-2011",
                  "values": [22, 35, 45, 3, 6, 5, 30, 1, 4, 5, 2, 1, 2],
                  "labels": labels,
                  "domain": {"x": [0, 2]},
                  "name": "Number of Students",
                  "hoverinfo":"label+value+name", # updated to have numbers of students rather than percentages
                  "textinfo":"value",
                  #"name": "Percent of Students",
                  #"hoverinfo":"label+percent+name",
                  "hole": .4,
                  "type": "pie"
                })



        elif selected_class == "Ma 3":
            labels = [
                    "Ma 1a",
                    "Ma 1b",
                    "Ma 1c",
                    "Ma 2",
                    "Ch 1b",
                    "Ph 1a",
                    "Ph 2b",
                    "Ph 1c", 
                    "ACM 11",
                    "CS 150", 
                    "CS 1", 
                    "Ph 3", 
                    "Bi 1"
                  ]
            data.append({
              "values": [7, 14, 9, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1],
              "labels": labels,
              "domain": {"x": [0, 2]},
              "name": "Number of Students",  # updated to have numbers of students rather than percentages
              "hoverinfo":"label+value+name",
              "textinfo":"value",
              #"name": "Percent of Students",
              #"hoverinfo":"label+percent+name",
              "hole": .4,
              "type": "pie"
            })


        else:
            labels = [
                    "Ma 1a",
                    "Ma 1b",
                    "Ma 1c",
                    "Ch 1a",
                    "Ch 1b",
                    "Ph 1a",
                    "Ph 1b",
                    "Ph 1c", 
                    "Bi 1x",
                    "Ph 2a", 
                    "Bi 9", 
                  ]
            data.append(
                {
                  "values": [20, 39, 34, 1, 1, 5, 13, 13, 1, 1, 1],
                  "labels": labels,
                  "domain": {"x": [0, 2]},
                  "name": "Number of Students",  # updated to have numbers of students rather than percentages
                  "hoverinfo":"label+value+name",
                  "textinfo":"value",
                  #"name": "Percent of Students",
                  #"hoverinfo":"label+percent+name",
                  "hole": .4,
                  "type": "pie"
                })

    else:
        df_major = df[df['option'] == val_dict[value]]

        df_major.drop(df_major.columns[[0, 1, 2]], axis=1, inplace=True)

        df_major = df_major.dropna(axis=1, how='all')

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

        labels = cs_df["class"].tolist()
        temp_dict = {
                "values": cs_df["data"].tolist(),
                "labels": labels,
                #"hoverinfo":"label+percent",
                # 'textinfo':'none',
                "hoverinfo":"label+value+name",  # updated to have numbers of students rather than percentages
                "textinfo":"value",
                'name' : selected_class,
                "hole": .4,
                "type": "pie",

            }

        framelist.append(cs_df)
        data.append(temp_dict)

    colors = []
    for i in range(len(labels)):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        out = 'rgb(' + str(r) + ", " + str(g) + ", " + str(b) + ")"
        colors.append(out)
    data[0]['marker'] = {'colors': colors}

    layout_dict.append({
                "font": {
                    "size": 20
                },
                    "showarrow": False,
                    "text": selected_class,
                       
                })
        


    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,

                "layout": {
                    'annotations' : layout_dict, # Vibha added a small title
                     'height': 600,
                    'title':"For each surveyed class, the donut shows the different classes that certain numbers of students found helpful."
                    }

               })])



# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
    # Uncomment below to run locally
    # app.server.run(debug=True)
