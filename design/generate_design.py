# -*- coding: utf-8 -*-
# @Time    : 3/9/22 00:34
# @Author  : godot
# @FileName: generate_design.py
# @Project : prevoyance
# @Software: PyCharm

from dash import html
from dash import dcc
from DoseResponse import FirstOrder
import pandas as pd


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
    result = dict(result)
    result = pd.DataFrame(list(result.items()),
                          columns=['Point', 'Weight'])
    return result.to_dict('records'), [{'name': i, 'id': i} for i in result.columns], False
