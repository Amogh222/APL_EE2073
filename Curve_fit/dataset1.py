import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines  # This import just to add a legend for the error bars

filepath = 'dataset1.txt'


def curve_fit_linear(file):
    f = open(file, 'r')
    x, y = read(f)

    # Assumed function is y = a * x + b
    m = np.column_stack([x, np.ones(len(x))])  # Formation of the m matrix
    (a, b), _, _, _ = np.linalg.lstsq(m, y, rcond=None)

    y_est = st_line(a, x, b)

    error = error_bar(y, y_est)

    # Plotting the noisy data twice to not get a different legend
    line1, = plt.plot(x, y, "#a6f1a6", alpha=.5, label="Noisy data", marker='o', ls='-', ms=.5)
    plt.errorbar(x, y, fmt='#a6f1a6', alpha=.5, yerr=error, ecolor='r', errorevery=(0, 25))

    # Line 3 for plotting error bar legend
    line2, = plt.plot(x, y_est, "k", label='Estimation')
    line3 = mlines.Line2D([], [], color='red', label='ErrorBar')
    plt.legend(loc=2, handles=[line1, line2, line3])
    plt.savefig("dataset1.png")


def read(f):
    # A function to read the data
    sfp = f.readlines()
    x = []
    y = []
    for i in range(len(sfp)):
        dummy = sfp[i].split()
        x.append(float(dummy[0]))
        y.append(float(dummy[1]))
    return np.array(x), np.array(y)


def st_line(t, m, c):
    return m * t + c


def error_bar(y, y_t):
    # Funtion to get errors for each point in dataset
    err_list = []
    i = 0
    while i < len(y):
        err_list.append(abs(y[i] - y_t[i]))
        i += 1
    err_list = np.array(err_list)
    return err_list


curve_fit_linear(filepath)