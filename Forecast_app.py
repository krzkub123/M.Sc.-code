# -*- coding: utf-8 -*-
"""

@author: KKubacki
"""

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox

from tkinter.filedialog import askopenfilename
import plots as pt
import ExtraColumns as ec

import pandas as pd
from scipy.optimize import minimize
import numpy as np

import sys, os

# globally declare value
def globalDeclareValues():
    """
    globaly declaration of values, used for clearing existing data
    :return:
    BROWN
    HOLT
    WINTERS
    OTHER
    """
    # BROWN INIT
    global v, BROWN_SUM_ARR, brown_0, alpha_B, alpha_B_it, dataB, brownMinStatus
    v = ""
    # init guess
    BROWN_SUM_ARR = np.array([])
    brown_0 = [1]
    brownMinStatus = False

    # HOLT INIT
    global HOLT_SUM_ARR, holt_0, alpha_H, beta_H, dataH, holtMinStatus
    HOLT_SUM_ARR = np.array([])
    holt_0 = [1, 1]
    holtMinStatus = False

    # WINTERS INIT
    global WINTERS_SUM_ARR, winters_0, alpha_W, beta_W, gamma_W, dataW, wintersMinStatus, wintersVersionsOption
    WINTERS_SUM_ARR = np.array([])
    winters_0 = [1, 1, 1]
    wintersMinStatus = False
    wintersVersionsOption = ["multiplicative", "additive"]

    # OTHER
    global dataList, df
    # --- data manipulation ---
    dataList = []
    df = pd.DataFrame()

    # clearing existing tree
    brown.tree.delete(*brown.tree.get_children())
    holt.tree.delete(*brown.tree.get_children())
    winters.tree.delete(*brown.tree.get_children())
    return None

# non important data overall
digit_num = 2
step = 10**(-digit_num)
n = int(round(1/step))

def restart_program():
    """
    restart GUI
    :return:
    """
    python = sys.executable
    os.execl(python, python, * sys.argv)

# prepare functions for usage in tkinter - no parameter
# ---------------------
def import_B():
    """
    import data Brown
    :return:
    """
    global StatTable
    StatTable = False
    try:
        import_csv_data(brown)
        inputDataToTable(brown)
        brown.B1["state"] = "active"
        StatTable = True
    except FileNotFoundError:
        print("no file chosen")

def import_H():
    """
    import data Holt
    :return:
    """
    global StatTable
    StatTable = False
    try:
        import_csv_data(holt)
        inputDataToTable(holt)
        holt.B1["state"] = "active"
    except FileNotFoundError:
        print("no file chosen")

def import_W():
    """
    import data Winters
    :return:
    """
    global StatTable
    StatTable = False
    try:
        import_csv_data(winters)
        inputDataToTable(winters)
        winters.B1["state"] = "active"
        winters.B4["state"] = "active"
        StatTable = True
    except FileNotFoundError:
        print("no file chosen")

# reports
def reportB():
    """
    reporting with Brown data
    :return:
    """
    global BROWN_SUM_ARR, n, alpha_B_sc, alpha_B_it
    ec.ColumnsBrown(alpha_B_sc , brown.data)
    pt.plottingBrownSum_Alfa(BROWN_SUM_ARR, n)
    pt.plottingUsageVsPredicted(brown.data)
    scbr1 = "Minimal alpha found with python funtion is %.4f.\n" %(alpha_B_sc)
    scbr2 = "Solution found after # todo\n" # todo: how to measure usage of computer resources
    itbr1 = "Minimal alpha found with iteration over alpha is %.2f.\n" % (alpha_B_it)
    itbr2 = "Solution found after # todo\n"  #
    tk.messagebox.showinfo(title="Brown minimalization summary", message = scbr1 + scbr2 +"\n"+ itbr1 + itbr2)

def reportH():
    """
    reporting with Holt data
    :return:
    """
    global HOLT_SUM_ARR, n, alpha_H_sc, beta_H_sc, holt_B_it
    ec.ColumnsHolt(alpha_H_sc, beta_H_sc, brown.data)
    # pt.plottingBrownSum_Alfa(BROWN_SUM_ARR, n) todo 3D plot holt method
    pt.plottingUsageVsPredicted(holt.data)
    scho1 = "Minimal alpha found with python funtion is a = %.4f.\n" % (alpha_H_sc)
    scho2 = "Minimal beta found with python funtion is a = %.4f.\n" % (beta_H_sc)
    scho3 = "Solution found after #todo\n"  # todo: how to measure usage of computer resources
    itho1 = "Minimal alpha found with iteration over alpha is %.2f.\n" % (alpha_H_it)
    itho2 = "Minimal beta found with iteration over beta is %.2f.\n" % (alpha_H_it)
    itho3 = "Solution found after #todo\n"  #
    tk.messagebox.showinfo(title="Holt minimalization summary", message=scho1 + scho2 + scho3 + "\n" + itho1 + itho2 + itho3)

def reportW():
    """
    reporting with Winters data
    :return:
    """
    pt.PltWintersEstimation(winters.data, winters.demandEstimation, winters.periodTime.get())
    print("winters goal function: ", winters.data['y^{^}'].sum())
    print("analysed data: \n", winters.data)
    print("demand estimation list: ", winters.demandEstimation)
    l = len(winters.data['time'])
    print("predicted value: ", round((winters.data['col4'].loc[l-1] + winters.data['col7'].loc[l-1]*1) + winters.data['col10'].loc[8],1))
    winters.data.to_clipboard()

def pltConsumedWinters():
    """
    plotting chart that will help user to decide if data is for multiplicative or additive Winters method
    :return:
    """
    pt.PltUserDecisionIfWintersMltOrAdd(winters.data)

# import data and prepare it
# ---------------------
def import_csv_data(method):
    """
    import csv data; proper data structure: column[0] = "time" / column[1] = "value" / separator = ";"
    :return:
    """
    global v, df
    csv_file_path = askopenfilename(filetype=(("csv files", "*.csv"),("All Files", "*.*")))
    v = tk.StringVar(root)
    v.set(csv_file_path)
    df = pd.read_csv(csv_file_path, ';')
    method.tree.delete(*method.tree.get_children())
    method.data = df

def inputDataToTable(method):
    """
    input data to table method: tab where data will be placed
    :return:
    """
    global df
    method.dataList = []
    d = method.data
    l = len(d["time"])
    if StatTable:
        for i in range(l):
            method.dataList.append((str(d["time"][i]), str(d["value"][i]), round(d['y^{^}'][i],1)))
    else:
        for i in range(l):
            method.dataList.append((str(d["time"][i]), str(d["value"][i]), "???"))
    for i in method.dataList:
        method.tree.insert('', tk.END, values = i)

def addDataToTable(method, list):
    """
    add data to existing table
    :return:
    """
    for i in list:
        method.tree.insert('',tk.END, values = i)

def funB(x):
    """
    prepare Brown function to optimizing
    :return:
    """
    sum = ec.ColumnsBrown(x, brown.data)
    return sum

def funH(x):
    """
    prepare Holt function to optimizing
    :return:
    """
    sum = ec.ColumnsHolt(x[0], x[1], holt.data)
    return sum

def funW(x):
    """
    prepare Winters function to optimizing
    :return:
    """
    sum = ec.ColumnsWinters(x[0], x[1], x[2], winters.WintersVersionStr.get(), int(winters.periodTime.get()), int(winters.overTakeTime.get()), winters.data)
    return sum

def BrownMin():
    """
    return brown min function with scipy optimize; minimizing Brown coefficient
    :return: Brown opt scipy
    """
    global alpha_B_sc, StatTable, dataB, df
    resB = minimize(funB, brown_0, method = 'TNC' , bounds = [(0.001,1)])
    alpha_B_sc = resB.x
    StatTable = True
    brown.tree.delete(*brown.tree.get_children())
    inputDataToTable(brown)
    tk.messagebox.showinfo(title="Brown method result", message="Optimal alpha for Brown method by python function is %.4f" % (alpha_B_sc))
    brown.B2["state"] = "active"

def HoltMin():
    """
    return holt min function with scipy.optimize ; minimizing Holt coefficients
    :return: holt opt scipy
    """
    global alpha_H_sc, beta_H_sc, holtMinStatus, StatTable
    resH = minimize(funH, holt_0, method='TNC', bounds=[(0.001, 1), (0.001, 1)])
    alpha_H_sc = resH.x[0]
    beta_H_sc = resH.x[1]
    StatTable = True
    holt.tree.delete(*holt.tree.get_children())
    inputDataToTable(holt)
    tk.messagebox.showinfo(title="Holt method result", message="For Holt method by python function minimal alpha is %.4f, beta is %.4f" % (alpha_H_sc, beta_H_sc))
    holt.B2["state"] = "active"

def WitersMin():
    """
    return winters min function with scipy.optimize ; minimizing Winters coefficients
    :return: winters opt scipy
    """
    global alpha_W_sc, beta_W_sc, gamma_W_sc, wintersMinStatus, StatTable
    resW = minimize(funW, winters_0, method='TNC', bounds=[(0.001, 1), (0.001, 1), (0.001, 1)])
    alpha_W_sc = resW.x[0]
    beta_W_sc = resW.x[1]
    gamma_W_sc = resW.x[2]
    StatTable = True
    winters.tree.delete(*winters.tree.get_children())
    inputDataToTable(winters)
    winters.demandEstimation = ec.demandEstimation(winters.WintersVersionStr.get(), int(winters.periodTime.get()), int(winters.overTakeTime.get()), winters.data)
    print(winters.WintersVersionStr.get())
    addDataToTable(winters, winters.demandEstimation)
    print(winters.data)
    print('len of i is: ', len(winters.data["time"]))
    print('len of j is: ', len(winters.data["value"]))
    print('len of k is: ', len(winters.data["y^{^}"]))
    tk.messagebox.showinfo(title="Winters method result", message="For Winters method by python function minimal alpha is %.4f, beta is %.4f and gamma is %.4f" % (alpha_W_sc, beta_W_sc, gamma_W_sc))
    winters.B2["state"] = "active"

def BrownIteration():
    """
    function that iterates over alpha and finds min sum with plotting sum(alpha) ; not recommended to use
    :return: alpha opt iterated
    """
    global alpha_B_it, n, BROWN_SUM_ARR
    e2 = ec.ColumnsBrown(0.5, brown.data)
    for i in range(1,n):
        sum = ec.ColumnsBrown(i / n, brown.data)
        if sum < e2:
            e2 = sum
            alpha_B_it = i / n
        # valpha_opt += dec_prec
        BROWN_SUM_ARR = np.append(BROWN_SUM_ARR, sum)
    msgbox.showinfo(title="Brown method result", message="Optimal alpha for Brown method by iteration is %.2f"%(alpha_B_it))
    brown.B3["state"] = ["active"]

def HoltIteration():
    """
    function that iterates over alpha and beta and finds min sum ; not recommended to use
    :return: alpha opt iterated
    """
    global alpha_H_it, beta_H_it, n, HOLT_SUM_ARR
    e2 = ec.ColumnsHolt(0.5, 0.5, holt.data)
    for i in range(1, n): # i stands for alpha
        for j in range(1,n): # j stands for beta
            sum = ec.ColumnsHolt(i/n, j/n, holt.data)
            if sum < e2:
                e2 = sum
                alpha_H_it = i/n
                beta_H_it = j/n
            HOLT_SUM_ARR = np.append(HOLT_SUM_ARR, sum)
    tk.messagebox.showinfo(title="Holt method result", message="Optimal alpha and beta for Holt method by iteration is:\n alpha = %.2f\nbeta = %.2f" % (alpha_H_it, beta_H_it))
    holt.B3["state"] = ["active"]

def WintersIteration():
    """
    function that iterates over alpha, beta and gamma and finds min sum ; not recommended to use
    :return: alpha opt iterated
    """
    global alpha_W_it, beta_W_it, gamma_W_it, n, HOLT_SUM_ARR, m, h, WintersVersionStr # todo: chart sum(alpha,beta)
    # shorIteration = n /
    e2 = ec.ColumnsWinters(0.5, 0.5, 0.5, WintersVersionStr, m, h, winters.data)
    for i in range(1, n): # i stands for alpha
        for j in range(1,n): # j stands for beta
            for k in range(1,n): # k stands for gamma
                sum = ec.ColumnsWinters(i, j, k, WintersVersionStr, m, h, winters.data)
                if sum < e2:
                    e2 = sum
                    alpha_W_it = i/n
                    beta_W_it = j/n
                    gamma_W_it = j/n
    tk.messagebox.showinfo(title="Holt method result", message="Optimal alpha and beta for Holt method by iteration is:\n alpha = %.2f\nbeta = %.2f" % (alpha_B_it, beta_H_it))
    holt.B3["state"] = ["active"]

def DoNothing():
    """
    check if sth works; initial assigment to buttons
    :return:
    """
    print("hello world")

class tabGUI():
    """
    creating separate tab; further used in Brown/ Holt/ Winters
    :return:
    """
    def __init__(self, rt, namemethod):
        # tree creating
        self.name = namemethod
        self.tree = ttk.Treeview(rt, columns = ('#1', '#2', '#3'), show='headings')
        self.tree.heading('#1', text='time')
        self.tree.heading('#2', text='consumption')
        self.tree.heading('#3', text='predicted consumption')
        self.tree.grid(row=1, column=0, sticky='nsew')
        self.scrollbar = ttk.Scrollbar(rt, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree.column("#0", anchor="e", width=120, minwidth=20)
        self.tree.column("#1", anchor="e", width=60)
        self.tree.column("#2", width=60)
        self.tree.column("#3", width=60)
        # buttons
        self.B1 = tk.Button(rt, text='Minimalize ' + self.name + ' method', command=DoNothing)
        self.B2 = tk.Button(rt, text='Iteration ' + self.name, command=DoNothing)
        self.B3 = tk.Button(rt, text='Report ' + self.name, command=DoNothing)
        self.BLoad = tk.Button(rt, text='Load ' + self.name + ' data', command=DoNothing)
        self.buttonsCol = 0
        self.B1.grid(row=2, column=self.buttonsCol)
        self.B2.grid(row=3, column=self.buttonsCol)
        self.B3.grid(row=4, column=self.buttonsCol)
        # self.Btest.grid(row = 0, column=buttonsCol+1)
        self.BLoad.grid(row = 0, column=self.buttonsCol)
        B = [self.B1, self.B2, self.B3]
        for item in B:
            item["state"] = "disabled" # disabled / active
            item["heigh"] = 1
            item["width"] = 20
        # data operation
        self.dataList = []
        self.data = pd.DataFrame(columns = ["time", "value"])

if __name__ == '__main__':
    root = tk.Tk()

    tabControl = ttk.Notebook(root)
    ResetBut = tk.Button(root, text='reset', command=restart_program)
    ResetBut.grid(columnspan = 2, sticky = 'n')
    # create menubar

    tabBrown = tk.Frame(tabControl)
    tabHolt = tk.Frame(tabControl)
    tabWinters = tk.Frame(tabControl)

    tabControl.add(tabBrown, text='Brown')
    tabControl.add(tabHolt, text='Holt')
    tabControl.add(tabWinters, text='Winters')
    tabControl.grid(row = 12, column = 2)
    # --- brown tab ---
    brown = tabGUI(tabBrown, "Brown")
    brown.BLoad["command"] = import_B
    brown.B1["command"] = BrownMin
    brown.B2["command"] = BrownIteration
    brown.B3["command"] = reportB
    # --- holt tab ---
    holt = tabGUI(tabHolt, "Holt")
    holt.BLoad["command"] = import_H
    holt.B1["command"] = HoltMin
    holt.B2["command"] = HoltIteration
    holt.B3["command"] = reportH
    # --- winters tab --- 
    winters = tabGUI(tabWinters, "Winters")
    winters.BLoad["command"] = import_W
    winters.B1["command"] = WitersMin
    winters.B2["command"] = WintersIteration
    winters.B3["command"] = reportW
    winters.B3["state"] = "active"
    winters.B4 = tk.Button(tabWinters, text='Plot consumed', state="disabled", command=pltConsumedWinters)
    winters.B4.grid(row=1, column=winters.buttonsCol + 2)

    globalDeclareValues()

    # --- properties for winters method ---
    # ["multiplicative", "additive"]
    winters.WintersVersionStr = tk.StringVar(tabWinters)
    winters.WintersVersionStr.set(wintersVersionsOption[0])
    winters.versionButt = tk.OptionMenu(tabWinters, winters.WintersVersionStr, *wintersVersionsOption)
    winters.versionButt.grid()
    # periods length
    # get needed variables
    winters.periodTime = tk.Entry(tabWinters)
    winters.overTakeTime = tk.Entry(tabWinters)
    winters.periodTime.grid()
    winters.overTakeTime.grid()
    # prompts for props
    winters.WintersVersionStrPrompt = tk.Label(tabWinters, text = "Winters version:")
    winters.periodTimePrompt = tk.Label(tabWinters, text="Period length (m):")
    winters.overTakeTimePrompt = tk.Label(tabWinters, text="Overtake length (h):")
    winters.versionButt.grid(row = 2, column = winters.buttonsCol + 2)
    winters.WintersVersionStrPrompt.grid(row = 2, column = winters.buttonsCol + 1)
    winters.periodTime.grid(row = 3, column = winters.buttonsCol + 2)
    winters.periodTimePrompt.grid(row = 3, column = winters.buttonsCol + 1)
    winters.overTakeTime.grid(row = 4, column = winters.buttonsCol + 2)
    winters.overTakeTimePrompt.grid(row = 4, column = winters.buttonsCol + 1)
    # --- end of declaring properties for winters method ---

    root.mainloop()