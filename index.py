# -*- coding: utf-8 -*-
# @Time    : 1/23/22 23:22
# @Author  : godot
# @FileName: index.py
# @Project : prevoyance_dash
# @Software: PyCharm

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px

import design
import introduction
import paramaters
import plot
from DoseResponse import FirstOrder
import pandas as pd
import plotly.graph_objs as go


external_scripts = [
    {
        'type': 'text/javascript',
        'id': 'MathJax-script',
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'
    }
]
app = dash.Dash(__name__, external_scripts=external_scripts, suppress_callback_exceptions=True)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


app.title = "Prevoyance"
app.layout = html.Div(children=[
    introduction.intro(),
    dcc.Tabs(id="function_selector", value='Design', children=[
        dcc.Tab(label='Generate Optimal Design', value='Design'),
        dcc.Tab(label='Check Design Effiency', value='Effiency'),
    ]),
    html.Div(id='tabs-content'),
    html.Div(id='hidden-div', style={'display': 'none'}),
])


@app.callback(Output('tabs-content', 'children'),
              Input('function_selector', 'value'))
def functionSelect(function_selector):
    if function_selector == 'Design':
        return design.designFrame()
    elif function_selector == 'Effiency':
        return html.Div([
            html.H3('Effiency')
        ])


@app.callback(Output('paramater_inputer', 'children'),
              Input('model_selector', 'value'))
def paramater(model_selector):
    return paramaters.paramaters(model_selector)


@app.callback([Output("plof_of_function", "figure"),Output("plot_title", "hidden")],
              Input('compute_button', 'n_clicks'),
              State('a', 'value'),
              State('b', 'value'),
              State('c', 'value'),
              State('d', 'value'),
              State('plus_minus_sign', 'value'),
              State('model_selector', 'value'),
              State('lowerBoundary', 'value'),
              State('upperBoundary', 'value'),
              State('maxIteration', 'value'))
def plotFunction(n_clicks, a, b, c, d, plus_minus_sign, model,
                     lowerBoundary, upperBoundary, maxIteration):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    args = (a, b, c, d)
    lowerBoundary = float(lowerBoundary)
    upperBoundary = float(upperBoundary)
    x, y = plot.plotFunc(model, plus_minus_sign, lowerBoundary, upperBoundary, *args)
    fig = px.line(x=x, y=y)
    return fig, False


@app.callback([Output("result", "data"),Output("result", "columns"),Output("result_title", "hidden")],
              Input('compute_button', 'n_clicks'),
              State('a', 'value'),
              State('b', 'value'),
              State('c', 'value'),
              State('d', 'value'),
              State('plus_minus_sign', 'value'),
              State('model_selector', 'value'),
              State('lowerBoundary', 'value'),
              State('upperBoundary', 'value'),
              State('maxIteration', 'value'))
def GenerateDesign(n_clicks, a, b, c, d, plus_minus_sign, model,
                     lowerBoundary, upperBoundary, maxIteration):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    args = (a, b, c, d)
    maxIteration = int(maxIteration)
    lowerBoundary = float(lowerBoundary)
    upperBoundary = float(upperBoundary)
    points = FirstOrder.createInitialPoints(lowerBoundary, upperBoundary)
    result = FirstOrder.firstOrder(points,lowerBoundary,upperBoundary, plus_minus_sign, model, maxIteration,1000, *args)
    result = dict(result)
    result = pd.DataFrame(list(result.items()),
                 columns=['Point', 'Weight'])
    print(result.values)
    return result.to_dict('records'), [{'name': i, 'id': i} for i in result.columns], False


if __name__ == '__main__':
    app.run_server(debug=True)
