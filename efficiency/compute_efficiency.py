# -*- coding: utf-8 -*-
# @Time    : 3/9/22 00:31
# @Author  : godot
# @FileName: compute_efficiency.py
# @Project : prevoyance
# @Software: PyCharm
import numpy as np
from dash import html

from DoseResponse import FirstOrder


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
    initialpoints = FirstOrder.createInitialPoints(lowerBoundary, upperBoundary, model)
    optimalDesignPoints = FirstOrder.firstOrder(initialpoints, lowerBoundary, upperBoundary, plus_minus_sign,
                                                model,
                                                maxIteration,
                                                *args)

    optimalDesignPoints = [(0.01 if i[0] - 0 <= 1e-2 else float(i[0]), float(i[1])) for i in
                           optimalDesignPoints]
    currentDesignPoints = [(0.01 if i[0] - 0 <= 1e-2 else float(i[0]), float(i[1])) for i in
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
    return html.Div([
        html.Br(),
        html.B("D-Efficiency of proposed design: "),
        str(efficiency)])
