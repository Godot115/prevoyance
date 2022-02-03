import math

import numpy as np


# args[0] = a, args[1] = b, args[2] = d

def partialaPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return math.exp((x / b) ** d)


def partialaNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return math.exp(-1 * (x / b) ** d)


def partialbPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return -a * b ** (-d - 1) * d \
           * x ** d * math.exp((x / b) ** d)


def partialbNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return a * b ** (-d - 1) * d \
           * x ** d * math.exp(-1 * (x / b) ** d)


def partialdPositive(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return (a * x ** d * math.exp((x / b) ** d)
            * math.log(x) - a * math.log(b) * x ** d
            * math.exp((x / b) ** d)) / b ** d


def partialdNegative(x, *args):
    a = args[0]
    b = args[1]
    c = args[2]
    d = args[3]
    return -1 * (math.exp(-(x / b) ** d) * (
            a * x ** d * math.log(x) - a
            * math.log(b) * x ** d)) / b \
           ** d


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
        return np.array([[partialaPositive(x, *args),
                          partialbPositive(x, *args),
                          partialdPositive(x, *args)]]).T
    else:
        return np.array([[partialaNegative(x, *args),
                          partialbNegative(x, *args),
                          partialdNegative(x, *args)]]).T


def informationMatrix(designPoints, plus_minus_sign="positive", *args):
    """
    :param designPoints: design points
    :return: information matrix
    """
    weights = [1 / len(designPoints) for i in range(len(designPoints))]
    result = np.zeros((3, 3))
    for i in range(len(designPoints)):
        result += vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args) * \
                  vectorOfPartialDerivative(designPoints[i], plus_minus_sign, *args).T * \
                  weights[i]
    return np.array(result)


def inverseInformationMatrix(informationMatrix):
    return np.linalg.inv(informationMatrix)


def variance(x, vectorOfPartialDerivative, inverseInformationMatrix,
             plus_minus_sign="positive", *args):
    left = np.matmul(vectorOfPartialDerivative(x, plus_minus_sign, *args).T, inverseInformationMatrix)
    result = np.matmul(left, vectorOfPartialDerivative(x, plus_minus_sign, *args))
    return result[0][0]
