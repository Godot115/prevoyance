# -*- coding: utf-8 -*-
# @Time    : 7/2/22 03:15
# @Author  : godot
# @FileName: DbScan.py
# @Project : prevoyance
# @Software: PyCharm
from typing import List

import numpy as np
from sklearn.cluster import DBSCAN


# def DbScan(designPoints: List[List[float]], lowerBound: float, upperBound: float) -> List[float]:
#     keys = [[i[0]] for i in designPoints]
#     points = []
#     for idx in range(len(designPoints)):
#         points += keys[idx] * int(designPoints[idx][1] * 1000)
#     points = np.array(points)
#     points = points.reshape(len(points), 1)
#     db = DBSCAN(eps=int((upperBound - lowerBound) / 100), min_samples=100).fit(points)
#     labels = db.labels_
#     clusters = dict()
#     points_num = 0
#     for label in labels:
#         if not label == -1:
#             points_num += 1
#             clusters[label] = []
#     for i in range(len(points)):
#         if not labels[i] == -1:
#             clusters[labels[i]].append(points[i])
#     cluster_centers = []
#     for key in clusters:
#         cluster_centers.append([float(sum(clusters[key]) / len(clusters[key])), len(clusters[key]) / points_num])
#     return cluster_centers


def DbScan(designPoints: List[List[float]], lambda_1: int, lowerBound: float, upperBound: float) -> List[float]:
    space_len = upperBound - lowerBound
    keys = list(set([i[0] for i in designPoints]))
    p_w_dict = dict()
    for key in keys:
        p_w_dict[key] = 0
    for point in designPoints:
        p_w_dict[point[0]] += point[1]
    points = []
    for item in p_w_dict.items():
        points += [item[0]] * int(item[1] * 1000)
    points = np.array(points)
    points = points.reshape(len(points), 1)
    db = DBSCAN(eps=(space_len / 100), min_samples=(lambda_1 / 10)).fit(points)
    labels = db.labels_
    l_p_dict = dict()
    for key in set(labels):
        l_p_dict[key] = []

    for idx in range(len(labels)):
        l_p_dict[labels[idx]].append(points[idx][0])

    res = []
    weight_sum = 0
    for key in l_p_dict.keys():
        if not key == -1:
            l_p_dict[key] = list(set(l_p_dict[key]))
            weight = 0
            for point in l_p_dict[key]:
                weight += p_w_dict[point]
            weight_sum += weight
            res.append([l_p_dict[key], weight])
    res = [[i[0], i[1] / weight_sum] for i in res]
    # for key in l_p_dict.keys():
    #     if not key == -1:
    #         points = [item for item in l_p_dict[key]]
    #         print(points)
    #         res.append([[], ])
    # for sup_point in designPoints:
    #     if sup_point[0] in points_lable:
    #         clusters[points_lable[sup_point[0]]].append(sup_point)
    #
    # # print(clusters.values())
    # res = []
    # weights_sum = 0
    # for group in clusters.values():
    #     points = [i[0] for i in group]
    #     weights = [i[1] for i in group]
    #     weight = sum(weights)
    #     weights_sum += weight
    #     res.append([list(set(points)), weight])
    # for i in range(len(res)):
    #     res[i][1] /= weights_sum
    # # print([i[0] for i in res])
    return res
    # cluster_centers = []
    # for key in clusters:
    #     cluster_centers.append([float(sum(clusters[key])/len(clusters[key])), len(clusters[key]) / points_num])
    # print(len(cluster_centers))
    # return cluster_centers
