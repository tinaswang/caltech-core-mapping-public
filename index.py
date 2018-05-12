import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from loremipsum import get_sentences
import pandas as pd
import re
from collections import Counter as C

app = dash.Dash()

app.scripts.config.serve_locally = True

vertical = True

if not vertical:
    app.layout = html.Div([
        dcc.Tabs(
            tabs=[
                {'label': 'Computer Science', 'value': 1},
                {'label': 'Mechanical Engineering', 'value': 2},
                # {'label': 'Physics and Astrophysics', 'value': 3},
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
        html.Div(id='tab-output')
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
                # {'label': 'Physics and Astrophysics', 'value': 3},
                {'label': 'Electrical Engineering', 'value': 4},
                {'label': 'Chemistry', 'value': 5},
                {'label': 'Chemistry Engineering', 'value': 6},
                {'label': 'Biology and Bioengineering', 'value': 7},
                {'label': 'Geological and Planetary Sciences', 'value': 8},
                # {'label': 'Pseudocore', 'value': 9},
                ],
                value=2,
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
        html.Div(
            html.Div(id='tab-output'),
            style={'width': '80%', 'float': 'right'}
        )
    ], style={
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto',
    })



df = pd.read_csv('response.csv')

majors = df['option'].unique()

domain = [{'x': [0, 0.18],'y': [0, .19]},
          {'x': [0, .18],'y': [.21, 0.4]},
          {'x': [0, .18],'y': [.42, 0.6]},
          {'x': [0, .18],'y': [.62, 0.8]},
          {'x': [0, .18],'y': [.82, 1]},
          {'x': [0.22, 0.4],'y': [0, .19]},
          {'x': [0.22, .4],'y': [.21, 0.4]},
          {'x': [0.22, .4],'y': [.42, 0.6]},
          {'x': [0.22, .4],'y': [.62, 0.8]},
          {'x': [0.22, .4],'y': [.82, 1]},  
          {'x': [0.42, 0.6],'y': [0, .19]},
          {'x': [0.42, .6],'y': [.21, 0.4]},
          {'x': [0.42, .6],'y': [.42, 0.6]},
          {'x': [0.42, .6],'y': [.62, 0.8]},
          {'x': [0.42, .6],'y': [.82, 1]},  
          {'x': [0.62, 0.8],'y': [0, .19]},
          {'x': [0.62, .8],'y': [.21, 0.4]},
          {'x': [0.62, .8],'y': [.42, 0.6]},
          {'x': [0.62, .8],'y': [.62, 0.8]},
          {'x': [0.62, .8],'y': [.82, 1]},
          {'x': [0.82, 1],'y': [0, .19]},
          {'x': [0.82, 1],'y': [.21, 0.4]},
          {'x': [0.82, 1],'y': [.42, 0.6]},
          {'x': [0.82, 1],'y': [.62, 0.8]},
          {'x': [0.82, 1],'y': [.82, 1]},         
        ]

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):
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

    j = 0

    classes = list(df_major)
    for i in classes:
        cs_class = df_major[i].tolist()
        cs_class = [x for x in cs_class if str(x) != 'nan']
        cs_clean = []
        for word in cs_class:
            word = re.split(' ,|, | , ', word)
            cs_clean.extend(word)

        c = C(cs_clean)
        cs_final = dict(c)
        cs_df = pd.DataFrame(list(cs_final.items()))
        cs_df.columns = ["class", "data"]
        temp_dict = {
            "values": cs_df["data"].tolist(),
            "labels": cs_df["class"].tolist(),
            "domain": domain[j],
            "hoverinfo":"label+percent",
            'textinfo':'none',
            'name' : 'i',
            "hole": .4,
            "type": "pie",

            }

        layout_dict.append(

                {
                "font": {
                    "size": 8
                },
                    "showarrow": False,
                    "text": i,
                    "x": ((domain[j]["x"])[1] + (domain[j]["x"])[0])/2 - 0.02,
                    "y": ((domain[j]["y"])[1] + (domain[j])["y"][0])/2 
                }
                
        )
        framelist.append(cs_df)
        data.append(temp_dict)
        j += 1
    


    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data,

                "layout": {
                    'showlegend': False,
                    'annotations' : layout_dict,
                     'height': 800
                    }

               })])

if __name__ == '__main__':
    app.run_server(debug=True)