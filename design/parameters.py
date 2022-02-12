# -*- coding: utf-8 -*-
# @Time    : 1/28/22 17:44
# @Author  : godot
# @FileName: parameters.py
# @Project : prevoyance
# @Software: PyCharm
from dash import dcc
from dash import html


def paramaters(model):
    # if model == "testmodel":
    #     return html.Div(children=
    #     [
    #         html.Label("𝒃:"),
    #         " ",
    #         dcc.Input(id='a',
    #                   placeholder='Enter a value...',
    #                   type='number',
    #                   value='1.0'
    #                   ),
    #         html.Br(),
    #         html.Label("𝒄:"),
    #         " ",
    #         dcc.Input(id='b',
    #                   placeholder='Enter a value...',
    #                   type='number',
    #                   value='1.0'
    #                   ),
    #         html.Br(),
    #         html.Label("𝒃:"),
    #         " ",
    #         dcc.Input(id='c',
    #                   placeholder='Enter a value...',
    #                   type='number',
    #                   value='1.0'
    #                   ),
    #         html.Br(),
    #         html.Label("e:"),
    #         " ",
    #         dcc.Input(id='d',
    #                   placeholder='Enter a value...',
    #                   type='number',
    #                   value='1.0'
    #                   ),
    #         html.Br(),
    #         html.Select([
    #             html.Option('+', value='positive'),
    #             html.Option('-', value='negative'),
    #         ],
    #             id='plus_minus_sign',
    #             style={'visibility': 'hidden'}
    #         ),
    #         html.Br()
    #     ]
    #     )

    if model == "Model5":
        return html.Div(children=
        [
            html.Label("𝒂:"),
            " ",
            dcc.Input(id='a',
                      placeholder='Enter a value...',
                      type='number',
                      value='349.02687'
                      ),
            html.Br(),
            html.Label("𝒃:"),
            " ",
            dcc.Input(id='b',
                      placeholder='Enter a value...',
                      type='number',
                      value='1067.04343'
                      ),
            html.Br(),
            html.Label("𝒄:"),
            " ",
            dcc.Input(id='c',
                      placeholder='Enter a value...',
                      type='number',
                      value='0.76332'
                      ),
            html.Br(),
            html.Label("𝒅:"),
            " ",
            dcc.Input(id='d',
                      placeholder='Enter a value...',
                      type='number',
                      value='2.60551'
                      ),
            html.Br(),
            html.Select([
                html.Option('+', value='positive'),
                html.Option('-', value='negative'),
            ],
                id='plus_minus_sign',
                style={'visibility': 'hidden'}
            ),
            html.Br()
        ]
        )
    if model == "Model4":
        return html.Div(children=
                        [html.Label("𝒂:"),
                         " ",
                         dcc.Input(id='a',
                                   placeholder='Enter a value...',
                                   type='number',
                                   value='349.02687'
                                   ),
                         html.Br(),
                         html.Label("𝒃:"),
                         " ",
                         dcc.Input(id='b',
                                   placeholder='Enter a value...',
                                   type='number',
                                   value='1067.04343'
                                   ),
                         html.Br(),
                         html.Label("𝒄:"),
                         " ",
                         dcc.Input(id='c',
                                   placeholder='Enter a value...',
                                   type='number',
                                   value='0.76332'
                                   ),
                         html.Br(),
                         dcc.Input(id='d',
                                   placeholder='Enter a value...',
                                   type='number',
                                   value='2.60551',
                                   style={'visibility': 'hidden'}
                                   ),
                         html.Select([
                             html.Option('+', value='positive'),
                             html.Option('-', value='negative'),
                         ],
                             id='plus_minus_sign',
                             style={'visibility': 'hidden'}
                         ),
                         html.Br(),
                         html.Br()]
                        )

    if model == "Model3":
        return html.Div(children=
                        [html.Label("𝒂:"),
                         " ",
                         dcc.Input(
                             id='a',
                             placeholder='Enter a value...',
                             type='number',
                             value='349.02687'
                         ),
                         html.Br(),
                         html.Label("𝒃:"),
                         " ",
                         dcc.Input(
                             id='b',
                             placeholder='Enter a value...',
                             type='number',
                             value='1067.04343'
                         ),
                         html.Br(),

                         html.Label("𝒅:"),
                         " ",
                         dcc.Input(
                             id='d',
                             placeholder='Enter a value...',
                             type='number',
                             value='2.60551'
                         ),
                         html.Br(),
                         html.Label("±:"),
                         " ",
                         html.Div([
                             dcc.Dropdown(
                                 id='plus_minus_sign',
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
                         ),
                         dcc.Input(
                             id='c',
                             placeholder='Enter a value...',
                             type='number',
                             value='1067.04343',
                             style={'visibility': 'hidden'}
                         ),
                         html.Br(),
                         html.Br()]
                        )

    if model == "Model2":
        return html.Div(children=[html.Label("𝒂:"),
                                  " ",
                                  dcc.Input(
                                      id='a',
                                      placeholder='Enter a value...',
                                      type='number',
                                      value='349.02687'
                                  ),
                                  html.Br(),
                                  html.Label("𝒃:"),
                                  " ",
                                  dcc.Input(
                                      id='b',
                                      placeholder='Enter a value...',
                                      type='number',
                                      value='1067.04343'
                                  ),
                                  dcc.Input(
                                      id='c',
                                      placeholder='Enter a value...',
                                      type='number',
                                      value='1067.04343',
                                      style={'visibility': 'hidden'}
                                  ),
                                  dcc.Input(
                                      id='d',
                                      placeholder='Enter a value...',
                                      type='number',
                                      value='1067.04343',
                                      style={'visibility': 'hidden'}
                                  ),
                                  html.Select([
                                      html.Option('+', value='positive'),
                                      html.Option('-', value='negative'),
                                  ],
                                      id='plus_minus_sign',
                                      style={'visibility': 'hidden'}
                                  ),
                                  html.Br(),
                                  html.Br()]
                        )
