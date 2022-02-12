# -*- coding: utf-8 -*-
# @Time    : 3/9/22 00:37
# @Author  : godot
# @FileName: bayesian_parameter_inputer.py
# @Project : prevoyance
# @Software: PyCharm
from dash import html
from dash import dcc


def generateBayesianParameterInputer(number_of_parameter_sets_bayesian, model_selector_bayesian):
    paramater_sets = ['a', 'b']
    if model_selector_bayesian == "Model3":
        paramater_sets.append('d')
    elif model_selector_bayesian == "Model4":
        paramater_sets.append('c')
    elif model_selector_bayesian == "Model5":
        paramater_sets.append('c')
        paramater_sets.append('d')
    parameters = []
    numberOfDesignPoints = int(number_of_parameter_sets_bayesian)
    initialParam = [349.02687, 1067.04343, 0.76332, 2.60551]
    for j in range(numberOfDesignPoints):
        parameters.append(html.B('Parameter set ' + str(j + 1) + ': '))
        for index, param in enumerate(paramater_sets):
            parameters.append(
                html.Div([
                    html.B(param.__repr__()[1] + ': '),
                    dcc.Input(type='number', value=initialParam[index],
                              id={
                                  'type': 'parameter',
                                  'index': j
                              }), '        ',
                ],
                style={'margin-left':'20px'})
            )
        parameters.append(html.Br())


    return parameters