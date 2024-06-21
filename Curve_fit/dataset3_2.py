import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filepath = "dataset3.txt"


def curve_fit_complex(file):
    f = open(file, 'r')

    x, y = read(f)
    plt.plot(x, y, label="Noisy_Data")

    # Initial Guess close to their original values for all h, c, k, T
    initial_guess = [6.6*1e-34, 3*1e8, 1e-23, 5000]
    z = curve_fit(bb_rad_p, x, y, p0=initial_guess)[0]
    y_curve_fit = bb_rad_p(x, z[0], z[1], z[2], z[3])
    plt.plot(x, y_curve_fit, 'r', label='Curve_fit_for_all_values')

    plt.legend()
    plt.savefig("dataset3_2.png")


def bb_rad_p(x, h, c, k, T):
    numerator = 2.0 * h * x ** 3 / c ** 2
    denominator = np.exp((h * x) / (k * T)) - 1
    return numerator / denominator


def read(f):
    # A function to read the values of x and y
    sfp = f.readlines()
    x = []
    y = []
    for i in range(len(sfp)):
        dummy = sfp[i].split()
        x.append(float(dummy[0]))
        y.append(float(dummy[1]))
    return np.array(x), np.array(y)


curve_fit_complex(filepath)