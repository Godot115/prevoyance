# -*- coding: utf-8 -*-
# @Time    : 3/9/22 00:25
# @Author  : godot
# @FileName: efficiency_points_inputer.py
# @Project : prevoyance
# @Software: PyCharm

from dash import html
from dash import dcc

def generateEfficiencyPointsInputer(number_of_design_points_efficiency):
    points = []
    numberOfDesignPoints = int(number_of_design_points_efficiency)
    initialCurrentPoints = [float(0.01), 713.213, 1291.291, 2500.0, 10.0, 10.0, 10.0, 10.0, 10.0]
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