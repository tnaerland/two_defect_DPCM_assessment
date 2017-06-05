import matplotlib.pyplot as plt
import matplotlib.markers as markers
import matplotlib
import numpy as np
from numpy import *
from pylab import *
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
from matplotlib.font_manager import FontProperties
import os, os.path
from tempfile import mkstemp
from shutil import move
from os import remove, close
import csv
import os, os.path
import pickle
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from os.path import join, dirname, abspath
import xlrd
import pprint
import json

#Constants
p0 = 2e15  # cm-3

# Firm constants:
Ev = 0.0  # eV
Ec = 1.132  # eV
k_b = 1.38e-23  # m2Kgs-2K-1
q = 1.602e-19  # C

def calculate_tau_effective(delta_n, T, tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2):

    #Temperature dependence
    Nc = 2.86e19 * (T/300.0)**1.58 #cm-3 #Green 1990
    Nv = 3.1e19 * (T/300.0)**1.85 #cm-3 #Green 1990
    Eg = 1.1752165 - ((0.000473*T**2)/(T+636.0)) #eV Altermatt 2011
    ni = 2.9738e19 * ((T/300.0)**1.5)*exp((-q*Eg)/(2*k_b*T)) #cm-3 Mackel 2012
    n0 = ni**2/p0
    n = n0 + delta_n
    p = p0 + delta_n

    # SRH Equations:
    n1_1 = Nc * exp((-(Ec - Et_1) * q) / (k_b * T))
    p1_1 = Nv * exp((-(Et_1 - Ev) * q / (k_b * T)))
    tau_SRH_1 = 1e6*((tau_p0_1/k_1)*(p0 + p1_1 + delta_n)+tau_p0_1*(n1_1+delta_n))/(p0+n0+delta_n) #p-type

    n1_2 = Nc * exp((-(Ec - Et_2) * q) / (k_b * T))
    p1_2 = Nv * exp((-(Et_2 - Ev) * q / (k_b * T)))
    tau_SRH_2 = 1e6*((tau_p0_2/k_2)*(p0 + p1_2 + delta_n)+tau_p0_2*(n1_2+delta_n))/(p0+n0+delta_n) #p-type

    #tau_SRH = 1e6*(tau_p0*(n0 + n1 + delta_n)+((tau_p0/k)*(p1+delta_n)))/(n0+p0+delta_n)  # n-type
    #tau_eff = 1/((1/tau_SRH_1)+(1/tau_SRH_2)+(1/tau_intr))
    tau_eff = 1/((1/tau_SRH_1)+(1/tau_SRH_2))

    return tau_eff

Temperatures = [298, 328, 358, 388, 418, 448, 478]
Injections = np.logspace(12, 17, num=100)

def calculate_all_tau_effs(tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2):
    all_tau_effs=[]
    for T in Temperatures:
        tau_eff_full_curve = []
        for delta_n in range(0, len(Injections)):
            delta_n_value = Injections[delta_n]
            tau_eff = calculate_tau_effective(delta_n_value, T, tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2)
            tau_eff_full_curve.append(tau_eff)
        all_tau_effs.append(tau_eff_full_curve)
    return all_tau_effs


def simulate_lifetime(all_tau_effs, tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2, title, directory):
    fig = plt.figure(2,figsize=(6,5.6))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xscale('log')
    plt.title(title)
    text_style = dict(horizontalalignment='right', verticalalignment='center',
                      fontsize=12, fontdict={'family': 'monospace'})
    marker_style = dict(linestyle=':', color='cornflowerblue', markersize=10)

    plt.ylabel('Minority carrier lifetime [$\mu s$]',fontsize=16)
    plt.xlabel('Excess minority carrier concentration $\Delta n$ [$cm^3$]',fontsize=16)

    color=iter(cm.bwr(np.linspace(0,1,len(all_tau_effs))))
    for i in all_tau_effs:
        c=next(color)
        plt.plot(Injections, i, 'k.',linewidth=1.5, markersize=10, markeredgewidth=0.5, markeredgecolor='k', c=c,fillstyle='full')
    #plt.plot(Injections,all_tau_effs[0],'k.',label='p0=1e16cm-3, k=200, Et=0.24eV \nT-range=298-478K', markersize=5, markeredgewidth=1, markeredgecolor='k',fillstyle='full')

    #Legend without line
    leg1 = Rectangle((0, 0), 0, 0, alpha=0.0)
    plt.legend([leg1], ['$k_1$='+str(k_1)+', $E_{t,1}$='+str(Et_1)+'\n $k_2$='+str(k_2)+', $E_{t,2}$='+str(Et_2)+'\n T-range=298-478K'], handlelength=0, loc='upper center')

    ax.set_ylim(1, 1000)
    ax.set_yscale('log')
    ax.set_xlim(1e13, 1e16)
    plt.tick_params(labelsize=14)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(directory + title + '.png')
    plt.close()

    #Write to file list of tau_effs
    Delta_n_values = np.logspace(13, 16, num=6)
    #print Delta_n_values
    list_of_tau_effs_for_all_Ts=[]
    for T in Temperatures:
        tau_eff_delta_n_values = []
        for i in Delta_n_values:
            tau_eff = calculate_tau_effective(i, T, tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2)
            tau_eff_delta_n_values.append(tau_eff)
        list_of_tau_effs_for_all_Ts.append(tau_eff_delta_n_values)

    first_T = list_of_tau_effs_for_all_Ts[0]
    second_T = list_of_tau_effs_for_all_Ts[1]
    third_T = list_of_tau_effs_for_all_Ts[2]
    forth_T = list_of_tau_effs_for_all_Ts[3]
    fift_T = list_of_tau_effs_for_all_Ts[4]
    sixt_T = list_of_tau_effs_for_all_Ts[5]
    seventh_T = list_of_tau_effs_for_all_Ts[6]

    out = open(directory + title + ' curves.txt', 'w')
    out.write(str(first_T).strip('[]')+'\n')
    out.write(str(second_T).strip('[]')+'\n')
    out.write(str(third_T).strip('[]')+'\n')
    out.write(str(forth_T).strip('[]')+'\n')
    out.write(str(fift_T).strip('[]')+'\n')
    out.write(str(sixt_T).strip('[]')+'\n')
    out.write(str(seventh_T).strip('[]')+'\n')
    out.close()

# Execute
# Read directory structure to find tau_p0_data files for combination of defects.
root_path = './tau_p0_data/'
tau_p0_data_files = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        full_path = join(root, file)
        ext = os.path.splitext(file)[1]
        if ext == '.txt':
            tau_p0_data_files.append(full_path)

tau_p0_data = []
for combination in tau_p0_data_files:
    with open(combination, 'r') as data_file:
        print combination
        data = json.load(data_file)
        data['directory'] = str(combination).rsplit('tau_p0_rawdata.txt', 1)[0]
        tau_p0_data.append(data)

for data in tau_p0_data:
    # Run five plots and data files, one for each fraction a,b,c,d,e (0.01, 0.25, 0.5, 0.75, 0.99)
    Et_1 = data['Et_1']
    k_1 = data['k_1']
    Et_2 = data['Et_2']
    k_2 = data['k_2']
    directory = data['directory']
    print "Directory is:"
    print directory

    fractions = {"a": 0.5, "b": 0.625, "c": 0.75, "d": 0.875}
    for fraction in ["a", "b", "c", "d"]:
        tau_p0_1 = data['tau_p0_1_' + fraction]
        tau_p0_2 = data['tau_p0_2_' + fraction]
        title = data['impurity'] + " combined with " + data['combined_with'] + ' for fraction ' + fraction
        all_tau_effs = calculate_all_tau_effs(tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2)
        simulate_lifetime(all_tau_effs, tau_p0_1, Et_1, k_1, tau_p0_2, Et_2, k_2, title, directory)