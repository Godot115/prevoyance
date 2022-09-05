# -*- coding: utf-8 -*-
# @Time    : 7/2/22 03:15
# @Author  : godot
# @FileName: DbScan.py
# @Project : prevoyance
# @Software: PyCharm
from typing import List

import numpy as np
from sklearn.cluster import DBSCAN


def DbScan(designPoints: List[List[float]], lowerBound: float, upperBound: float) -> List[float]:
    keys = [[i[0]] for i in designPoints]
    points = []
    for idx in range(len(designPoints)):
        points += keys[idx] * int(designPoints[idx][1] * 1000)
    points = np.array(points)
    points = points.reshape(len(points), 1)
    db = DBSCAN(eps=int((upperBound - lowerBound) / 100), min_samples=100).fit(points)
    labels = db.labels_
    clusters = dict()
    points_num = 0
    for label in labels:
        if not label == -1:
            points_num += 1
            clusters[label] = []
    for i in range(len(points)):
        if not labels[i] == -1:
            clusters[labels[i]].append(points[i])
    cluster_centers = []
    for key in clusters:
        cluster_centers.append([float(sum(clusters[key])/len(clusters[key])), len(clusters[key]) / points_num])
    return cluster_centers
