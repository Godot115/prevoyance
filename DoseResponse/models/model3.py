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
    return -a * d * log(x) * x / b

def partialbNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return -a * d * log(x) * x / b


def partialdPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return a * log(x) * x * log(log(x) ** (1 / d))

def partialdNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return a * log(x) * x * log((-log(x)) ** (1 / d))


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
        x = exp(-(x / args[1]) ** args[3])
        return np.array([[partialaNegative(x, *args),
                          partialbNegative(x, *args),
                          partialdNegative(x, *args)]]).T


def informationMatrix(designPoints, plus_minus_sign="positive", *args):
    """
    :param designPoints: design points
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


def variance(x, inverseInformationMatrix, plus_minus_sign="positive", *args):
    left = np.matmul(vectorOfPartialDerivative(x, plus_minus_sign, *args).T, inverseInformationMatrix)
    result = np.matmul(left, vectorOfPartialDerivative(x, plus_minus_sign, *args))
    return result[0][0]
