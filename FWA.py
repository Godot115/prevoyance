# -*- coding: utf-8 -*-
# @Time    : 7/2/22 15:46
# @Author  : godot
# @FileName: FWA.py
# @Project : prevoyance
# @Software: PyCharm
import sys
import time

import numpy as np

from Cluster.DbScan import DbScan
from DoseResponse.models import model2, model3, model4, model5


def modifiedFWA(lowerBoundary, upperBoundary,
                plus_minus_sign, model,
                grid, *args):
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
    spaceLength = upperBoundary - lowerBoundary
    designPoints = [[lowerBoundary + spaceLength / (4 + 1) * (i + 1), 1 / 4] for i in range(4)]
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=int(grid / 100))
    if model == "Model2":
        model = model2
    elif model == "Model3":
        model = model3
    elif model == "Model4":
        model = model4
    elif model == "Model5":
        model = model5
    spaceLenth = upperBoundary - lowerBoundary
    FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    invFIM = model.inverseInformationMatrix(FIM)
    det_FIM = np.linalg.det(FIM)
    FIM_gain = det_FIM

    i = 4
    start = time.time()
    maxVariance = float('inf')

    while maxVariance - 4 > 0.01:
        i += 1
        maxVariance = float('-inf')
        maxVariancePoint = sys.maxsize
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], invFIM, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        newSpace = np.linspace(
            maxVariancePoint - spaceLenth / 10 if maxVariancePoint - spaceLenth / 10 > lowerBoundary else lowerBoundary,
            maxVariancePoint + spaceLenth / 10 if maxVariancePoint + spaceLenth / 10 < upperBoundary else upperBoundary,
            num=int(grid / 100))
        for k in newSpace:
            dVariance = model.variance(k, invFIM, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = k
        A_point = model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args) * \
                  model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T

        max_gain = float('-inf')
        max_gain_alpha = 0
        for alpha_s in np.linspace(0, 1, num=10000)[1:-1]:
            post_FIM = FIM * (1 - alpha_s) + A_point * alpha_s
            if np.linalg.det(post_FIM) - det_FIM > max_gain:
                max_gain = np.linalg.det(post_FIM) - det_FIM
                max_gain_alpha = alpha_s
        # if (max_gain_alpha == 0):
        #     print(maxVariance)
        designPoints = [[point[0], point[1] * (1 - max_gain_alpha)] for point in designPoints]
        inserted = False
        for idx in range(len(designPoints)):
            if designPoints[idx][0] == maxVariancePoint:
                designPoints[idx][1] += max_gain_alpha
                inserted = True
        if not inserted:
            designPoints.append([maxVariancePoint, max_gain_alpha])
        if i % 40 == 0:
            # print("********")
            designPoints = DbScan(designPoints, lowerBoundary, upperBoundary)
        FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
        invFIM = model.inverseInformationMatrix(FIM)
        FIM_gain = np.linalg.det(FIM) - det_FIM
        det_FIM = np.linalg.det(FIM)
        # print(FIM_gain)
    end = time.time()
    print(end - start)
    print(det_FIM)
    return i


def FWA(lowerBoundary, upperBoundary,
        plus_minus_sign, model,
        grid, *args):
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
    designPoints = [[lowerBoundary + spaceLength / (4 + 1) * (i + 1), 1 / 4] for i in range(4)]
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=grid)
    FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    invFIM = model.inverseInformationMatrix(FIM)
    det_FIM = np.linalg.det(FIM)
    FIM_gain = det_FIM
    i = 4
    maxVariance = float('inf')
    start = time.time()
    maxVariancePoint = sys.maxsize
    designPointsLen = len(designPoints)
    while maxVariance - numOfDesignPoints > 0.01:
        i += 1
        maxVariance = float('-inf')
        maxVariancePoint = sys.maxsize
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], invFIM, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        designPointsLen += 1
        FIM = (1 - 1 / designPointsLen) * FIM + model.vectorOfPartialDerivative(
            maxVariancePoint, plus_minus_sign, *args) * \
              model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T * (1 / designPointsLen)
        invFIM = model.inverseInformationMatrix(FIM)
        FIM_gain = np.linalg.det(FIM) - det_FIM
        det_FIM = np.linalg.det(FIM)
        print(FIM_gain)
    end = time.time()
    print(det_FIM)
    print(end - start)
    return i

def FWAwithAlphaS(lowerBoundary, upperBoundary,
        plus_minus_sign, model,
        grid, *args):
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
    designPoints = [[lowerBoundary + spaceLength / (4 + 1) * (i + 1), 1 / 4] for i in range(4)]
    designSpace = np.linspace(lowerBoundary, upperBoundary, num=grid)
    FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    invFIM = model.inverseInformationMatrix(FIM)
    det_FIM = np.linalg.det(FIM)
    FIM_gain = det_FIM
    i = 4
    maxVariance = float('inf')
    start = time.time()
    maxVariancePoint = sys.maxsize
    while maxVariance - numOfDesignPoints > 0.01:
        i += 1
        maxVariance = float('-inf')
        maxVariancePoint = sys.maxsize
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], invFIM, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]

        A_point = model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args) * \
                  model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T

        max_gain = float('-inf')
        max_gain_alpha = 0
        for alpha_s in np.linspace(0, 1, num=1000)[1:-1]:
            post_FIM = FIM * (1 - alpha_s) + A_point * alpha_s
            if np.linalg.det(post_FIM) - det_FIM > max_gain:
                max_gain = np.linalg.det(post_FIM) - det_FIM
                max_gain_alpha = alpha_s

        FIM = (1 - max_gain_alpha) * FIM + A_point * max_gain_alpha
        invFIM = model.inverseInformationMatrix(FIM)
        FIM_gain = np.linalg.det(FIM) - det_FIM
        det_FIM = np.linalg.det(FIM)
        print(det_FIM,maxVariance)
    end = time.time()
    print(det_FIM)
    print(end - start)
    return i

def FWAwithBack(lowerBoundary, upperBoundary,
                plus_minus_sign, model,
                grid, *args):
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
    designPoints = [[lowerBoundary + spaceLength / (4 + 1) * (i + 1), 1 / 4] for i in range(4)]
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
    FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    invFIM = model.inverseInformationMatrix(FIM)
    det_FIM = np.linalg.det(FIM)
    FIM_gain = det_FIM
    i = 0
    maxVariance = float('inf')
    minVariance = float('-inf')
    maxVariancePoint = sys.maxsize
    minVariancePoint = sys.maxsize
    start = time.time()
    while maxVariance - numOfDesignPoints > 0.01:
        i += 1
        maxVariance = float('-inf')
        minVariance = float('inf')
        maxVariancePoint = sys.maxsize
        minVariancePoint = sys.maxsize
        gamma_s_add = 1 / (numOfDesignPoints + i)

        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], invFIM, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        for sup_point in designPoints:
            dVariance = model.variance(sup_point[0], invFIM, plus_minus_sign, *args)
            if dVariance < minVariance:
                minVariance = dVariance
                minVariancePoint = sup_point[0]
                gamma_s_del = -gamma_s_add if sup_point[1] >= gamma_s_add else -sup_point[1] / (1 - sup_point[1])

        designPoints = [[sup[0], (1 - gamma_s_add - gamma_s_del) * sup[1]] for sup in designPoints]
        added = False
        remove_idx = -1
        for idx in range(len(designPoints)):
            if designPoints[idx][0] == minVariancePoint:
                designPoints[idx][1] += gamma_s_del
                if designPoints[idx][1] == 0:
                    remove_idx = idx
            if designPoints[idx][0] == maxVariancePoint:
                designPoints[idx][1] += gamma_s_add
                added = True
        if not remove_idx == -1:
            designPoints.pop(remove_idx)
        if not added:
            designPoints.append([maxVariancePoint, gamma_s_add])

        FIM = (1 - gamma_s_add - gamma_s_del) * FIM + model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign,
                                                                                      *args) * \
              model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T * \
              gamma_s_add + model.vectorOfPartialDerivative(minVariancePoint, plus_minus_sign, *args) * \
              model.vectorOfPartialDerivative(minVariancePoint, plus_minus_sign, *args).T * \
              gamma_s_del
        invFIM = model.inverseInformationMatrix(FIM)
        FIM_gain = np.linalg.det(FIM) - det_FIM
        det_FIM = np.linalg.det(FIM)
        # print(det_FIM)
    end = time.time()
    print(det_FIM)
    print(end - start)
    return i


grid = 10000
lowerBoundary = 0.01
upperBoundary = 2500
spaceLength = upperBoundary - lowerBoundary
# for k in range(40):
initialPoints = [lowerBoundary + spaceLength / (4 + 1) * (i + 1) for i in range(4)]
a = 349.02687
b = 1067.04343
c = 0.76332
d = 2.60551
args = (a, b, c, d)
FWA(lowerBoundary, upperBoundary,
            "positive", "Model5", grid, *args)
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
