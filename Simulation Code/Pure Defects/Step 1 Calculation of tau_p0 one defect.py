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
import sys

#Doping concentration
p0 = 2e15  # cm-3

#Concentration fraction
fractions=[1]

Et_1 = None
k_1 = None
tau_p0_1 = np.logspace(-7, 1, num=10000) # unit=s, decides on a tau_p0_1 range and calculates the tau_p0_2 range from there)





# Firm constants:
Ev = 0.0  # eV
Ec = 1.132  # eV
k_b = 1.38e-23  # m2Kgs-2K-1
q = 1.602e-19  # C

def calculate_tau_effective(delta_n, T, tau_p0_1):

    #Temperature dependence
    Nc = 2.86e19 * (T/300.0)**1.58 #cm-3 #Green 1990
    Nv = 3.1e19 * (T/300.0)**1.85 #cm-3 #Green 1990
    Eg = 1.1752165 - ((0.000473*T**2)/(T+636.0)) #eV Altermatt 2011
    ni = 2.9738e19 * ((T/300.0)**1.5)*exp((-q*Eg)/(2*k_b*T)) #cm-3 Mackel 2012
    n0 = ni**2/p0

    # SRH Equations:
    n1_1 = Nc * exp((-(Ec - Et_1) * q) / (k_b * T))
    p1_1 = Nv * exp((-(Et_1 - Ev) * q / (k_b * T)))
    tau_SRH_1 = 1e6*((tau_p0_1/k_1)*(p0 + p1_1 + delta_n)+tau_p0_1*(n1_1+delta_n))/(p0+n0+delta_n) #p-type


    #tau_SRH = 1e6*(tau_p0*(n0 + n1 + delta_n)+((tau_p0/k)*(p1+delta_n)))/(n0+p0+delta_n)  # n-type
    #tau_eff = 1/((1/tau_SRH_1)+(1/tau_SRH_2)+(1/tau_intr))
    tau_eff = 1/((1/tau_SRH_1))

    return tau_eff

	
	
	
#The temperatures to consider:	
Temperatures = [298, 328, 358, 388, 418, 448, 478]
#The injection range and number of points for the figure:
Injections = np.logspace(12, 17, num=100) #If num is changes "Injections[53] below will not any longer point to an injection level of 5e14cm-3


#In the following we are determining the values of tau_p0_1 and tau_p0_2 to maintain a tau_eff of approx 50 us at 5e14 cm-3 for the different fractions.

def calculate_lifetimes():
    results = []


    lifetime_at_5e14 = []
    meta_lifetime_at_5e14 = []
    for tau_p0_1_value in tau_p0_1:
        result = calculate_tau_effective(Injections[53], Temperatures[0], tau_p0_1_value) #Injection[53] equals 5e14 cm-3
        lifetime_at_5e14.append(result)
        meta_lifetime_at_5e14.append((tau_p0_1_value, result))

    closest_index = None
    closest_less_than_50 = 0
    closest_less_than_50_index = None
    closest_larger_than_50 = sys.maxint
    closest_larger_than_50_index = None
    for i, value in enumerate(lifetime_at_5e14):
        if 50 > value > closest_less_than_50:
            closest_less_than_50 = value
            closest_less_than_50_index = i
        if 50 < value < closest_larger_than_50:
            closest_larger_than_50 = value
            closest_larger_than_50_index = i


    if closest_less_than_50 > 0:
        closest_index = closest_less_than_50_index
    if closest_larger_than_50 < sys.maxint:
        closest_index = closest_larger_than_50_index

    if closest_less_than_50 > 0 and closest_larger_than_50_index < sys.maxint:
        if (closest_larger_than_50 - 50) < (50 - closest_less_than_50):
            closest_index = closest_larger_than_50_index
        else:
            closest_index = closest_less_than_50_index

    print closest_index

    results.append(meta_lifetime_at_5e14[closest_index][0])
    results.append(meta_lifetime_at_5e14[closest_index][1])

    return results



	# Listing of the impurities we are combining
impurities = [
    { "name": "CuI",
      "Et"      : 0.92,
      "k"       : 0.05
    },
    { "name": "CuII",
      "Et"      : 0.62,
      "k"       : 16.00
    },
    { "name": "PtI",
      "Et"      : 0.32,
      "k"       : 0.01
    },
    { "name": "Ti",
      "Et"      : 0.854,
      "k"       : 22.00
    },
    { "name": "Mo",
      "Et"      : 0.28,
      "k"       : 30.00
    },
    { "name": "Zn",
      "Et"      : 0.33,
      "k"       : 0.34
    },
    { "name": "PtII",
      "Et"      : 0.89,
      "k"       : 1.12
    },
    { "name": "Au",
      "Et"      : 0.574,
      "k"       : 0.02
    },
    { "name": "DefectX",
      "Et"      : 0.56,
      "k"       : 1.00
    }
]

#Printing results to the shell and to directories
results = []
# comparisons = []
for impurity in impurities:
    Et_1 = impurity["Et"]
    k_1 = impurity["k"]

    result = calculate_lifetimes()
    results.append(
        {
            "impurity"      : impurity["name"],
            "Et_1"          : impurity["Et"],
            "k_1"           : impurity["k"],
            "tau_p0_1_a"    : result[0],

                }
            )
print results
# print "Comparisons:"
# print comparisons
pprint.pprint(results)
print len(results)

# Make a directory structure and write to file for each dictionary in results
for result in results:
    directory = result["impurity"]

    path = './tau_p0_data/'+ directory
    try:
        os.makedirs(path)
    except OSError:
        pass
    with open(path + '/tau_p0_rawdata.txt', 'wb') as handle:
        json.dump(result, handle)

