# -*- coding: utf-8 -*-
# @Time    : 7/28/22 18:44
# @Author  : godot
# @FileName: MFEA.py
# @Project : prevoyance
# @Software: PyCharm
import time

import numpy as np

from DoseResponse.models import model2
from DoseResponse.models import model3
from DoseResponse.models import model4
from DoseResponse.models import model5


def modifiedFE(designPoints, lowerBoundary, upperBoundary,
               plus_minus_sign, model,
               maxIteration=100, grid=100, *args):
    if model == "Model2":
        model = model2
        support_nums = 2
    elif model == "Model3":
        model = model3
        support_nums = 3
    elif model == "Model4":
        model = model4
        support_nums = 3
    elif model == "Model5":
        model = model5
        support_nums = 4

    spaceLength = upperBoundary - lowerBoundary
    design_set = [lowerBoundary + spaceLength / (support_nums + 1) * (i + 1) for i in
                  range(support_nums)]

    candidate_set = [lowerBoundary + spaceLength / (grid + 1) * (i + 1) for i in range(grid)]
    flag = True
    start = time.time()
    while flag:
        flag = False
        for x_i in design_set:
            FIM = model.informationMatrix(design_set, plus_minus_sign, *args)
            invFIM = model.inverseInformationMatrix(FIM)
            det_FIM = np.linalg.det(FIM)
            print(det_FIM)
            # if det_FIM > 283.55732804825425:
            #     flag = False
            #     break
            dxi = model.variance(x_i, invFIM, plus_minus_sign, *args)
            max_delta_xi_xj = float('-inf')
            max_couple = ()
            for x_j in candidate_set:
                dxj = model.variance(x_j, invFIM, plus_minus_sign, *args)
                d_xi_xj = model.combinedVariance(x_i, x_j, invFIM, plus_minus_sign, *args)
                delta_xi_xj = dxj - (dxi * dxj - d_xi_xj * d_xi_xj) - dxi
                if delta_xi_xj > max_delta_xi_xj:
                    max_delta_xi_xj = delta_xi_xj
                    max_couple = (x_i, x_j)
            if max_delta_xi_xj > 0:
                design_set[design_set.index(max_couple[0])] = max_couple[1]
                flag = True
    end = time.time()
    print(det_FIM)
    print(end - start)


modifiedFE([1, 1, 1, 1], 0.001, 2500, "positive", "Model5", 10000, 10000, *(349.02687, 1067.04343, 0.76332, 2.60551))
