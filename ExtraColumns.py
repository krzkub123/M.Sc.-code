# -*- coding: utf-8 -*-
"""
columns refered to:
[4] ZWOLINSKA B. (2020). Niepublikowane materialy dydaktyczne z przedmiotu Logistyka przemyslowa - prognozowanie. Akademia Górniczo- Hutnicza.
@author: KKubacki
"""
import pandas as pd
import numpy as np



# ----- BROWN MODEL -----
def brownModel2(alpha, data, mainvalue, returnValue):
    """
    solving Brown's equation for column 2
    :return:
    """
    data[returnValue] = data[mainvalue]*alpha
    return None


def brownModel3_4(alpha, data, mainvalue, columnName2,columnName3, columnName4):
    """
    solving Brown's equations for columns 3,4
    :return:
    """
    ran = range(len(data[mainvalue]))
    data[columnName3] = 0.1
    data[columnName4] = 0.1
    for i in ran:
        if i == 0:
            data[columnName3][i] = (1 - alpha) * data[mainvalue].mean()
            data[columnName4][i] = data[columnName2][i] + data[columnName3][i]
        elif i >= 1 or i < ran:
            data[columnName3][i] = (1 - alpha) * data[columnName4][i-1]
            data[columnName4][i] = data[columnName2][i] + data[columnName3][i]
        elif i == ran:
            break
    return None


def brownModel5(data, value, mainValue, columnName5):
    """
    solving Brown's equation for column 5
    :return:
    """
    ran = range(len(data[mainValue]))
    data[columnName5] = 0.1
    for i in ran:
        if i == 0:
            data[columnName5][i] = data[value].mean()
        elif i == 1:
            data[columnName5][i] = data[mainValue][i-1]
        elif i >= 2:
            data[columnName5][i] = data[mainValue][i-1]
        elif i == ran:
            break
    return None


def brownModel6(data, y_tb, y_te,columnName):
    """
    solving Brown's equation for column 6
    :return:
    """
    data[columnName] = data[y_tb] - data[y_te]
    return None


def brownModel7(data, e, columnName):
    """
    solving Brown's equation for column 7
    :return:
    """
    data[columnName] = data[e]**2
    return None

def ColumnsBrown(alpha, data, value = "value", col2 = 'a*y', col3 = '(1-a)*y_{i-1}', col4 = 'y^{_}', col5 = 'y^{^}', col6 = 'e', col7 = 'e**2'):
    """
    solving Brown's equations
    :return: sum of error for Brown
    """
    brownModel2(alpha, data, value, col2)
    brownModel3_4(alpha, data, value, col2,col3,col4)
    brownModel5(data, value, col4, col5)
    brownModel6(data, value, col5, col6)
    brownModel7(data, col6, col7)
    return data[col7].sum()


# ----- HOLT MODEL -----
def holtModel2(alpha_H, data_H, mainvalue_H, columnName2):
    """
    solving Holt's equation for column 2
    :return:
    """
    data_H[columnName2] = data_H[mainvalue_H] * alpha_H
    return None

def holtModel3_4_5_6_7(alpha_H, beta_H,  data_H, mainValue, columnName2, columnName3, columnName4, columnName5,
                       columnName6,
                       columnName7):
    """
    solving Holt's equations for columns 3, 4, 5, 6, 7
    :return:
    """
    data_H[columnName3] = 0.1
    data_H[columnName4] = 0.1
    data_H[columnName5] = 0.1
    data_H[columnName6] = 0.1
    data_H[columnName7] = 0.1
    ran = range(len(data_H[mainValue]))
    for i in ran:
        if i == 0:
            data_H[columnName3][i] = (1 - alpha_H) * (data_H[mainValue].mean() + (data_H[mainValue][i+1] - data_H[mainValue][i]))
            data_H[columnName4][i] = data_H[columnName2][i] + data_H[columnName3][i]
            data_H[columnName5][i] = beta_H * (data_H[columnName4][i] - data_H[mainValue].mean()) # yt^{-} = data_H[mainValue].mean()
            data_H[columnName6][i] = (1 - beta_H) * (data_H[mainValue][i+1] - data_H[mainValue][i]) # bt = (data_H[mainValue][i+1] - data_H[mainValue][i])
            data_H[columnName7][i] = data_H[columnName5][i] + data_H[columnName6][i]
        elif i >= 1 or i < ran:
            data_H[columnName3][i] = (1 - alpha_H) * (data_H[columnName4][i-1] + data_H[columnName7][i-1])
            data_H[columnName4][i] = data_H[columnName2][i] + data_H[columnName3][i]
            data_H[columnName5][i] = beta_H * (data_H[columnName4][i] - data_H[columnName4][i-1])
            data_H[columnName6][i] = (1 - beta_H) * data_H[columnName7][i-1]
            data_H[columnName7][i] = data_H[columnName5][i] + data_H[columnName6][i]
        else:
            break
    return None

def holtModel8(data_H, columnName4, columnName7, columnName8):
    """
    solving Holt's equation for column 8
    :return:
    """
    data_H[columnName8] = data_H[columnName4] + data_H[columnName7]
    return None

def holtModel9(data_H, mainValue, columnName8, columnName9):
    """
    solving Holt's equation for column 9
    :return:
    """
    ran = range(len(data_H[mainValue]))
    data_H[columnName9] = 0.1
    for i in ran:
        if i == 0:
            data_H[columnName9] = data_H[mainValue].mean() + (data_H[mainValue][i+1] - data_H[mainValue][i])
        elif i >= 1 or i < ran:
            data_H[columnName9][i] = data_H[columnName8][i-1]
        else:
            break

def holtModel10(data_H, mainValue, columnName8, columnName10):
    """
    solving Holt's equation for column 10
    :return:
    """
    data_H[columnName10] = 0.1
    ran = range(len(data_H[mainValue]))
    for i in ran:
        if i == 0:
            data_H[columnName10][i] = (data_H[mainValue].mean() + (data_H[mainValue][i+1] - data_H[mainValue][i])) - data_H[mainValue][i]
        elif i >= 1 or i < ran:
            data_H[columnName10][i] = data_H[mainValue][i] - data_H[columnName8][i-1]
        else:
            break
    return None

def holtModel11(data_H, columnName10, columnName11):
    """
    solving Holt's equation for column 11
    :return:
    """
    data_H[columnName11] = data_H[columnName10] ** 2
    return None

def ColumnsHolt(a_H, b_H, data, value = 'value', col2 = 'a*y', col3 = '(1-a)*(y_t-y_{t-1})', col4 = 'y_t', col5 = 'b*(y_t-y_{t-1})', col6 = '(1-b)*b_{t-1}', col7 = 'b_t', col8 = 'y^_{t+1}', col9 = 'y^{^}', col10 = 'e_t', col11 = 'e_t**2'):
    """
    solving Holt's equations
    :return: sum of error for Holt
    """
    holtModel2(a_H, data, value, col2)
    holtModel3_4_5_6_7(a_H, b_H, data, value, col2, col3, col4, col5,col6,col7)
    holtModel8(data, col4, col7, col8)
    holtModel9(data, value, col8, col9)
    holtModel10(data, value, col8, col10)
    holtModel11(data, col10, col11)
    return data[col11].sum()

# --- WINTERS MODEL ---


def wintersModel2_3_4_5_6_7_8_9_10(version, m, alpha_W, beta_W, gamma_W, data_W, mainValue, columnName2, columnName3, columnName4, columnName5,columnName6,columnName7, columnName8,columnName9,columnName10):
    """
    solving Winter's equations for columns 3, 4, 5, 6, 7, 8, 9, 10
    :return:
    """
    inval = 0.1
    data_W[columnName2] = inval
    data_W[columnName3] = inval
    data_W[columnName4] = inval
    data_W[columnName5] = inval
    data_W[columnName6] = inval
    data_W[columnName7] = inval
    data_W[columnName8] = inval
    data_W[columnName9] = inval
    data_W[columnName10] = inval
    ran = range(len(data_W[mainValue]))
    a_0 = data_W[mainValue].loc[0:m-1].mean()
    c_0 = data_W[mainValue].loc[m:2*m-1].mean() - data_W[mainValue].loc[0:m-1].mean()
    for i in ran:
        if i < m:
            data_W[columnName10].loc[i] = m * data_W[mainValue].loc[i] / data_W[mainValue].loc[0:m-1].sum()
        elif i == m:
            if version == "additive":
                data_W[columnName2].loc[i] = alpha_W * (data_W[mainValue].loc[i] - data_W[columnName10].loc[i-m])
            elif version == "multiplicative":
                data_W[columnName2].loc[i] = alpha_W * (data_W[mainValue].loc[i] / data_W[columnName10].loc[i-m])
            data_W[columnName3].loc[i] = (1 - alpha_W) * (a_0 + c_0)
            data_W[columnName4].loc[i] = data_W[columnName2].loc[i] + data_W[columnName3].loc[i]
            data_W[columnName5].loc[i] = beta_W * (data_W[columnName4].loc[i] - a_0)
            data_W[columnName6].loc[i] = (1 - beta_W) * c_0
            data_W[columnName7].loc[i] = data_W[columnName5].loc[i] + data_W[columnName6].loc[i]
            if version == "additive":
                data_W[columnName8].loc[i] = gamma_W * (data_W[mainValue].loc[i] - data_W[columnName4].loc[i])
            elif version == "multiplicative":
                data_W[columnName8].loc[i] = (gamma_W * data_W[mainValue].loc[i]) / data_W[columnName4].loc[i]
            data_W[columnName9].loc[i] = (1 - gamma_W) * data_W[columnName10].loc[i-m]
            data_W[columnName10].loc[i] = data_W[columnName8].loc[i] + data_W[columnName9].loc[i]
        elif i > m:
            if version == "additive":
                data_W[columnName2].loc[i] = alpha_W * (data_W[mainValue].loc[i] - data_W[columnName10].loc[i-m])
            elif version == "multiplicative":
                data_W[columnName2].loc[i] = alpha_W * (data_W[mainValue].loc[i] / data_W[columnName10].loc[i-m])
            data_W[columnName3].loc[i] = (1 - alpha_W) * (data_W[columnName4].loc[i-1] + data_W[columnName7].loc[i-1])
            data_W[columnName4].loc[i] = data_W[columnName2].loc[i] + data_W[columnName3].loc[i]
            data_W[columnName5].loc[i] = beta_W * (data_W[columnName4].loc[i] - data_W[columnName4].loc[i-1])
            data_W[columnName6].loc[i] = (1 - beta_W) * data_W[columnName7].loc[i-1]
            data_W[columnName7].loc[i] = data_W[columnName5].loc[i] + data_W[columnName6].loc[i]
            if version == "additive":
                data_W[columnName8].loc[i] = gamma_W * (data_W[mainValue].loc[i] - data_W[columnName4].loc[i])
            elif version == "multiplicative":
                data_W[columnName8].loc[i] = (gamma_W * data_W[mainValue].loc[i]) / data_W[columnName4].loc[i]
            data_W[columnName9].loc[i] = (1 - gamma_W) * data_W[columnName10].loc[i-m]
            data_W[columnName10].loc[i] = data_W[columnName8].loc[i] + data_W[columnName9].loc[i]
    return None


def wintersModel11(version, m, data_W, mainValue, columnName4, columnName7, columnName10, columnName11):
    """
    solving Winter's equation for column 11
    :return:
    """
    l = len(data_W[mainValue])
    data_W[columnName11] = 0
    a_0 = data_W[mainValue].loc[0:m-1].mean()
    c_0 = data_W[mainValue].loc[m:2*m-1].mean() - data_W[mainValue].loc[0:m-1].mean()

    for i in range(m, l):
        if i == m:
            if version == "additive":
                data_W[columnName11].loc[i] = (a_0 + c_0) + data_W[columnName10].loc[i-m]
            elif version == "multiplicative":
                data_W[columnName11].loc[i] = (a_0 + c_0) * data_W[columnName10].loc[i-m]
        elif i > m:
            if version == "additive":
                data_W[columnName11].loc[i] = (data_W[columnName4].loc[i-1] + data_W[columnName7].loc[i-1]) + data_W[columnName10].loc[i-m]
            elif version == "multiplicative":
                data_W[columnName11].loc[i] = (data_W[columnName4].loc[i-1] + data_W[columnName7].loc[i-1]) * data_W[columnName10].loc[i-m]
    return None

def wintersModel12(m, h, data_W, mainValue, columnName11, columnName12):
    """
    solving Winter's equation for column 12
    :return:
    """
    data_W[columnName12] = data_W[mainValue] - data_W[columnName11]
    return None

def wintersModel13(m, h, data_W, columnName12, columnName13):
    """
    solving Winter's equation for column 13
    :return:
    """
    data_W[columnName13]= data_W[columnName12]**2
    return None

def ColumnsWinters(a, b, g, version, m, h, data_W, time = 'time', value = 'value', col2 = 'col2', col3 = 'col3', col4='col4', col5='col5', col6='col6', col7='col7', col8= 'col8', col9= 'col9', col10= 'col10', col11 = 'y^{^}', col12 = 'col12', col13 = 'col13'):
    """
    solving Winter's equations
    :return:
    """
    wintersModel2_3_4_5_6_7_8_9_10(version, m, a, b, g, data_W, value, col2, col3, col4, col5, col6, col7, col8, col9, col10)
    wintersModel11(version, m, data_W, value, col4, col7, col10, col11)
    wintersModel12(m, h, data_W, value, col11, col12)
    wintersModel13(m, h, data_W, col12, col13)
    return data_W[col13].loc[m:len(data_W[time])].sum()

def demandEstimation(version, m, h, data_W, time = 'time', mainValue = 'value', columnName4 = 'col4', columnName7 = 'col7', columnName10 = 'col10'):
    """
    solving Winter's equations for demand mlt or add
    :return:
    """
    id = 1
    l = len(data_W[mainValue])
    dmndEst = []
    consumed = "?"
    for i in range(l, l+h):
        if version == "additive":
            dmndEst.append([str(l) + " + " + str(id), consumed, round(data_W[columnName4].loc[l-1] + data_W[columnName7].loc[l-1]*id + data_W[columnName10].loc[i - m], 1)])
        elif version == "multiplicative":
            dmndEst.append([str(l) + " + " + str(id), consumed, round((data_W[columnName4].loc[l-1] + data_W[columnName7].loc[l-1]*id) * data_W[columnName10].loc[i - m], 1)])
        id += 1
    return dmndEst