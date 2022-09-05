# -*- coding: utf-8 -*-
# @Time    : 9/25/22 17:47
# @Author  : godot
# @FileName: Cocktail.py
# @Project : prevoyance
# @Software: PyCharm
import sys
import time

import numpy as np

from DoseResponse.models import model2, model3, model4, model5


def Cocktail(lo_bound, up_bound,
             plus_minus_sign, model,
             grid, *args):
    model_name = model
    algorithm = 'FWAwithAlphaS'
    min_sup_points = 0
    if model == "Model2":
        model = model2
        min_sup_points = 2
        model_name = 2
    elif model == "Model3":
        model = model3
        min_sup_points = 3
        model_name = 3
    elif model == "Model4":
        model = model4
        min_sup_points = 3
        model_name = 4
    elif model == "Model5":
        model = model5
        min_sup_points = 4
        model_name = 5

    space_len = up_bound - lo_bound
    design_points = [[lo_bound + space_len / (min_sup_points + 1) * (i + 1), 1 / (min_sup_points)] for i
                     in
                     range(min_sup_points)]
    design_space = np.linspace(lo_bound, up_bound, num=grid)

    fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
    inv_fim = model.inverseInformationMatrix(fim)
    det_fim = np.linalg.det(fim)
    fim_gain = det_fim

    iteration = 0
    start = time.time()
    time_recorder = []
    det_fim_recorder = []
    threshold = 1e-5
    det_fim_gain = float('inf')
    while det_fim_gain / det_fim > threshold:

        iteration += 1
        max_variance = float('-inf')
        max_variance_point = sys.maxsize
        for j in range(len(design_space)):
            d_variance = model.variance(design_space[j], inv_fim, plus_minus_sign, *args)
            if d_variance > max_variance:
                max_variance = d_variance
                max_variance_point = design_space[j]
        # print(max_variance)

        A_point = model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args) * \
                  model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args).T
        alpha_s = ((max_variance / min_sup_points) - 1) / (max_variance - 1)
        design_points = [[point[0], point[1] * (1 - alpha_s)] for point in design_points]
        design_points.append([max_variance_point, alpha_s])
        fim = (1 - alpha_s) * fim + alpha_s * A_point
        inv_fim = model.inverseInformationMatrix(fim)

        for idx in range(len(design_points) - 1):
            if design_points[idx] == None:
                continue
            # if (design_points[idx + 1][0] - design_points[idx][0]) < (space_len / 1000):
            if True:

                delta = VertexExchangeDelta(idx, idx + 1, design_points, model, inv_fim, plus_minus_sign, *args)
                # print(design_points[idx][1], design_points[idx + 1][1], delta)
                w_i = design_points[idx][1]
                w_j = design_points[idx + 1][1]
                x_i = design_points[idx][0]
                x_j = design_points[idx + 1][0]
                variance_xi = model.variance(x_i, inv_fim, plus_minus_sign, *args)
                variance_xj = model.variance(x_j, inv_fim, plus_minus_sign, *args)
                variance_xi_xj = model.combinedVariance(x_i, x_j, inv_fim, plus_minus_sign, *args)
                delta_i_j = (variance_xi - variance_xj) / 2 * (
                        variance_xi_xj * variance_xi_xj - variance_xj * variance_xi)
                delta = min(w_i, max(-w_j, delta_i_j))

                steps = np.linspace(-w_j, w_i, 100000)
                A_i = model.vectorOfPartialDerivative(design_points[idx][0], plus_minus_sign, *args) * \
                      model.vectorOfPartialDerivative(design_points[idx][0], plus_minus_sign,
                                                      *args).T
                A_j = model.vectorOfPartialDerivative(design_points[idx + 1][0], plus_minus_sign, *args) * \
                      model.vectorOfPartialDerivative(design_points[idx + 1][0], plus_minus_sign, *args).T

                opt_step = 0
                opt_det_fim = np.linalg.det(fim)
                for step in steps:
                    new_fim = fim + step * A_j - step * A_i
                    if np.linalg.det(new_fim) > opt_det_fim:
                        opt_det_fim = np.linalg.det(new_fim)
                        opt_step = step

                print(opt_step, delta)
                # print(delta, w_i, w_j)
                design_points[idx][1] -= opt_step
                design_points[idx + 1][1] += opt_step
                # print(delta, opt_step)
                # fim = fim - opt_step * model.vectorOfPartialDerivative(design_points[idx][0], plus_minus_sign, *args) * \
                #       model.vectorOfPartialDerivative(design_points[idx][0], plus_minus_sign,
                #                                       *args).T + opt_step * model.vectorOfPartialDerivative(
                #     design_points[idx + 1][0], plus_minus_sign, *args) * \
                #       model.vectorOfPartialDerivative(design_points[idx + 1][0], plus_minus_sign, *args).T
                fim = fim + opt_step * A_j - opt_step * A_i
                inv_fim = np.linalg.inv(fim)
                if design_points[idx][1] == 0:
                    design_points[idx] = None
                if design_points[idx + 1][1] == 0:
                    design_points[idx + 1] = None

        design_points = list(filter(None, design_points))

        denominator = 0
        variances = [0] * len(design_points)
        for idx in range(len(design_points)):
            variances[idx] = model.variance(design_points[idx][0], inv_fim, plus_minus_sign, *args)
            denominator += design_points[idx][1] * variances[idx]
        for idx in range(len(design_points)):
            design_points[idx][1] *= variances[idx] / denominator
        fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
        inv_fim = model.inverseInformationMatrix(fim)
        det_fim_gain = np.linalg.det(fim) - det_fim
        det_fim = np.linalg.det(fim)
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)
        print(det_fim)
    print("det:", det_fim, time.time() - start)


def VertexExchangeDelta(idx_i, idx_j, design_points, model, inv_fim, plus_minus_sign, *args):
    x_i = design_points[idx_i][0]
    x_j = design_points[idx_j][0]
    w_i = design_points[idx_i][1]
    w_j = design_points[idx_j][1]
    variance_xi = model.variance(x_i, inv_fim, plus_minus_sign, *args)
    variance_xj = model.variance(x_j, inv_fim, plus_minus_sign, *args)
    variance_xi_xj = model.combinedVariance(x_i, x_j, inv_fim, plus_minus_sign, *args)
    delta_i_j = (variance_xj - variance_xi) / 2 * (variance_xj * variance_xi - variance_xi_xj * variance_xi_xj)
    delta = min(w_i, max(-w_j, delta_i_j))
    return delta


# a = 349.02687
# b = 1067.04343
# c = 0.76332
# d = 2.60551
#
# args = (a, b, c, d)
#
# grid_conditions = [20, 50, 1000, 5000, 10000, 50000, 100000]
#
# models = ["Model2", "Model3", "Model4", "Model5"]
# #
# low_high_list = [(0.01, 2500.0), (0.01, 1200.0)]
#
# for low_high in low_high_list:
#     low = low_high[0]
#     high = low_high[1]
#
#     for grid in grid_conditions:
#         # print("####################################################################")
#         # print("grid:", grid, "------")
#         for model in models:
#             # print("Model:", model)
#             # print()
#
#             # try:
#             # modifiedFWA(low, high,
#             #             "neg", model,
#             #             grid, *args)
#             # modifiedFWATest(low, high,
#             #                 "neg", model,
#             #                 grid, *args)
#             # CA(low, high,
#             #    "neg", model,
#             #    grid, *args)
#             #
#             # FWAwithAlphaS(low, high,
#             #               "neg", model,
#             #               grid, *args)
#             # Multiplicative(low, high,
#             #                "neg", model,
#             #                grid, *args)
#             Cocktail(low, high,
#                      "neg", model,
#                      grid, *args)
#         # except BaseException:
#         #     print(BaseException)
# # db.close()
