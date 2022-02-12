# -*- coding: utf-8 -*-
# @Time    : 2/4/22 00:20
# @Author  : godot
# @FileName: efficiency.py
# @Project : prevoyance
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 1/24/22 02:29
# @Author  : godot
# @FileName: design_frame.py
# @Project : prevoyance
# @Software: PyCharm
from dash import dcc
from dash import html
import plotly.graph_objects as go
from dash import dash_table

from dash.dependencies import Input, Output





def efficiencyFrame():
    return html.Div(children=
    [
        html.Div(children=[
            html.B('Model:'),
            dcc.RadioItems(id='model_selector_efficiency',
                           options=[
                               {'label': 'Model 2', 'value': 'Model2'},
                               {'label': 'Model 3', 'value': 'Model3'},
                               {'label': 'Model 4', 'value': 'Model4'},
                               {'label': 'Model 5', 'value': 'Model5'},
                               # {'label': 'testmodel', 'value': 'testmodel'}
                           ],
                           value='Model5',
                           labelStyle={'display': 'flex'}
                           ),
            html.Br(),
            html.B("Parameters:"),
            html.Br(),
            # 输入参数，输入框跟随Model变化
            html.Div(id='paramater_inputer_efficiency'),
            html.B("Settings for design:"), html.Br(),
            html.Label("lower dose boundary (min 0.01):"), html.Br(),
            dcc.Input(
                id='lowerBoundary_efficiency',
                placeholder='Enter a value...',
                type='number',
                min=0.01,
                value='0.01',
            ),
            html.Br(),
            html.Label("upper dose boundary:"), html.Br(),
            dcc.Input(
                id='upperBoundary_efficiency',
                placeholder='Enter a value...',
                type='number',
                value='2500'
            ),
            html.Br(),
            html.Label("Number of iterations for algorithm (min 100):"), html.Br(),
            dcc.Input(
                id='maxIteration_efficiency',
                placeholder='Enter a value...',
                type='number',
                min=100,
                value='100'
            ),
            html.Br(),
            html.Br(),
        ],
            style={
            'background-color': '#f2f2f2',
            'width': '30%',
            'border': '2px #f1f1f1 double',
            'float': 'left',
            'margin': '1%'
        }
        ),
        html.Div(children=[

            html.Div(children=[html.B('Number of Design Points (max 9):'),html.Br(),
            dcc.Input(type='number',id='number_of_design_points_efficiency',value=4,min=1,max=9),],
                     style={
                     'background-color': '#f2f2f2',
                     'width': '30%',
                     }),
            html.Br(),
            html.Br(),
            html.Div([

                html.B('Design Points:'),
                html.P('The sum of the weights should be 1.'),
                html.Div([
                    html.Div(id='design_points_efficiency'),
                    html.Br(),
                    html.Button('Compute', id='compute_button_efficiency', n_clicks=0),
                ],
                    style={
                        'background-color': '#f2f2f2',
                        'width': '50%',
                    }
                )
            ]),
            html.Div(id='result_efficiency'),


        ],
                 id='output_div_efficiency',
                 style={"background-color": '#1',
            'width': '65%',
            'float': 'right',
            'margin': '1%'
    })
    ], style={
        'border': "2px #f2f2f2 dotted",
        'width': '85%',
        'overflow': 'auto',
        'margin': '0 auto',
        'padding': 10,
        'flax': 1,
        'flex-direction': 'row'
    }
    )

