# -*- coding: utf-8 -*-
"""

@author: KKubacki
"""
import matplotlib.pyplot as plt
# import ExtraColumns as ec
import numpy as np

def plottingBrownSum_Alfa(SumArray, NumberOfSamples):
    """
    Brown; plotting sum of err in function of alpha
    :return:
    """
    step = 1/NumberOfSamples
    alpha = np.linspace(step, 1-step, NumberOfSamples-1)
    plt.plot(alpha, SumArray)
    plt.xlabel('alpha')
    plt.ylabel('values')
    plt.show()

def plottingUsageVsPredicted(data, t= "time", y = "value", yt = 'y^{^}'):
    """
    usage vs predicted (usage vs demand)
    :return:
    """
    i = data[t]
    j = data[y]
    k = data[yt]

    plt.plot(i,j, color = 'blue', marker = 'o', linestyle = '-', label = 'consumed')
    plt.plot(i,k,color = 'red', marker = 'o', linestyle = '--', label = 'predicted')
    plt.xlabel('Time')
    plt.ylabel('Quantity')
    plt.legend()
    plt.show()


def PltUserDecisionIfWintersMltOrAdd(data):
    """
    helps user to choose proper winters solver (multiplicative or additive)
    :return:
    """
    plt.plot(data["time"], data["value"])
    plt.title('Monotonicity of the consumed sequence')
    plt.xlabel('Time')
    plt.ylabel('Quantity')
    plt.show()


def PltWintersEstimation(data, list, m, t= "time", y = "value", yt = 'y^{^}'):
    """
    show Winters plot with extension
    :param data:
    :param list:
    :param h:
    :param t:
    :param y:
    :param yt:
    :return:
    """

    r = len(data[t])
    i = data[t] # time axis
    j = data[y] # consumed values
    k = data[yt] # predicted values

    arr = np.zeros((len(list) + 1, 2)) # extended predicted

    for h in range(len(list) + 1):
        if h == 0:
            arr[h][0] = len(data[t])
            arr[h][1] = data[yt].iloc[-1]
        else:
            arr[h][0] = len(data[t]) + h
            arr[h][1] = list[h-1][2]

    plt.plot(i,j, color = 'blue', marker = 'o', linestyle = '-', label = 'consumed')
    plt.plot(i.loc[m:r],k.loc[m:r],color = 'red', marker = 'o', linestyle = '--', label = 'predicted')
    plt.plot(arr[:,0], arr[:,1], color = 'red', marker = 'x', linestyle = ':', label = 'estimation')
    plt.xlabel('Time')
    plt.ylabel('Quantity')
    plt.legend()
    plt.show()