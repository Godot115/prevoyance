from math import log, exp

import numpy as np


# args[0] = a, args[1] = b, args[2] = d

def partialaPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return x

def partialaNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return x


def partialbPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return (-a * d * log(x) * x) / b

def partialbNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return (-a * d * log(x) * x) / b


def partialdPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return a * log(x) * x * log(log(x) ** (-d))

def partialdNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return a * log(x) * x * log((-log(x)) ** (-d))


def vectorOfPartialDerivative(x, plus_minus_sign="positive", *args):
    """
    :param x: value of the design point
    :return: f(x,Theta).T
    [[∂η(x,Theta) / ∂θ1],
     [∂η(x,Theta) / ∂θ2],
     ..................
     [∂η(x,Theta) / ∂θm]]
     [∂η(x,Theta) / ∂θm]]
    """
    if plus_minus_sign == "positive":
        x = exp((x / args[1]) ** args[3])
        return np.array([[partialaPositive(x, *args),
                          partialbPositive(x, *args),
                          partialdPositive(x, *args)]]).T
    else:
        x = exp(-((x / args[1]) ** args[3]))
        return np.array([[partialaNegative(x, *args),
                          partialbNegative(x, *args),
                          partialdNegative(x, *args)]]).T


def informationMatrix(designPoints, plus_minus_sign="positive", *args):
    """
    :param designPoints: design points
    :return: information matrix
    """
    result = np.zeros((3, 3))
    weights = [1 / len(designPoints) for i in range(len(designPoints))]
    for i in range(len(designPoints)):
        result += vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args) * \
                  vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args).T * \
                  weights[i]
    return np.array(result)

def informationMatrixWithWeight(designPoints, plus_minus_sign="positive", *args):
    """
    :param designPoints: design points
    :return: information matrix
    """
    result = np.zeros((3, 3))
    for i in range(len(designPoints)):
        result += vectorOfPartialDerivative(designPoints[i][0], plus_minus_sign, *args) * \
                  vectorOfPartialDerivative(designPoints[i][0], plus_minus_sign, *args).T * \
                  designPoints[i][1]
    return np.array(result)


def inverseInformationMatrix(informationMatrix):
    return np.linalg.inv(informationMatrix)


def variance(x, inverseInformationMatrix, plus_minus_sign="positive", *args):
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
# x=exp((1 / args[1]) ** args[3])
# print(x)
# print(partialdPositive(x, *args))