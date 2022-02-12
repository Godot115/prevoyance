import random
import sys
import time
from collections import Counter
from sklearn.cluster import KMeans
import numpy as np

from DoseResponse.models import model2
from DoseResponse.models import model3
from DoseResponse.models import model4
from DoseResponse.models import model5
from DoseResponse.models import testmodel


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


def cluster(newPoint, currentPoints, designSpace):
    """
    add new point to the current points and clustercluster them
    :param newPoint: new point
    :param currentPoints: list of current design points
    :param designSpace: the length of design space
    """
    threshold = designSpace / 50
    for i in range(len(currentPoints)):
        if abs(newPoint - currentPoints[i]) < threshold:
            currentPoints[i] = newPoint
    currentPoints.append(newPoint)
    currentPoints.sort()
    return currentPoints


def delPoint(informationMatrix, point, plus_minus_sign, currentPoints, model, *args):
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
    informationMatrix = (currentPointsNumber / (currentPointsNumber - 1)) * informationMatrix - (
            1 / (currentPointsNumber - 1)) * model.vectorOfPartialDerivative(
        point, plus_minus_sign, *args) * \
                        model.vectorOfPartialDerivative(point, plus_minus_sign, *args).T
    return informationMatrix


def addPoint(informationMatrix, newPoint, currentPoints, model, designSpace, plus_minus_sign,
             *args):
    """
    add a point into design points, return new design points and new information matrix
    :param informationMatrix:
    :param newPoint:
    :param currentPoints:
    :param model:
    :param designSpace:
    :param plus_minus_sign:
    :param args:
    :return:
    """
    threshold = designSpace / 50
    currentPointsNumber = len(currentPoints)
    informationMatrix = ((
                                 currentPointsNumber - 1) / currentPointsNumber) * informationMatrix + model.vectorOfPartialDerivative(
        newPoint, plus_minus_sign, *args) * \
                        model.vectorOfPartialDerivative(newPoint, plus_minus_sign, *args).T * \
                        (1 / currentPointsNumber)
    for i in range(len(currentPoints)):
        if abs(newPoint - currentPoints[i]) < threshold:
            informationMatrix = (currentPointsNumber / (currentPointsNumber - 1)) * informationMatrix - (
                    1 / (currentPointsNumber - 1)) * model.vectorOfPartialDerivative(
                currentPoints[i], plus_minus_sign, *args) * \
                                model.vectorOfPartialDerivative(currentPoints[i], plus_minus_sign, *args).T
            informationMatrix = ((
                                         currentPointsNumber - 1) / currentPointsNumber) * informationMatrix + model.vectorOfPartialDerivative(
                newPoint, plus_minus_sign, *args) * \
                                model.vectorOfPartialDerivative(newPoint, plus_minus_sign, *args).T * \
                                (1 / currentPointsNumber)
            currentPoints[i] = newPoint
    currentPoints.append(newPoint)
    currentPoints.sort()
    return currentPoints, informationMatrix


def createInitialPoints(lowerBoundary, upperBoundary):
    points = list(np.linspace(lowerBoundary, upperBoundary, num=10))
    points.sort()
    return points


def firstOrderTest(designPoints, lowerBoundary, upperBoundary,
               plus_minus_sign, model,
               maxIteration=100, grid=1000, *args):
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
    start = time.time()
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=grid)
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

    initialPoints = []
    for i in designPoints:
        initialPoints.append(i)
    informationMatrix = model.informationMatrix(designPoints, plus_minus_sign, *args)
    invInformationMatrix = model.inverseInformationMatrix(informationMatrix)
    i = 0
    while i < maxIteration:
        if i < 50 and i >= 40:
            if initialPoints[0] in designPoints:
                informationMatrix = delPoint(informationMatrix, initialPoints[0], plus_minus_sign, designPoints, model,
                                             *args)
                designPoints.remove(initialPoints[0])
            initialPoints.remove(initialPoints[0])
            invInformationMatrix = model.inverseInformationMatrix(informationMatrix)
        i += 1
        maxVariance = sys.float_info.min
        maxVariancePoint = random.uniform(0, 1000)
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], invInformationMatrix, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        designPoints, informationMatrix = addPoint(informationMatrix, maxVariancePoint, designPoints, model,
                                                   upperBoundary - lowerBoundary, plus_minus_sign, *args)
        invInformationMatrix = model.inverseInformationMatrix(informationMatrix)

    result = formatResult(designPoints)
    end = time.time()
    print(end - start)
    return result



def firstOrder(designPoints, lowerBoundary, upperBoundary,
               plus_minus_sign, model,
               maxIteration=100, grid=1000, *args):
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
    start = time.time()
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=grid)
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
        #testmodel
    # elif model == "testmodel":
    #     model = testmodel
    #     numOfDesignPoints = 4

    initialPoints = []
    for i in designPoints:
        initialPoints.append(i)
    informationMatrix = model.informationMatrix(designPoints, plus_minus_sign, *args)
    invInformationMatrix = model.inverseInformationMatrix(informationMatrix)
    i = 0
    while i < maxIteration:
        if i < 50 and i >= 40:
            if initialPoints[0] in designPoints:
                informationMatrix = delPoint(informationMatrix, initialPoints[0], plus_minus_sign, designPoints, model,
                                             *args)
                designPoints.remove(initialPoints[0])
            initialPoints.remove(initialPoints[0])
            invInformationMatrix = model.inverseInformationMatrix(informationMatrix)
        i += 1
        maxVariance = sys.float_info.min
        maxVariancePoint = random.uniform(0, 1000)
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], invInformationMatrix, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]

        currentPointsNumber = len(designPoints)
        informationMatrix  = ((
                                 currentPointsNumber - 1) / currentPointsNumber) * informationMatrix + model.vectorOfPartialDerivative(
        maxVariancePoint, plus_minus_sign, *args) * \
                        model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T * \
                        (1 / currentPointsNumber)
        designPoints.append(maxVariancePoint)
        invInformationMatrix = model.inverseInformationMatrix(informationMatrix)

    designPoints = [[i] for i in designPoints]
    km = KMeans(n_clusters=numOfDesignPoints, max_iter=1000).fit(designPoints)
    designPoints = km.cluster_centers_
    designPoints = [i[0] for i in designPoints]
    designPoints.sort()
    result = formatResult(designPoints)
    end = time.time()
    print(end - start)

    return result


def calculateInformationMatrix(designPoints, plus_minus_sign, model, *args):
    if model == "Model2":
        model = model2
    elif model == "Model3":
        model = model3
    elif model == "Model4":
        model = model4
    elif model == "Model5":
        model = model5
        #testmodel
    # elif model == "testmodel":
    #     model = testmodel

    informationMatrix = model.informationMatrix(designPoints, plus_minus_sign, *args)
    return informationMatrix
