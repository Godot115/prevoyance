# -*- coding: utf-8 -*-
# @Time    : 2/3/22 20:32
# @Author  : godot
# @FileName: plot.py
# @Project : prevoyance
# @Software: PyCharm

import numpy as np
import plotly.graph_objs as go
from dash import dcc
from dash import html
import plotly.express as px



def chooseModel(x, model, plus_minus_sign, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    if model == "Model2":
        return a * np.exp(x / b)
    elif model == "Model3":
        if plus_minus_sign == "positive":
            return a * np.exp((x / b) ** d)
        else:
            return a * np.exp(-(x / b) ** d)
    elif model == "Model4":
        return a * (c - (c - 1) * np.exp(-x / b))
    elif model == "Model5":
        return a * (c - (c - 1) * np.exp(-(x / b) ** d))
    # elif model == "testmodel":
    #     return args[1] + (args[2]-c) / (1 + np.exp( args[0] * (np.log(x)-np.log(args[3]))))



def plotFunc(model, plus_minus_sign, lowerBoundary, upperBoundary, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    x = np.linspace(lowerBoundary, upperBoundary, 100)
    y = chooseModel(x, model, plus_minus_sign, a, b, c, d)
    return x, y


def plotFunction(n_clicks, a, b, c, d, plus_minus_sign, model,
                 lowerBoundary, upperBoundary, maxIteration):
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    args = (a, b, c, d)
    lowerBoundary = float(lowerBoundary)
    upperBoundary = float(upperBoundary)
    x, y = plotFunc(model, plus_minus_sign, lowerBoundary, upperBoundary, *args)
    fig = px.line(x=x, y=y)
    return fig, False