# -*- coding: utf-8 -*-
# @Time    : 1/24/22 02:29
# @Author  : godot
# @FileName: design.py
# @Project : prevoyance
# @Software: PyCharm
import plotly.graph_objects as go
from dash import dash_table
from dash import dcc
from dash import html


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig


def designFrame():
    return html.Div(children=
    [
        html.Div(children=[
            html.B('Model:'),
            dcc.RadioItems(id='model_selector',
                           options=[
                               {'label': 'Model 2', 'value': 'Model2'},
                               {'label': 'Model 3', 'value': 'Model3'},
                               {'label': 'Model 4', 'value': 'Model4'},
                               {'label': 'Model 5', 'value': 'Model5'}
                           ],
                           value='Model5',
                           labelStyle={'display': 'flex'}
                           ),
            html.Br(),
            html.B("Parameters:"),
            html.Br(),
            # 输入参数，输入框跟随Model变化
            html.Div(id='paramater_inputer'),
            html.B("Settings for design:"), html.Br(),
            html.Label("lower dose boundary (big than 0):"), html.Br(),
            dcc.Input(
                id='lowerBoundary',
                placeholder='Enter a value...',
                type='number',
                min=0.0000000001,
                value='0.00001',
            ),
            html.Br(),
            html.Label("upper dose boundary:"), html.Br(),
            dcc.Input(
                id='upperBoundary',
                placeholder='Enter a value...',
                type='number',
                value='2500'
            ),
            html.Br(),
            html.Label("Number of iterations for algorithm (min 100):"), html.Br(),
            dcc.Input(
                id='maxIteration',
                placeholder='Enter a value...',
                type='number',
                min=100,
                value='100'
            ),
            html.Br(),
            html.Br(),
            html.Button('Compute', id='compute_button', n_clicks=0),
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
            # plot of function
            html.Div(id='plot_div',
                     children=[
                         html.Div(id='plot_title', children=[html.B('Plot of Function:')],
                                  hidden=True),
                         dcc.Graph(id="plof_of_function", figure=blank_fig())
                     ]),
            html.Div(
                children=[
                    html.Div(id='result_title', children=[html.B('Result:')],
                             hidden=True),
                    dash_table.DataTable(
                        id='result',
                        style_cell_conditional=[
                            {
                                'textAlign': 'left'
                            }
                        ],
                    )
                ])
        ],
            id='output_div',
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
