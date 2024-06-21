import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.constants as sc

filepath = "dataset3.txt"


def curve_fit_complex(file):
    f = open(file, 'r')

    x, y = read(f)
    plt.plot(x, y, label="Noisy_Data")

    # Initial Guess only for T
    z = curve_fit(bb_rad, x, y, p0=1000)[0]
    y_curve_fit = bb_rad(x, z[0])
    plt.plot(x, y_curve_fit, 'k', label="Curve_fit_for_temp")

    plt.legend()
    plt.savefig("dataset3_1.png")


def bb_rad(x, T):
    h = sc.h
    c = sc.c
    k = sc.k
    numerator = 2.0 * h * x ** 3 / c ** 2
    denominator = np.exp((h * x) / (k * T)) - 1
    return numerator / denominator


def read(f):
    # A function to get the values of x and y
    sfp = f.readlines()
    x = []
    y = []
    for i in range(len(sfp)):
        dummy = sfp[i].split()
        x.append(float(dummy[0]))
        y.append(float(dummy[1]))
    return np.array(x), np.array(y)


curve_fit_complex(filepath)