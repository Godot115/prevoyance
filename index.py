# -*- coding: utf-8 -*-
# @Time    : 1/23/22 23:22
# @Author  : godot
# @FileName: index.py
# @Project : prevoyance
# @Software: PyCharm

import dash
import dash_defer_js_import as dji
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL

from bayesian import bayesian, bayesian_parameter_inputer
from bayesian.calculate_bayesian_design import GenerateBayesian
from design import parameters, design_frame, plot, generate_design
from efficiency import efficiency, efficiency_points_inputer, compute_efficiency
from intro import introduction

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {
                inlineMath: [ ['$','$'],],
                processEscapes: true
                }
            });
            </script>
            {%renderer%}
        </footer>
    </body>
</html>
'''
mathjax_script = dji.Import(src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")

app.title = "Prevoyance"
app.layout = html.Div(children=[
    introduction.intro(),
    dcc.Tabs(id="function_selector", value='Design', children=[
        dcc.Tab(label='Generate Optimal Design', value='Design'),
        dcc.Tab(label='Check Design Efficiency', value='Efficiency'),
        dcc.Tab(label='Quasi-Bayesian Designs', value='Bayesian'),
    ]),
    html.Div(id='tabs-content'),
    html.Div(id='hidden-div', style={'display': 'none'}), mathjax_script,
])


@app.callback(Output('tabs-content', 'children'),
              Input('function_selector', 'value'))
def functionSelect(function_selector):
    if function_selector == 'Design':
        return design_frame.designFrame()
    elif function_selector == 'Efficiency':
        return html.Div([
            efficiency.efficiencyFrame()
        ])
    elif function_selector == 'Bayesian':
        return bayesian.bayesianFrame()


@app.callback(Output('paramater_inputer', 'children'),
              Input('model_selector', 'value'))
def paramater(model_selector):
    return parameters.paramaters(model_selector)


@app.callback(Output('paramater_inputer_efficiency', 'children'),
              Input('model_selector_efficiency', 'value'))
def paramater_efficiency(model_selector):
    return parameters.paramaters(model_selector)


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
    return plot.plotFunction(n_clicks, a, b, c, d, plus_minus_sign, model,
                             lowerBoundary, upperBoundary, maxIteration)


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
    return generate_design.GenerateDesign(n_clicks, a, b, c, d, plus_minus_sign, model,
                                          lowerBoundary, upperBoundary, maxIteration)


@app.callback(Output('design_points_efficiency', 'children'),
              Input('number_of_design_points_efficiency', 'value'))
def generatePointsInputer(number_of_design_points_efficiency):
    return efficiency_points_inputer.generateEfficiencyPointsInputer(number_of_design_points_efficiency)


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
    return compute_efficiency.computeEfficiency(n_clicks, dose, weight, a, b, c, d, plus_minus_sign, model,
                                                lowerBoundary, upperBoundary,
                                                maxIteration)





@app.callback(Output('parameter_sets_bayesian', 'children'),
              Input('number_of_parameter_sets_bayesian', 'value'),
              Input('model_selector_bayesian', 'value'))
def generateBayesianParameterInputer(number_of_parameter_sets_bayesian, model_selector_bayesian):
    return bayesian_parameter_inputer.generateBayesianParameterInputer(number_of_parameter_sets_bayesian,
                                                                       model_selector_bayesian)

@app.callback(Output('paramater_inputer_bayesian', 'hidden'),
              Input('model_selector_bayesian', 'value'),
              prevent_initial_call=True)
def plus_minus(model):
    if model == 'Model3':
        return False
    return True
    # return plus_minus_selector.selector(model)

@app.callback([Output("result_bayesian", "data"), Output("result_bayesian", "columns"), Output("result_title_bayesian", "hidden")],
              State({"type": 'parameter', 'index': ALL}, 'value'),
              State('model_selector_bayesian', 'value'),
              State('plus_minus_sign_bayesian', 'value'),
              State('lowerBoundary_bayesian', 'value'),
              State('upperBoundary_bayesian', 'value'),
              State('maxIteration_bayesian', 'value'),
              Input("compute_button_bayesian", "n_clicks"),
              prevent_initial_call=True)
def fetchParametersandCalBaye(parameter, model, plus_minus_sign, lowerBoundary, upperBoundary, maxIteration, n_clicks):
    paramNum = 0
    if model == 'Model2':
        paramNum = 2
    elif model == 'Model3' or model == 'Model4':
        paramNum = 3
    elif model == 'Model5':
        paramNum = 4
    parameter = [tuple(parameter[i:i + paramNum]) for i in range(0, len(parameter), paramNum)]
    lowerBoundary = float(lowerBoundary)
    upperBoundary = float(upperBoundary)
    maxIteration = int(maxIteration)


    return GenerateBayesian(parameter, model, plus_minus_sign, lowerBoundary, upperBoundary, maxIteration, n_clicks)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
