# -*- coding: utf-8 -*-
# @Time    : 7/24/22 22:54
# @Author  : godot
# @FileName: Multiplicative.py
# @Project : prevoyance
# @Software: PyCharm
import time

import numpy as np

from DoseResponse.models import model2
from DoseResponse.models import model3
from DoseResponse.models import model4
from DoseResponse.models import model5


def Multiplicative(lowerBoundary, upperBoundary,
                   plus_minus_sign, model,
                   grid=100, *args):
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
    FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
    det_FIM = np.linalg.det(FIM)
    start = time.time()
    FIM_gain = det_FIM
    variances = [0] * grid
    while FIM_gain > 0.01:
        denominator = 0
        inv_fim = np.linalg.inv(FIM)
        for idx in range(len(designPoints)):
            variances[idx] = model.variance(designPoints[idx][0], inv_fim, plus_minus_sign, *args)
            denominator += designPoints[idx][1] * variances[idx]
        for idx in range(len(designPoints)):
            designPoints[idx][1] *= variances[idx] / denominator
        weight_sum = 0
        for point_j in iter(designPoints):
            weight_sum += point_j[1]
        FIM = model.informationMatrixWithWeight(designPoints, plus_minus_sign, *args)
        FIM_gain = np.linalg.det(FIM) - det_FIM
        det_FIM = np.linalg.det(FIM)
    end = time.time()
    print(det_FIM)
    print(end - start)


# Multiplicative(1, 2500, "positive", "Model5", 10000, *(349.02687, 1067.04343, 0.76332, 2.60551))
