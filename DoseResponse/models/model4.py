import math

import numpy as np


# a,b,c


# def partialaNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     return math.exp(-x / b) * (c * math.exp(x / b) - c + 1)

def partialaNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    return c - (c - 1) * x


# def partialbNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     return -(a * c - a) * x * math.exp(-x / b) / b ** 2

def partialbNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    return (a * c - a) * math.log(x) * x / b


# def partialcNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     return math.exp(-x / b) * (a * math.exp(x / b) - a)

def partialcNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    return x * (a / x - a)


def vectorOfPartialDerivative(x, plus_minus_sign, *args):
    """
    :param x: value of the design point
    :return: f(x,Theta).T
    [[∂η(x,Theta) / ∂θ1],
     [∂η(x,Theta) / ∂θ2],
     ..................
     [∂η(x,Theta) / ∂θm]]
    """
    x = math.exp(-x / args[1])
    return np.array([[partialaNegative(x, *args),
                      partialbNegative(x, *args),
                      partialcNegative(x, *args)]]).T


def informationMatrix(designPoints, plus_minus_sign, *args):
    """
    :param designPoints: design points
    :param weights: weights of the design points
    :return: information matrix
    """
    result = np.zeros((3, 3))
    if type(designPoints[0]) == np.float64:
        weights = [1 / len(designPoints) for i in range(len(designPoints))]
        for i in range(len(designPoints)):
            result += vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args) * \
                      vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args).T * \
                      weights[i]
    else:
        for i in range(len(designPoints)):
            result += vectorOfPartialDerivative(designPoints[i][0], plus_minus_sign, *args) * \
                      vectorOfPartialDerivative(designPoints[i][0], plus_minus_sign, *args).T * \
                      designPoints[i][1]
    return np.array(result)


def inverseInformationMatrix(informationMatrix):
    return np.linalg.inv(informationMatrix)


def variance(x, vectorOfPartialDerivative, inverseInformationMatrix, plus_minus_sign, *args):
    left = np.matmul(vectorOfPartialDerivative(x, plus_minus_sign, *args).T, inverseInformationMatrix)
    result = np.matmul(left, vectorOfPartialDerivative(x, plus_minus_sign, *args))
    return result[0][0]
