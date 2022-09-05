import math

import numpy as np


# def partiala(x, *args):
#     a = args[0]
#     b = args[1]
#     return math.exp(x / b)

def partiala(x, *args):
    a = args[0]
    b = args[1]
    return x


# def partialb(x, *args):
#     a = args[0]
#     b = args[1]
#     return -1 * ((a * x * math.exp(x / b)) / (b ** 2))

def partialb(x, *args):
    a = args[0]
    b = args[1]
    return -a * b * math.log(x) * x / (b * b)


def vectorOfPartialDerivative(x, plus_minus_sign, *args):
    """
    :param x: value of the design point
    :return: f(x,Theta).T
    [[∂η(x,Theta) / ∂θ1],
     [∂η(x,Theta) / ∂θ2],
     ..................
     [∂η(x,Theta) / ∂θm]]
    """
    x = math.exp(x / args[1])
    return np.array([[partiala(x, *args),
                      partialb(x, *args)]]).T


def informationMatrix(designPoints, plus_minus_sign, *args):
    """
    :param designPoints: design points
    :return:
    """
    result = np.zeros((2, 2))
    weights = [1 / len(designPoints) for i in range(len(designPoints))]
    for i in range(len(designPoints)):
        result += vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args) * \
                  vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args).T * \
                  weights[i]
    return np.array(result)


def informationMatrixWithWeight(designPoints, plus_minus_sign, *args):
    """
    :param designPoints: design points
    :return:
    """
    result = np.zeros((2, 2))
    for i in range(len(designPoints)):
        result += np.matmul(vectorOfPartialDerivative(designPoints[i][0], plus_minus_sign, *args),
                            vectorOfPartialDerivative(designPoints[i][0], plus_minus_sign, *args).T) * \
                  designPoints[i][1]
    return np.array(result)


def inverseInformationMatrix(informationMatrix):
    return np.linalg.inv(informationMatrix)


def variance(x, inverseInformationMatrix, plus_minus_sign, *args):
    left = np.matmul(vectorOfPartialDerivative(x, plus_minus_sign, *args).T, inverseInformationMatrix)
    result = np.matmul(left, vectorOfPartialDerivative(x, plus_minus_sign, *args))
    return result[0][0]


def combinedVariance(x_i, x_j, invFIM, plus_minus_sign, *args):
    return np.matmul(np.matmul(vectorOfPartialDerivative(x_i, plus_minus_sign, *args).T, invFIM),
                     vectorOfPartialDerivative(x_j, plus_minus_sign, *args))[0][0]


def delta(x_i, x_j, invFIM, plus_minus_sign, *args):
    return variance(x_j, invFIM, plus_minus_sign, *args) - (
            variance(x_i, invFIM, plus_minus_sign, *args) * variance(x_j, invFIM, plus_minus_sign,
                                                                     *args) - combinedVariance(x_i, x_j, invFIM,
                                                                                               plus_minus_sign,
                                                                                               *args) * combinedVariance(
        x_i, x_j, invFIM, plus_minus_sign, *args)) - variance(x_i, invFIM, plus_minus_sign, *args)


# a = 349.02687
# b = 1067.04343
# c = 0.76332
# d = 2.60551
# args = (a, b, c, d)
#
# np.matmul(vectorOfPartialDerivative(i, "plus_minus_sign", *args),
#               vectorOfPartialDerivative(i, "plus_minus_sign", *args).T)