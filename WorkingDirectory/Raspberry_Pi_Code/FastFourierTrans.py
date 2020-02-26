"""
Brief: this function calculates fft of given data
Pass the data as column vector, the sampleRate, normalize value (if any)
windowtype is unused for now
"""
import math
import numpy as np


def fastFourierTrans(data,sampleRate,normalizeVal, windowType):
    """
    To get fast fourier transformation of data
    :param data: the data in column vector
    :param sampleRate: the rate at which data was collected
    :param normalizeVal: the normalizing values (if any)
    :param windowType: the type of window used (eg hann,gauss etc.) unused for now
    :return:
    """
    # normalizing acc magnitude
    data = data - normalizeVal
    L = data.shape[0]

    # Getting frequency spectrum values
    f = sampleRate * np.linspace(0, math.ceil(L / 2), math.ceil(L / 2)) / L
    # print(np.shape(f))
    Y = np.fft.fft(data)
    P2 = np.abs(Y / L)
    # print(P2.shape)
    # print(np.sum(P2))

    P1 = P2[0:math.ceil(L / 2)]
    P1 = 2 * P1
    return f, P1


