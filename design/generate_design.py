# -*- coding: utf-8 -*-
# @Time    : 3/9/22 00:34
# @Author  : godot
# @FileName: generate_design.py
# @Project : prevoyance
# @Software: PyCharm

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from DoseResponse import FirstOrder
from DoseResponse.models import model2
from DoseResponse.models import model3
from DoseResponse.models import model4
from DoseResponse.models import model5


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
    points = FirstOrder.createInitialPoints(lowerBoundary, upperBoundary, model)
    result = FirstOrder.firstOrder(points, lowerBoundary, upperBoundary, plus_minus_sign, model, maxIteration,
                                   *args)
    # print(result)
    plotEquivalence(result, lowerBoundary, upperBoundary, plus_minus_sign, model, *args)
    result = dict(result)
    result = pd.DataFrame(list(result.items()),
                          columns=['Point', 'Weight'])
    return result.to_dict('records'), [{'name': i, 'id': i} for i in result.columns], False


def plotEquivalence(result, lowerBoundary, upperBoundary, plus_minus_sign, model, *args):
    """
    First order alrogithm
    :param designPoints:
    :param lowerBoundary:
    :param upperBoundary:
    :param model:
    :param maxIteration:
    :param grid:
    :param args:
    :return:
    """
    result = [i[0] for i in result]
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=100)
    if model == "Model2":
        model = model2
    elif model == "Model3":
        model = model3
    elif model == "Model4":
        model = model4
    elif model == "Model5":
        model = model5
    plt.rcParams['font.sans-serif'] = ['Heiti TC']
    plt.rcParams['axes.unicode_minus'] = False
    InvInf = model.inverseInformationMatrix(model.informationMatrix(result, plus_minus_sign, *args))
    x = []
    y = []
    for i in designSpace:
        x.append(i)
        y.append(model.variance(i, InvInf, plus_minus_sign, *args))
    plt.xlabel('实验区间', fontsize=15)
    plt.ylabel('方差', fontsize=15)
    plt.plot(x, y)
    plt.savefig('plot.png')

# a = 349.02687
# b = 1067.04343
# c = 0.76332
# d = 2.60551
# args = (a, b, c, d)
# maxIteration = 100
# lowerBoundary = 0.001
# upperBoundary = 2500.0
# points = FirstOrder.createInitialPoints(lowerBoundary,upperBoundary,"Model5")
# result = FirstOrder.firstOrder(points, lowerBoundary, upperBoundary, "positive", "Model5", maxIteration,
#                                *args)
# # print(result)
# plotEquivalence(result, lowerBoundary, upperBoundary, "positive", "Model5", *args)
# result = dict(result)
# result = pd.DataFrame(list(result.items()),
#                       columns=['Point', 'Weight'])
