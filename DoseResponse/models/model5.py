from math import exp
from math import log

import numpy as np


# a[c-(c-1)exp(-(x/b)^d)]
# a = args[0]
# b = args[1]
# c = args[2]
# d = args[3]


# def partialaNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     d = args[3]
#     return c - (c - 1) * exp(-(x / b) ** d)

def partialaNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]

    return c - (c - 1) * x


# def partialbNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     d = args[3]
#     return a * d * (x / b) ** d * (1 - c) * exp(-(x / b) ** d) / b

def partialbNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]

    return a * d * (-log(x)) * (1 - c) * x / b


# def partialcNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     d = args[3]
#     return a * (1 - exp(-(x / b) ** d))

def partialcNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]

    return a * (1 - x)


# def partialdNegative(x, *args):
#     a = args[0]
#     b = args[1]
#     c = args[2]
#     d = args[3]
#     return -a * (x / b) ** d * (1 - c) * exp(-(x / b) ** d) * log(x / b)

def partialdNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]

    return -a * (-log(x)) * (1 - c) * x * log((-log(x)) ** (1 / d))


def vectorOfPartialDerivative(x, plus_minus_sign, *args):
    """
    :param x: value of the design point
    :return: f(x,Theta).T
    [[∂η(x,Theta) / ∂θ1],
     [∂η(x,Theta) / ∂θ2],
     ..................
     [∂η(x,Theta) / ∂θm]]
    """
    x = exp(-(x / args[1]) ** args[3])
    return np.array([[partialaNegative(x, *args),
                      partialbNegative(x, *args),
                      partialcNegative(x, *args),
                      partialdNegative(x, *args)]]).T


def informationMatrix(designPoints, plus_minus_sign, *args):
    """
    :param designPoints: design points
    :return: information matrix
    """
    result = np.zeros((4, 4))
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


def variance(x, inverseInformationMatrix, plus_minus_sign, *args):
    left = np.matmul(vectorOfPartialDerivative(x, plus_minus_sign, *args).T, inverseInformationMatrix)
    result = np.matmul(left, vectorOfPartialDerivative(x, plus_minus_sign, *args))
    return result[0][0]
