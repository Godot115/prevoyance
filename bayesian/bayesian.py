# -*- coding: utf-8 -*-
# @Time    : 3/8/22 23:57
# @Author  : godot
# @FileName: bayesian.py
# @Project : prevoyance
# @Software: PyCharm

import plotly.graph_objects as go
from dash import dash_table
from dash import dcc
from dash import html

def bayesianFrame():
    return html.Div(children=
    [
        html.Div(children=[
            html.B('Model:'),
            dcc.RadioItems(id='model_selector_bayesian',
                           options=[
                               {'label': 'Model 2', 'value': 'Model2'},
                               {'label': 'Model 3', 'value': 'Model3'},
                               {'label': 'Model 4', 'value': 'Model4'},
                               {'label': 'Model 5', 'value': 'Model5'},
                               # {'label': 'testmodel', 'value': 'testmodel'},
                           ],
                           value='Model5',
                           labelStyle={'display': 'flex'}
                           ),
            html.Br(),
            # 输入参数，输入框跟随Model变化
            html.Div(id='paramater_inputer_bayesian',children=[
                html.B('Parameters: '),
                html.Br(),
                html.Label("±:"),
                " ",
                html.Div([
                    dcc.Dropdown(
                        id='plus_minus_sign_bayesian',
                        options=[
                            {'label': '+', 'value': 'positive'},
                            {'label': '-', 'value': 'negative'}
                        ],
                        value='negative',
                        searchable=False,
                        clearable=False,
                        style={'height': '15px',
                               "vertical-align": "middle",
                               'line-height': '10px',
                               }
                    )
                ],
                    style={
                        'text-align': 'center',
                        'display': 'inline-block',
                        'width': '55%',
                        'height': '25px',
                    }
                )
            ],hidden=True),
            html.Br(),

            html.B("Settings for design:"), html.Br(),
            html.Label("lower dose boundary (min 0.01):"), html.Br(),
            dcc.Input(
                id='lowerBoundary_bayesian',
                placeholder='Enter a value...',
                type='number',
                min=0.01,
                value='0.01',
            ),
            html.Br(),
            html.Label("upper dose boundary:"), html.Br(),
            dcc.Input(
                id='upperBoundary_bayesian',
                placeholder='Enter a value...',
                type='number',
                value='2500'
            ),
            html.Br(),
            html.Label("Number of iterations for algorithm (min 100):"), html.Br(),
            dcc.Input(
                id='maxIteration_bayesian',
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

            html.Div(children=[html.B('Number of Parameter Sets (max 9):'), html.Br(),
                               dcc.Input(type='number', id='number_of_parameter_sets_bayesian', value=2, min=1,
                                         max=9), ],
                     style={
                         'background-color': '#f2f2f2',
                         'width': '30%',
                     }),
            html.Br(),
            html.Br(),
            html.Div([

                html.B('Parameter Sets:'),
                html.Br(),
                html.Div([
                    html.Div(id='parameter_sets_bayesian'),
                    html.Button('Compute', id='compute_button_bayesian', n_clicks=0),
                ],
                    style={
                        'background-color': '#f2f2f2',
                        'width': '50%',
                    }
                )
            ]),
            html.Div(
                children=[
                    html.Br(),
                    html.Div(id='result_title_bayesian', children=[html.B('Result:')],
                             hidden=True),
                    dash_table.DataTable(
                        id='result_bayesian',
                        style_cell_conditional=[
                            {
                                'textAlign': 'left'
                            }
                        ],
                    )
                ])

        ],
            id='output_div_bayesian',
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