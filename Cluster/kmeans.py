# -*- coding: utf-8 -*-
# @Time    : 7/1/22 19:30
# @Author  : godot
# @FileName: kmeans.py
# @Project : prevoyance
# @Software: PyCharm
from typing import List

import numpy as np
from sklearn.cluster import DBSCAN


def Kmeans(points, k: int, iteration: int) -> List[int]:
    """
    :param points:
    :type List[float]:
    :param k:
    :type int:
    :return: cluster_centers
    :rtype: List[float]
    """
    clusters = []
    for i in range(k):
        clusters.append((points[i], []))
    for i in range(iteration):
        for point in points:
            min_distance = float('inf')
            min_cluster = None
            for cluster in clusters:
                distance = pointsDistance(point, cluster[0])
                if distance < min_distance:
                    min_distance = distance
                    min_cluster = cluster
            min_cluster[1].append(point)
        new_clusters = []
        for cluster in clusters:
            new_clusters.append((sum(cluster[1]) / len(cluster[1]), cluster[1]))
        flag = False
        for i in range(len(clusters)):
            if clusters[i][0] != new_clusters[i][0]:
                flag = True
                break
        clusters = new_clusters
        if not flag:
            break
    return [cluster[0] for cluster in clusters]


def pointsDistance(point1, point2):
    return abs(point1 - point2)

