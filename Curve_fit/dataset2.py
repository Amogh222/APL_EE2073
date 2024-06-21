import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filepath = "dataset2.txt"


def read(f):
    # Function to get the x and y values
    sfp = f.readlines()
    x = []
    y = []
    for i in range(len(sfp)):
        dummy = sfp[i].split()
        x.append(float(dummy[0]))
        y.append(float(dummy[1]))
    return np.array(x), np.array(y)


def curve_fit_complex(file):
    f = open(file, 'r')
    x, y = read(f)

    plt.plot(x, y, 'b', alpha=.5, label="Noisy Data")

    # The Time period T of the curve
    T = 2 * tp(x, y)

    # Forming the M matrix and using the linalg function
    M = np.column_stack([np.ones(len(x)), np.sin(((2 * np.pi) / T) * x), np.sin(((2 * np.pi) / (T/3)) * x),
                         np.sin(((2 * np.pi) / (T/5)) * x)])
    p, _, _, _ = np.linalg.lstsq(M, y, rcond=None)
    y_linalg = f1(x, p[0], p[1], p[2], p[3], T)
    plt.plot(x, y_linalg, 'k', label="Linalg Estimation")

    # Curve_fit function
    initial_guess = [1, 1, 1, 1, 2]
    z = curve_fit(f1, x, y, p0=initial_guess)[0]
    y_curve_fit = f1(x, z[0], z[1], z[2], z[3], z[4])
    plt.plot(x, y_curve_fit, 'r', label="Curve_fit estimation")

    plt.legend(loc=2)
    plt.savefig("dataset2.png")


def f1(x, p0, p1, p2, p3, t):
    return p0 + p1 * np.sin(((2 * np.pi) / t) * x) + p2 * np.sin(((2 * np.pi) / (t/3)) * x) + p3 * np.sin(
        ((2 * np.pi) / (t/5)) * x)


def tp(x, y):
    # Function to get the T/2 value
    amp = max(y)
    dummy1 = 100
    closest_max = 0

    for i in range(len(y)):
        if y[i] != amp:
            dummy2 = amp + y[i]
            if dummy2 < dummy1:
                dummy1 = dummy2
                closest_max = i
    t1 = abs(x[closest_max] - x[np.where(y == amp)[0][0]])
    return t1


curve_fit_complex(filepath)
