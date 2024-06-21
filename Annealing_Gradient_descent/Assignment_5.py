import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


def gradient_descent(f, f_der, lim):

    # Finding whether 2D or 1d
    variables = len(lim)
    fig = plt.figure()

    # Total Iterations can be changed
    iterations = 10000

    if variables == 1:
        # 2D plane plot for the 1D function
        xbase = np.linspace(lim[0][0], lim[0][1], 100)
        ybase = f(xbase)
        ax = plt.axes()

        # 2D plot
        ax.plot(xbase, ybase)
        ax.set_xlabel('x - axis')
        ax.set_ylabel('y - axis')

        # Empty lists to be used later
        xall, yall = [], []
        lnall, = ax.plot([], [], 'ro')
        lngood, = ax.plot([], [], 'go', markersize=10)

        # Learning rate
        lr = 0.1

        # Generating a random value from the limits
        best = np.array([np.random.choice(np.linspace(lim[0][0], lim[0][1], 100))])

        for iter1 in range(iterations):
            # f_der_mat containing the derivative values at that point
            if len(f_der) == 0:
                f_der_mat = np.array([derivative(f, best[0])])
            else:
                f_der_mat = np.array(f_der[0](best[0]))

            # Actual Gradient Descent
            best = best - f_der_mat * lr
            xall.append(best[0])
            yall.append(f(best[0]))

    if variables == 2:
        # Create the axis and function
        xbase = np.linspace(lim[0][0], lim[0][1], 100)
        ybase = np.linspace(lim[1][0], lim[1][1], 100)

        # Mesh Formation for 3D surface
        X, Y = np.meshgrid(xbase, ybase)
        Z = f(X, Y)

        ax = plt.axes(projection='3d')
        # Graph Plot
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha=.5)

        # Scatter Plot
        scatter_1, = ax.plot([], [], [], c='r', marker='o')
        scatter_2, = ax.plot([], [], [], c='g', marker='o')
        ax.set_xlabel('x - axis')
        ax.set_ylabel('y - axis')
        ax.set_zlabel('z - axis')

        # Empty lists to be used later
        zall, xall, yall = [], [], []
        # Learning rate for x and y
        lr = [0.01, .01]

        # Generating a random value from the limits
        best = np.array([np.random.choice(np.linspace(lim[0][0], lim[0][1], 100)),
                         np.random.choice(np.linspace(lim[1][0], lim[1][1], 100))])

        for iter1 in range(iterations):
            # f_der_mat containing the derivative values at that point
            f_der_mat = np.array([f_der[0](best[0], best[1]), f_der[1](best[0], best[1])])

            # Actual Gradient Descent
            best = best - f_der_mat * lr

            # For cases where derivative value blows up
            if abs(best[0]) > 10000:
                best[0] = np.random.choice(np.linspace(lim[0][0], lim[0][1], 100))
            if abs(best[1]) > 10000:
                best[1] = np.random.choice(np.linspace(lim[1][0], lim[1][1], 100))
            else:
                xall.append(best[0])
                yall.append(best[1])
                zall.append(f(best[0], best[1]))

    # Count Variable for Animation
    i = 0

    # Function for 1D plot
    def plot_1d(frame):
        nonlocal xall, yall, i, lnall, lngood
        lnall.set_data(xall[:i*50], yall[:i*50])
        lngood.set_data(xall[i*50], yall[i*50])
        i += 1

    # Function for 2D plot
    def plot_2d(frame):
        nonlocal xall, yall, zall, i
        scatter_1.set_data(xall[:i*50], yall[:i*50])
        scatter_1.set_3d_properties(zall[:i*50])
        scatter_2.set_data([xall[i*50]], [yall[i*50]])
        scatter_2.set_3d_properties([zall[i*50]])
        i += 1

    if variables == 1:
        ani = FuncAnimation(fig, plot_1d, frames= int(iterations/50) - 1, interval=1, repeat=False)
        ani.save("Animation.gif", writer=PillowWriter(fps=20))
        print("Minimum =", yall[-1], "at x =", xall[-1])
    if variables == 2:
        ani = FuncAnimation(fig, plot_2d, frames=int(iterations/50) - 1, interval=1, repeat=False)
        ani.save("Animation.gif", writer=PillowWriter(fps=20))
        print("Minimum =", zall[-1], "at x =", xall[-1], "and y =", yall[-1])



def derivative(f, x):
    h = 1e-10
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)


def f1(x):
    return x ** 2 + 3 * x + 8


def f3(x, y):
    return x ** 4 - 16 * x ** 3 + 96 * x ** 2 - 256 * x + y ** 2 - 4 * y + 262


def df3_dx(x, y):
    return 4 * x ** 3 - 48 * x ** 2 + 192 * x - 256


def df3_dy(x, y):
    return 2 * y - 4


def f4(x, y):
    return np.exp(-(x - y) ** 2) * np.sin(y)


def df4_dx(x, y):
    return -2 * np.exp(-(x - y) ** 2) * np.sin(y) * (x - y)


def df4_dy(x, y):
    return np.exp(-(x - y) ** 2) * np.cos(y) + 2 * np.exp(-(x - y) ** 2) * np.sin(y) * (x - y)


def f5(x):
    return np.cos(x) ** 4 - np.sin(x) ** 3 - 4 * np.sin(x) ** 2 + np.cos(x) + 1


xlim5 = [0, 2 * np.pi]
ylim4 = [-np.pi, np.pi]
xlim4 = [-np.pi, np.pi]
xlim3 = [-10, 10]
ylim3 = [-10, 10]
xlim1 = [-5, 5]

# You can change the der list here
der = [df4_dx, df4_dy]

# Input the limits here
lim = [xlim4, ylim4]

# Main Function call change this here it can take any function
# gradient_descent(f, der, lim)

# Call whichever function you want
# gradient_descent(f1, [], [xlim1])
# gradient_descent(f3, [df3_dx, df3_dy], [xlim3, ylim3])
# gradient_descent(f4, [df4_dx, df4_dy], [xlim4, ylim4])
# gradient_descent(f5, [], [xlim5])
