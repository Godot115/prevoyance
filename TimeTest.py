# -*- coding: utf-8 -*-
# @Time    : 9/6/22 06:21
# @Author  : godot
# @FileName: TimeTest.py
# @Project : prevoyance
# @Software: PyCharm
import math
import sys
import time

import numpy as np
import pymysql

from Cluster.DbScan import DbScan
from DoseResponse.models import model2, model3, model4, model5


# def modifiedFWA(lo_bound, up_bound,
#                 plus_minus_sign, model,
#                 grid, *args):
#     """
#     First order alrogithm
#     :param design_points:
#     :param lo_bound:
#     :param up_bound:
#     :param model:
#     :param max_iter:
#     :param grid:
#     :param args:
#     :return:
#     """
#     algorithm = 'modifiedFWA'
#     model_name = model
#     min_sup_points = 0
#     if model == "Model2":
#         model = model2
#         min_sup_points = 2
#         model_name = 2
#     elif model == "Model3":
#         model = model3
#         min_sup_points = 3
#         model_name = 3
#     elif model == "Model4":
#         model = model4
#         min_sup_points = 3
#         model_name = 4
#     elif model == "Model5":
#         model = model5
#         min_sup_points = 4
#         model_name = 5
#
#     space_len = up_bound - lo_bound
#     design_points = [[lo_bound + space_len / (min_sup_points + 1) * (i + 1), 1 / min_sup_points] for i
#                      in
#                      range(min_sup_points)]
#     design_space = np.linspace(lo_bound, up_bound, num=math.ceil(math.sqrt(grid)))
#
#     fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
#     inv_fim = model.inverseInformationMatrix(fim)
#     det_fim = np.linalg.det(fim)
#
#     iteration = 0
#     start = time.time()
#     time_recorder = []
#     det_fim_recorder = []
#     threshold = 1e-6
#     det_fim_gain = float('inf')
#     while det_fim_gain / det_fim > threshold:
#         iteration += 1
#         max_variance = float('-inf')
#         max_variance_point = sys.maxsize
#         for j in range(len(design_space)):
#             dVariance = model.variance(design_space[j], inv_fim, plus_minus_sign, *args)
#             if dVariance > max_variance:
#                 max_variance = dVariance
#                 max_variance_point = design_space[j]
#         new_design_space = np.linspace(
#             max_variance_point - space_len / 10 if max_variance_point - space_len / 10 > lo_bound else lo_bound,
#             max_variance_point + space_len / 10 if max_variance_point + space_len / 10 < up_bound else up_bound,
#             num=math.ceil(math.sqrt(grid)))
#         for k in new_design_space:
#             dVariance = model.variance(k, inv_fim, plus_minus_sign, *args)
#             if dVariance > max_variance:
#                 max_variance = dVariance
#                 max_variance_point = k
#         A_point = model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args) * \
#                   model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args).T
#
#         # max_post_det_fim = float('-inf')
#         # alpha_s = 0
#         # for alpha in np.linspace(0, 1, num=1000)[1:-1]:
#         #     post_fim = fim * (1 - alpha) + A_point * alpha
#         #     if np.linalg.det(post_fim) > max_post_det_fim:
#         #         max_post_det_fim = np.linalg.det(post_fim)
#         #         alpha_s = alpha
#         alpha_s = ((max_variance / min_sup_points) - 1) / (max_variance - 1)
#         if alpha_s > 0:
#             design_points = [[point[0], point[1] * (1 - alpha_s)] for point in design_points]
#             design_points.append([max_variance_point, alpha_s])
#         elif alpha_s < 0:
#             for idx in range(len(design_points)):
#                 if design_points[idx][0] == max_variance_point:
#                     design_points[idx][1] += alpha_s
#                 else:
#                     design_points[idx][1] *= (1 - alpha_s)
#
#         fim = (1 - alpha_s) * fim + alpha_s * A_point
#         if len(design_points) % (min_sup_points * 10) == 0:
#             # print("********")
#             design_points = DbScan(design_points, lo_bound, up_bound)
#             fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
#             inv_fim = np.linalg.inv(fim)
#             denominator = 0
#             variances = [0] * len(design_points)
#             for idx in range(len(design_points)):
#                 variances[idx] = model.variance(design_points[idx][0], inv_fim, plus_minus_sign, *args)
#                 denominator += design_points[idx][1] * variances[idx]
#             for idx in range(len(design_points)):
#                 design_points[idx][1] *= variances[idx] / denominator
#             fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
#         inv_fim = model.inverseInformationMatrix(fim)
#         temp_det_fim = np.linalg.det(fim)
#         det_fim_gain = temp_det_fim - det_fim
#         det_fim = temp_det_fim
#         time_recorder.append(time.time() - start)
#         det_fim_recorder.append(det_fim)
#         # print(max_variance)
#     # sql = "INSERT INTO iteration(algorithm, \
#     #        model, space_points_num, parameters,lowbound,highbound,det_record,time_record,iteration_times,computer) \
#     #        VALUES ('%s',  %s,  %s, '%s',%s,%s,'%s','%s',%s,'%s')" % \
#     #       (algorithm, model_name, grid, str(args), lo_bound, up_bound,
#     #        det_fim_recorder, time_recorder, iteration, COMPUTER_NAME)
#     #
#     # cursor.execute(sql)
#     # db.commit()
#
#     end = time.time()
#     # print("*********  modifiedFWA  *************")
#     # print(design_points)
#     print(det_fim, end - start)
#     return [det_fim, end - start]


def modifiedFWA(lo_bound, up_bound,
                    plus_minus_sign, model,
                    grid, *args):
    """
    First order alrogithm
    :param design_points:
    :param lo_bound:
    :param up_bound:
    :param model:
    :param max_iter:
    :param grid:
    :param args:
    :return:
    """
    algorithm = 'modifiedFWA'
    model_name = model
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
    design_points = [[lo_bound + space_len / (min_sup_points + 1) * (i + 1), 1 / min_sup_points] for i
                     in
                     range(min_sup_points)]
    design_space = np.linspace(lo_bound, up_bound, num=math.ceil(math.sqrt(grid)))

    fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
    inv_fim = model.inverseInformationMatrix(fim)
    det_fim = np.linalg.det(fim)

    iteration = 0
    start = time.time()
    time_recorder = []
    det_fim_recorder = []
    threshold = 1e-6
    det_fim_gain = float('inf')
    while det_fim_gain / det_fim > threshold:
        iteration += 1
        max_variance = float('-inf')
        max_variance_point = sys.maxsize
        for j in range(len(design_space)):
            dVariance = model.variance(design_space[j], inv_fim, plus_minus_sign, *args)
            if dVariance > max_variance:
                max_variance = dVariance
                max_variance_point = design_space[j]
        new_design_space = np.linspace(
            max_variance_point - space_len / (math.ceil(math.sqrt(grid)) / 2) if max_variance_point - space_len / (
                    math.ceil(
                        math.sqrt(grid)) / 2) > lo_bound else lo_bound,
            max_variance_point + space_len / (math.ceil(math.sqrt(grid)) / 2) if max_variance_point + space_len / (
                    math.ceil(
                        math.sqrt(grid)) / 2) < up_bound else up_bound,
            num=math.ceil(math.sqrt(grid)))
        for k in new_design_space:
            dVariance = model.variance(k, inv_fim, plus_minus_sign, *args)
            if dVariance > max_variance:
                max_variance = dVariance
                max_variance_point = k
        A_point = model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args) * \
                  model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args).T

        # max_post_det_fim = float('-inf')
        # alpha_s = 0
        # for alpha in np.linspace(0, 1, num=1000)[1:-1]:
        #     post_fim = fim * (1 - alpha) + A_point * alpha
        #     if np.linalg.det(post_fim) > max_post_det_fim:
        #         max_post_det_fim = np.linalg.det(post_fim)
        #         alpha_s = alpha
        alpha_s = ((max_variance / min_sup_points) - 1) / (max_variance - 1)
        design_points = [[point[0], point[1] * (1 - alpha_s)] for point in design_points]

        if alpha_s > 0:
            design_points.append([max_variance_point, alpha_s])
        elif alpha_s < 0:
            for idx in range(len(design_points)):
                # design_points[idx][1] *= (1 - alpha_s)
                if design_points[idx][0] == max_variance_point:
                    design_points[idx][1] += alpha_s
                    break
        fim = (1 - alpha_s) * fim + alpha_s * A_point
        inv_fim = np.linalg.inv(fim)
        if len(design_points) % (min_sup_points * 10) == 0:
            clusters = DbScan(design_points, 1000, lo_bound, up_bound)
            if len(clusters) >= min_sup_points:
                design_points = []
                for group in clusters:
                    group_max_variance = float('-inf')
                    group_max_variance_point = sys.maxsize
                    weight = group[1]
                    for point in group[0]:
                        variance = model.variance(point, inv_fim, plus_minus_sign, *args)
                        if variance > group_max_variance:
                            group_max_variance = variance
                            group_max_variance_point = point
                    design_points.append([group_max_variance_point, weight])
                fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
                inv_fim = np.linalg.inv(fim)

                # design_points = DbScan(design_points, lo_bound, up_bound)
                # fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
                denominator = 0
                variances = [0] * len(design_points)
                for idx in range(len(design_points)):
                    variances[idx] = model.variance(design_points[idx][0], inv_fim, plus_minus_sign, *args)
                    denominator += design_points[idx][1] * variances[idx]
                for idx in range(len(design_points)):
                    design_points[idx][1] *= variances[idx] / denominator
                fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
                inv_fim = model.inverseInformationMatrix(fim)
        temp_det_fim = np.linalg.det(fim)
        det_fim_gain = temp_det_fim - det_fim
        det_fim = temp_det_fim
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)

    # matplotlib.pyplot.scatter(time_recorder, det_fim_recorder)
    # matplotlib.pyplot.show()
    # print(max_variance)
    sql = "INSERT INTO iteration(algorithm, \
           model, space_points_num, parameters,lowbound,highbound,det_record,time_record,iteration_times,computer) \
           VALUES ('%s',  %s,  %s, '%s',%s,%s,'%s','%s',%s,'%s')" % \
          (algorithm, model_name, grid, str(args), lo_bound, up_bound,
           det_fim_recorder, time_recorder, iteration, COMPUTER_NAME)
    #
    # cursor.execute(sql)
    # db.commit()

    end = time.time()
    # print("*********  modifiedFWA  *************")
    print(det_fim, end - start)
    return [det_fim, end - start]


def CA(lo_bound, up_bound,
       plus_minus_sign, model,
       grid, *args):
    """
    Combined Algorithm
    :param design_points:
    :param lo_bound:
    :param up_bound:
    :param model:
    :param maxIteration:
    :param grid:
    :param args:
    :return:
    """
    algorithm = 'CA'
    model_name = model
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
    design_points = [[lo_bound + space_len / (min_sup_points + 1) * (i + 1), 1 / min_sup_points] for i in
                     range(min_sup_points)]
    design_space = np.linspace(lo_bound, up_bound, num=grid)

    fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
    inv_fim = model.inverseInformationMatrix(fim)
    det_fim = np.linalg.det(fim)

    design_points_len = len(design_points)
    iteration = 0
    time_recorder = []
    det_fim_recorder = []
    start = time.time()
    threshold = 1e-6
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
        design_points = [[sup_points[0], sup_points[1] * (design_points_len / (design_points_len + 1))] for sup_points
                         in
                         design_points]
        design_points.append([max_variance_point, 1 / (design_points_len + 1)])
        design_points_len += 1
        fim = (1 - 1 / design_points_len) * fim + (1 / design_points_len) * model.vectorOfPartialDerivative(
            max_variance_point, plus_minus_sign, *args) * \
              model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args).T
        inv_fim = model.inverseInformationMatrix(fim)

        denominator = 0

        variances = [0] * design_points_len
        for idx in range(design_points_len):
            variances[idx] = model.variance(design_points[idx][0], inv_fim, plus_minus_sign, *args)
            denominator += design_points[idx][1] * variances[idx]
        for idx in range(design_points_len):
            design_points[idx][1] *= variances[idx] / denominator

        fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
        inv_fim = model.inverseInformationMatrix(fim)
        temp_det_fim = np.linalg.det(fim)
        det_fim_gain = temp_det_fim - det_fim
        det_fim = temp_det_fim
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)
    sql = "INSERT INTO iteration(algorithm, \
           model, space_points_num, parameters,lowbound,highbound,det_record,time_record,iteration_times,computer) \
           VALUES ('%s',  %s,  %s, '%s',%s,%s,'%s','%s',%s,'%s')" % \
          (algorithm, model_name, grid, str(args), lo_bound, up_bound,
           det_fim_recorder, time_recorder, iteration, COMPUTER_NAME)
    #
    cursor.execute(sql)
    db.commit()

    end = time.time()
    # print("*********  CA  *************")
    print(det_fim, end - start)
    return [det_fim, end - start]


def FWA(lo_bound, up_bound,
        plus_minus_sign, model,
        grid, *args):
    """
    First order alrogithm
    :param design_points:
    :param lo_bound:
    :param up_bound:
    :param model:
    :param maxIteration:
    :param grid:
    :param args:
    :return:
    """
    model_name = model
    algorithm = 'FWA'
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
    design_points = [[lo_bound + space_len / (min_sup_points + 1) * (i + 1), 1 / min_sup_points] for i
                     in
                     range(min_sup_points)]
    design_space = np.linspace(lo_bound, up_bound, num=grid)

    fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
    invfim = model.inverseInformationMatrix(fim)
    det_fim = np.linalg.det(fim)

    iteration = 0
    start = time.time()
    time_recorder = []
    det_fim_recorder = []

    threshold = 1e-6
    det_fim_gain = float('inf')
    while det_fim_gain / det_fim > threshold:
        iteration += 1
        max_variance = float('-inf')
        max_variance_point = sys.maxsize
        for j in range(len(design_space)):
            dVariance = model.variance(design_space[j], invfim, plus_minus_sign, *args)
            if dVariance > max_variance:
                max_variance = dVariance
                max_variance_point = design_space[j]

        A_point = model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args) * \
                  model.vectorOfPartialDerivative(max_variance_point, plus_minus_sign, *args).T

        alpha_s = ((max_variance / min_sup_points) - 1) / (max_variance - 1)

        fim = (1 - alpha_s) * fim + A_point * alpha_s
        invfim = model.inverseInformationMatrix(fim)
        temp_det_fim = np.linalg.det(fim)
        det_fim_gain = temp_det_fim - det_fim
        det_fim = temp_det_fim
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)

    sql = "INSERT INTO iteration(algorithm, \
           model, space_points_num, parameters,lowbound,highbound,det_record,time_record,iteration_times,computer) \
           VALUES ('%s', %s,  %s, '%s',%s,%s,'%s','%s',%s,'%s')" % \
          (algorithm, model_name, grid, str(args), lo_bound, up_bound,
           det_fim_recorder, time_recorder, iteration, COMPUTER_NAME)

    cursor.execute(sql)
    db.commit()

    # x = []
    # y = []
    # for num in design_space:
    #     x.append(num)
    #     y.append(model.variance(num, invfim, plus_minus_sign, *args))
    # plt.plot(x, y)
    # plt.show()

    end = time.time()
    # print("*********  FWAwithAlphas  *************")

    print(det_fim, end - start)
    return design_points


def Multiplicative(lo_bound, up_bound,
                   plus_minus_sign, model,
                   grid, *args):
    model_name = model
    algorithm = 'MA'
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
    design_points = [[lo_bound + space_len / (grid + 1) * (i + 1), 1 / grid] for i in range(grid)]

    fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
    det_fim = np.linalg.det(fim)
    variances = [0] * grid

    iteration = 0
    start = time.time()
    time_recorder = []
    det_fim_recorder = []
    threshold = 1e-6
    det_fim_gain = float('inf')
    while det_fim_gain / det_fim > threshold:
        iteration += 1
        denominator = 0
        inv_fim = np.linalg.inv(fim)
        for idx in range(len(design_points)):
            variances[idx] = model.variance(design_points[idx][0], inv_fim, plus_minus_sign, *args)
            denominator += design_points[idx][1] * variances[idx]
        for idx in range(len(design_points)):
            design_points[idx][1] *= variances[idx] / denominator
        fim = model.informationMatrixWithWeight(design_points, plus_minus_sign, *args)
        temp_det_fim = np.linalg.det(fim)
        det_fim_gain = temp_det_fim - det_fim
        det_fim = temp_det_fim
        time_recorder.append(time.time() - start)
        det_fim_recorder.append(det_fim)

    sql = "INSERT INTO iteration(algorithm, \
           model, space_points_num, parameters,lowbound,highbound,det_record,time_record,iteration_times,computer) \
           VALUES ('%s',  %s,  %s, '%s',%s,%s,'%s','%s',%s,'%s')" % \
          (algorithm, model_name, grid, str(args), lo_bound, up_bound,
           det_fim_recorder, time_recorder, iteration, COMPUTER_NAME)

    cursor.execute(sql)
    db.commit()

    end = time.time()
    # print("*********  Multiplicative  *************")
    print(det_fim, end - start)
    return [det_fim, end - start]


db = pymysql.connect(host="sh-cynosdbmysql-grp-8chifg7q.sql.tencentcdb.com",
                     user="root",
                     password="QQaN6zsouF49ab",
                     port=20345,
                     database="experiment_log"
                     )

cursor = db.cursor()

COMPUTER_NAME = 'APPLE M1 Pro'

a = 349.02687
b = 1067.04343
c = 0.76332
d = 2.60551

args = (a, b, c, d)

grid_conditions = [100, 500, 1000, 5000, 10000, 50000, 100000]

models = ["Model2", "Model3", "Model4", "Model5"]

low_high_list = [(0.01, 2500.0), (0.01, 1200.0)]
#
# modifiedFWATest(1000, 2500.0,
#                 "positive", 'Model3',
#                 100000, *args)

#
print("*********   *************")
start = time.time()
for i in range(100):
    modifiedFWA(0.01, 2500.0,
                "neg", 'Model5',
                10000, *args)

end = time.time()
print(end - start)
for low_high in low_high_list:
    low = low_high[0]
    high = low_high[1]

    for grid in grid_conditions:
        # print("####################################################################")
        print("grid:", grid, "------")
        for model in models:
            try:
                # pass
                modifiedFWA(low, high,
                            "neg", model,
                            grid, *args)
# #
#                 CA(low, high,
#                    "neg", model,
#                    grid, *args)
#                 FWA(low, high,
#                     "neg", model,
#                     grid, *args)
#                 Multiplicative(low, high,
#                                "neg", model,
#                                grid, *args)
            except BaseException:
                print(BaseException)
db.close()
