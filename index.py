# -*- coding: utf-8 -*-
# @Time    : 1/23/22 23:22
# @Author  : godot
# @FileName: index.py
# @Project : prevoyance
# @Software: PyCharm

import dash
import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL

import design
import efficiency
import introduction
import paramaters
import plot
from DoseResponse import FirstOrder

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
        dcc.Tab(label='Check Design Efficiency', value='Efficiency'),
    ]),
    html.Div(id='tabs-content'),
    html.Div(id='hidden-div', style={'display': 'none'}),
])


@app.callback(Output('tabs-content', 'children'),
              Input('function_selector', 'value'))
def functionSelect(function_selector):
    if function_selector == 'Design':
        return design.designFrame()
    elif function_selector == 'Efficiency':
        return html.Div([
            efficiency.efficiencyFrame()
        ])


@app.callback(Output('paramater_inputer', 'children'),
              Input('model_selector', 'value'))
def paramater(model_selector):
    return paramaters.paramaters(model_selector)


@app.callback(Output('paramater_inputer_efficiency', 'children'),
              Input('model_selector_efficiency', 'value'))
def paramater_efficiency(model_selector):
    return paramaters.paramaters(model_selector)


@app.callback([Output("plof_of_function", "figure"), Output("plot_title", "hidden")],
              Input('compute_button', 'n_clicks'),
              State('a', 'value'),
              State('b', 'value'),
              State('c', 'value'),
              State('d', 'value'),
              State('plus_minus_sign', 'value'),
              State('model_selector', 'value'),
              State('lowerBoundary', 'value'),
              State('upperBoundary', 'value'),
              State('maxIteration', 'value'),
              prevent_initial_call=True)
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


@app.callback([Output("result", "data"), Output("result", "columns"), Output("result_title", "hidden")],
              Input('compute_button', 'n_clicks'),
              [State('a', 'value'),
               State('b', 'value'),
               State('c', 'value'),
               State('d', 'value'),
               State('plus_minus_sign', 'value'),
               State('model_selector', 'value'),
               State('lowerBoundary', 'value'),
               State('upperBoundary', 'value'),
               State('maxIteration', 'value')],
              prevent_initial_call=True)
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
    result = FirstOrder.firstOrder(points, lowerBoundary, upperBoundary, plus_minus_sign, model, maxIteration, 1000,
                                   *args)
    print(result)
    result = dict(result)
    result = pd.DataFrame(list(result.items()),
                          columns=['Point', 'Weight'])
    return result.to_dict('records'), [{'name': i, 'id': i} for i in result.columns], False


@app.callback(Output('design_points_efficiency', 'children'),
              Input('number_of_design_points_efficiency', 'value'))
def generatePointsInputer(number_of_design_points_efficiency):
    points = []
    numberOfDesignPoints = int(number_of_design_points_efficiency)
    initialCurrentPoints = [float(0), 713.213, 1291.291, 2500.0, 10.0, 10.0, 10.0, 10.0, 10.0]
    for j in range(numberOfDesignPoints):
        points.append(html.Div([
            html.B('Dose ' + str(j + 1) + ': '),
            dcc.Input(type='number', value=initialCurrentPoints[j],
                      id={
                          'type': 'dose',
                          'index': j
                      }), '        ',
            html.B('Weight ' + str(j + 1) + ': '),
            dcc.Input(type='number', value=0.25, max=1, min=0,
                      id={
                          'type': 'weight',
                          'index': j
                      }), html.Br()
        ]))

    return points

@app.callback(Output('result_efficiency', 'children'),
              Input('compute_button_efficiency', 'n_clicks'),
              State({"type": 'dose', 'index': ALL}, 'value'),
              State({"type": 'weight', 'index': ALL}, 'value'),
              State('a', 'value'),
              State('b', 'value'),
              State('c', 'value'),
              State('d', 'value'),
              State('plus_minus_sign', 'value'),
              State('model_selector_efficiency', 'value'),
              State('lowerBoundary_efficiency', 'value'),
              State('upperBoundary_efficiency', 'value'),
              State('maxIteration_efficiency', 'value'),
              prevent_initial_call=True)
def computeEfficiency(n_clicks, dose, weight, a, b, c, d, plus_minus_sign, model, lowerBoundary, upperBoundary,
                      maxIteration):
    currentDesignPoints = []
    currentDesignPoints.clear()
    for i in range(len(dose)):
        currentDesignPoints.append((dose[i], weight[i]))
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    args = (a, b, c, d)
    maxIteration = int(maxIteration)
    lowerBoundary = float(lowerBoundary)
    upperBoundary = float(upperBoundary)
    randonInitialpoints = FirstOrder.createInitialPoints(lowerBoundary, upperBoundary)
    optimalDesignPoints = FirstOrder.firstOrder(randonInitialpoints, lowerBoundary, upperBoundary, plus_minus_sign, model,
                                                maxIteration, 1000,
                                                *args)

    optimalDesignPoints = [(0.000001 if i[0] - 0 <= 1e-2 else float(i[0]), float(i[1])) for i in
                           optimalDesignPoints]
    currentDesignPoints = [(0.000001 if i[0] - 0 <= 1e-2 else float(i[0]), float(i[1])) for i in
                           currentDesignPoints]
    optimalInformationMatrix = FirstOrder.calculateInformationMatrix(optimalDesignPoints, plus_minus_sign, model, *args)
    currentInformationMatrix = FirstOrder.calculateInformationMatrix(currentDesignPoints, plus_minus_sign, model, *args)
    if model == "Model2":
        paramNum = 2
    elif model == "Model3" or model == "Model4":
        paramNum = 3
    else:
        paramNum = 4

    efficiency = pow(np.linalg.det(currentInformationMatrix) / np.linalg.det(optimalInformationMatrix), 1 / paramNum)
    efficiency = round(efficiency, 3)
    print(efficiency)
    return html.Div([
        html.B("D-Efficiency of proposed design:"),
        html.Br(),
        html.P(efficiency)])


if __name__ == '__main__':
    app.run_server(debug=True)
