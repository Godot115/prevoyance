# -*- coding: utf-8 -*-
# @Time    : 3/9/22 02:17
# @Author  : godot
# @FileName: calculate_bayesian_design.py
# @Project : prevoyance
# @Software: PyCharm
import random
import sys
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from DoseResponse.models import model2
from DoseResponse.models import model3
from DoseResponse.models import model4
from DoseResponse.models import model5


def formatResult(designPoints):
    """
    format the result into a list of tuples
    :param designPoints:
    :return:
    """
    designPoints = Counter(designPoints)
    designPoints = designPoints.items()
    numbers = 0
    for i in designPoints:
        numbers += i[1]
    result = []
    for i in designPoints:
        result.append((round(i[0], 3), round(i[1] / numbers, 3)))
    return result


def infoMAT(designPoints, param, model, plus_minus):
    numOfPoints = len(designPoints)
    paramNum = len(param[0])
    # if model == 'Model2':
    #     model = model2
    # elif model == 'Model3':
    #     model = model3
    # elif model == 'Model4':
    #     model = model4
    # elif model == 'Model5':
    #     model = model5
    result = np.zeros((paramNum, paramNum))
    for i in param:
        # result += model.informationMatrixWithWeight(designPoints, plus_minus, *i) / paramNum
        result += model.informationMatrix(designPoints, plus_minus, *i) / paramNum
    return result


def createInitialPoints(lowerBoundary, upperBoundary):
    points = list(np.linspace(lowerBoundary, upperBoundary, num=10))
    points.sort()
    return points


def delPoint(informationMatrix, point, plus_minus_sign, currentPoints, model, param):
    """
    delete a point from design points, return new information matrix
    :param informationMatrix:
    :param point:
    :param plus_minus_sign:
    :param currentPoints:
    :param model:
    :return:
    """
    currentPointsNumber = len(currentPoints)
    for i in param:
        informationMatrix += (currentPointsNumber / (currentPointsNumber - 1)) * informationMatrix - (
                1 / (currentPointsNumber - 1)) * model.vectorOfPartialDerivative(
            point, plus_minus_sign, *i) * \
                             model.vectorOfPartialDerivative(point, plus_minus_sign, *i).T / len(param)
    return informationMatrix


def variance(model, inverseInformationMatrix, newPoint, plus_minus, param):
    # if model == 'Model2':
    #     model = model2
    # elif model == 'Model3':
    #     model = model3
    # elif model == 'Model4':
    #     model = model4
    # elif model == 'Model5':
    #     model = model5
    variance = 0
    for i in param:
        variance += model.variance(newPoint, inverseInformationMatrix, plus_minus, *i) / len(param)
    return variance


def firstOrder(param, model: str, plus_minus, lowerBoundary, upperBoundary, maxIteration=100):
    numOfDesignPoints = 0
    if model == "Model2":
        model = model2
        numOfDesignPoints = 2
    elif model == "Model3":
        model = model3
        numOfDesignPoints = 3
    elif model == "Model4":
        model = model4
        numOfDesignPoints = 3
    elif model == "Model5":
        model = model5
        numOfDesignPoints = 4
    spaceLenth = upperBoundary - lowerBoundary
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=100)
    initialPoints = createInitialPoints(lowerBoundary, upperBoundary)
    informationMatrix = infoMAT(initialPoints, param, model, plus_minus)
    invInformationMatrix = np.linalg.inv(informationMatrix)
    designPoints = []
    for i in initialPoints:
        designPoints.append(i)
    i = 0
    while i < maxIteration:
        if i < 50 and i >= 40:
            if designPoints[0] in initialPoints:
                informationMatrix = delPoint(informationMatrix, initialPoints[0], plus_minus, designPoints, model,
                                             param)
                initialPoints.remove(designPoints[0])
            designPoints.remove(designPoints[0])
            invInformationMatrix = np.linalg.inv(informationMatrix)
        i += 1
        maxVariance = sys.float_info.min
        maxVariancePoint = random.uniform(0, 1000)
        for j in range(len(designSpace)):
            dVariance = variance(model, invInformationMatrix, designSpace[j], plus_minus, param)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]

        newSpace = np.linspace(
            maxVariancePoint - spaceLenth / 10 if maxVariancePoint - spaceLenth / 10 > lowerBoundary else lowerBoundary,
            maxVariancePoint + spaceLenth / 10 if maxVariancePoint + spaceLenth / 10 < upperBoundary else upperBoundary,
            num=100)

        for k in newSpace:
            dVariance = variance(model, invInformationMatrix, designSpace[j], plus_minus, param)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = k

        currentPointsNumber = len(designPoints)
        for pa in param:
            informationMatrix = ((
                                         currentPointsNumber - 1) / currentPointsNumber) * informationMatrix + model.vectorOfPartialDerivative(
                maxVariancePoint, plus_minus, *pa) * \
                                model.vectorOfPartialDerivative(maxVariancePoint, plus_minus, *pa).T * \
                                (1 / currentPointsNumber) / len(param)
            designPoints.append(maxVariancePoint)
            invInformationMatrix = model.inverseInformationMatrix(informationMatrix)
    # variance(model, inverseInformationMatrix, newPoint, plus_minus, param):
    designPoints = [[i] for i in designPoints]
    km = KMeans(n_clusters=numOfDesignPoints, max_iter=1000).fit(designPoints)
    designPoints = km.cluster_centers_
    designPoints = [i[0] for i in designPoints]
    designPoints.sort()
    result = formatResult(designPoints)
    return result


def GenerateBayesian(parameter, model, plus_minus_sign, lowerBoundary, upperBoundary, maxIteration, n_clicks):
    lowerBoundary = float(lowerBoundary)
    upperBoundary = float(upperBoundary)
    points = createInitialPoints(lowerBoundary, upperBoundary)
    result = firstOrder(parameter, model, plus_minus_sign, lowerBoundary, upperBoundary, maxIteration)
    result = dict(result)
    result = pd.DataFrame(list(result.items()),
                          columns=['Point', 'Weight'])
    return result.to_dict('records'), [{'name': i, 'id': i} for i in result.columns], False

# if __name__ == '__main__':
#     # model = 'Model2'
#     # param = [(349.02687, 1067.04343), (311.02687, 1000.04343)]
#     model = 'Model5'
#     param = [(349.02687, 1067.04343, 0.76332, 2.60551), (349.02687, 1067.04343, 0.76332, 2.60551)]
#
#     plus_minus = 'negative'
#     lowerBoundary = 0.01
#     upperBoundary = 2500.0
#     maxIteration = 100
#     print(param)
#     print(model)
#     print(plus_minus)
#     print(lowerBoundary)
#     print(upperBoundary)
#     print(maxIteration)
#
#     firstOrder(param, model, plus_minus, lowerBoundary, upperBoundary, maxIteration, grid=1000)
