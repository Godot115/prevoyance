# -*- coding: utf-8 -*-
# @Time    : 9/23/22 23:22
# @Author  : godot
# @FileName: CA.py
# @Project : prevoyance
# @Software: PyCharm

import sys
import time

import numpy as np

from DoseResponse.models import model2, model3, model4, model5


def CA(lowerBoundary, upperBoundary,
       plus_minus_sign, model,
       grid, *args):
    """
    Combined Algorithm
    :param designPoints:
    :param lowerBoundary:
    :param upperBoundary:
    :param model:
    :param maxIteration:
    :param grid:
    :param args:
    :return:
    """

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

    designPoints = [[lowerBoundary + spaceLength / (numOfDesignPoints + 1) * (i + 1), 1 / numOfDesignPoints] for i in
                    range(numOfDesignPoints)]
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=grid)
    fim = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    inv_fim = model.inverseInformationMatrix(fim)
    det_fim = np.linalg.det(fim)
    fim_gain = det_fim
    i = 4
    maxVariance = float('inf')
    start = time.time()
    maxVariancePoint = sys.maxsize
    designPointsLen = len(designPoints)
    while fim_gain > 0.00001 * (det_fim - fim_gain):
        i += 1
        maxVariance = float('-inf')
        maxVariancePoint = sys.maxsize
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], inv_fim, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        designPoints = [[sup_points[0], sup_points[1] * (designPointsLen / (designPointsLen + 1))] for sup_points in
                        designPoints]
        designPoints.append([maxVariancePoint, 1 / (designPointsLen + 1)])
        designPointsLen = len(designPoints)
        fim = (1 - 1 / designPointsLen) * fim + model.vectorOfPartialDerivative(
            maxVariancePoint, plus_minus_sign, *args) * \
              model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T * (1 / designPointsLen)
        inv_fim = model.inverseInformationMatrix(fim)
        # FIM_gain = np.linalg.det(FIM) - det_FIM
        # det_FIM = np.linalg.det(FIM)
        # Determine the optimal weights
        denominator = 0
        variances = [0] * len(designPoints)
        for idx in range(len(designPoints)):
            variances[idx] = model.variance(designPoints[idx][0], inv_fim, plus_minus_sign, *args)
            denominator += designPoints[idx][1] * variances[idx]
        for idx in range(len(designPoints)):
            designPoints[idx][1] *= variances[idx] / denominator

        fim = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
        inv_fim = model.inverseInformationMatrix(fim)
        temp_fim = np.linalg.det(fim)
        fim_gain = temp_fim - det_fim
        det_fim = temp_fim
    end = time.time()
    print(det_fim)
    print(end - start)
    return i


# grid = 10000
# lowerBoundary = 0.01
# upperBoundary = 2500
# spaceLength = upperBoundary - lowerBoundary
# # for k in range(40):
# initialPoints = [lowerBoundary + spaceLength / (4 + 1) * (i + 1) for i in range(4)]
# a = 349.02687
# b = 1067.04343
# c = 0.76332
# d = 2.60551
# args = (a, b, c, d)
# CA(lowerBoundary, upperBoundary,
#    "positive", "Model5", grid, *args)
# import matplotlib.pyplot as plot
# import numpy as np
#
# x_val = list(range(1, 50))
# # y的值是x的平方
# y_val = [x ** 2 for x in x_val]
# # 设置x轴
# plot.xlabel("x", fontsize=12)
# # 设置y轴
# plot.ylabel("y", fontsize=12)
# plot.ylim(-0.1, 0.2)
# # 散点
# plot.scatter([0.01, 1480.1, 1590.0, 1500.3, 1510.5, 1989.2, 1990.9, 1995.9, 2000.0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
#              color='black')
# # 显示
# plot.show()
