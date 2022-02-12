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
    else:
        return a * (c - (c - 1) * np.exp(-(x / b) ** d))


def plotFunc(model, plus_minus_sign, lowerBoundary, upperBoundary, *args):
    print(args)
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    x = np.linspace(lowerBoundary, upperBoundary, 100)
    y = chooseModel(x, model, plus_minus_sign, a, b, c, d)
    return x, y
