# -*- coding: utf-8 -*-
# @Time    : 9/6/22 06:21
# @Author  : godot
# @FileName: TimeTest.py
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
    designPoints = [[lowerBoundary + spaceLength / (grid + 1) * (i + 1), 1 / grid] for i in range(grid)]
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
    fim = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    inv_fim = model.inverseInformationMatrix(fim)
    det_fim = np.linalg.det(fim)
    fim_gain = det_fim

    i = 4
    start = time.time()
    maxVariance = float('inf')
    time_recorder = []
    det_fim_recorder = []
    while fim_gain > 0.01:
        i += 1
        maxVariance = float('-inf')
        maxVariancePoint = sys.maxsize
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], inv_fim, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        newSpace = np.linspace(
            maxVariancePoint - spaceLenth / 10 if maxVariancePoint - spaceLenth / 10 > lowerBoundary else lowerBoundary,
            maxVariancePoint + spaceLenth / 10 if maxVariancePoint + spaceLenth / 10 < upperBoundary else upperBoundary,
            num=int(grid / 100))
        for k in newSpace:
            dVariance = model.variance(k, inv_fim, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = k
        A_point = model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args) * \
                  model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T

        max_gain = float('-inf')
        max_gain_alpha = 0
        for alpha_s in np.linspace(0, 1, num=10000)[1:-1]:
            post_fim = fim * (1 - alpha_s) + A_point * alpha_s
            if np.linalg.det(post_fim) - det_fim > max_gain:
                max_gain = np.linalg.det(post_fim) - det_fim
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
        fim = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
        inv_fim = model.inverseInformationMatrix(fim)
        fim_gain = np.linalg.det(fim) - det_fim
        det_fim = np.linalg.det(fim)
        # print(fim_gain)
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)

    time_recorder = np.array(time_recorder)
    det_fim_recorder = np.array(det_fim_recorder)
    # np.save("MFWA_"+TIME_FILE_NAME, time_recorder)
    # np.save("MFWA_"+DET_FILE_NAME, det_fim_recorder)

    end = time.time()
    print("*********  modifiedFWA  *************")
    print(det_fim)
    print(end - start)
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
    spaceLength = upperBoundary - lowerBoundary
    designPoints = [[lowerBoundary + spaceLength / (grid + 1) * (i + 1), 1 / grid] for i in range(grid)]
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
    time_recorder = []
    det_fim_recorder = []
    while fim_gain > 0.01:
        i += 1
        maxVariance = float('-inf')
        maxVariancePoint = sys.maxsize
        for j in range(len(designSpace)):
            dVariance = model.variance(designSpace[j], inv_fim, plus_minus_sign, *args)
            if dVariance > maxVariance:
                maxVariance = dVariance
                maxVariancePoint = designSpace[j]
        designPointsLen += 1
        fim = (1 - 1 / designPointsLen) * fim + model.vectorOfPartialDerivative(
            maxVariancePoint, plus_minus_sign, *args) * \
              model.vectorOfPartialDerivative(maxVariancePoint, plus_minus_sign, *args).T * (1 / designPointsLen)
        inv_fim = model.inverseInformationMatrix(fim)
        fim_gain = np.linalg.det(fim) - det_fim
        det_fim = np.linalg.det(fim)
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)

    time_recorder = np.array(time_recorder)
    det_fim_recorder = np.array(det_fim_recorder)
    # np.save("FWA_"+TIME_FILE_NAME, time_recorder)
    # np.save("FWA_"+DET_FILE_NAME, det_fim_recorder)

    end = time.time()
    print("*********  FWA  *************")

    print(det_fim)
    print(end - start)
    return i


def Multiplicative(lowerBoundary, upperBoundary,
                   plus_minus_sign, model,
                   grid, *args):
    if model == "Model2":
        model = model2
    elif model == "Model3":
        model = model3
    elif model == "Model4":
        model = model4
    elif model == "Model5":
        model = model5

    spaceLength = upperBoundary - lowerBoundary
    designPoints = [[lowerBoundary + spaceLength / (grid + 1) * (i + 1), 1 / grid] for i in range(grid)]
    fim = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    det_fim = np.linalg.det(fim)
    start = time.time()
    fim_gain = det_fim
    variances = [0] * grid
    time_recorder = []
    det_fim_recorder = []
    while fim_gain > 0.01:
        denominator = 0
        inv_fim = np.linalg.inv(fim)
        for idx in range(len(designPoints)):
            variances[idx] = model.variance(designPoints[idx][0], inv_fim, plus_minus_sign, *args)
            denominator += designPoints[idx][1] * variances[idx]
        for idx in range(len(designPoints)):
            designPoints[idx][1] *= variances[idx] / denominator
        weight_sum = 0
        for point_j in iter(designPoints):
            weight_sum += point_j[1]
        fim = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
        fim_gain = np.linalg.det(fim) - det_fim
        det_fim = np.linalg.det(fim)
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)

    time_recorder = np.array(time_recorder)
    det_fim_recorder = np.array(det_fim_recorder)
    # np.save("MA_"+TIME_FILE_NAME, time_recorder)
    # np.save("MA_"+DET_FILE_NAME, det_fim_recorder)

    end = time.time()
    print("*********  Multiplicative  *************")
    print(det_fim)
    print(end - start)


TIME_FILE_NAME = ""
DET_FILE_NAME = ""
a = 349.02687
b = 1067.04343
c = 0.76332
d = 2.60551
args = (a, b, c, d)
grid_conditions = [1000, 10000, 100000]
models = ["Model2", "Model3", "Model4", "Model5"]
for grid in grid_conditions:
    for model in models:
        print("####################################################################")
        print("grid:", grid, "Model:", model)
        print()
        TIME_FILE_NAME = "Time_" + str(grid) + "_" + model
        DET_FILE_NAME = "Det_" + str(grid) + "_" + model
        modifiedFWA(0.01, 2500,
                    "positive", model,
                    grid, *args)
        FWA(0.01, 2500,
            "positive", model,
            grid, *args)

        Multiplicative(0.01, 2500,
                       "positive", model,
                       grid, *args)
