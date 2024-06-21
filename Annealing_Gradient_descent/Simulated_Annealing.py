import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Filename and path name can be changed here
pathname = "Assignment_6/f1_10_city.txt"


def tsp(file):
    data = np.loadtxt(file, skiprows=1)
    cities = [element for element in data]
    cities = np.array(cities)

    # Total Cities
    n = len(cities)

    fig, ax = plt.subplots()

    # The data for the Annealing stuff
    temp = 10000
    decayrate = .995
    best_distance = 1000000
    iterations = 30000

    # Defining a random starting order
    best_order = np.arange(n)
    np.random.shuffle(best_order)
    initial_order = list(best_order)
    initial_distance = distance(cities, initial_order)

    # A list used for animation
    order_list = []

    for k in range(iterations):

        # New copy of the best order
        current_order = best_order.copy()
        current_distance = distance(cities, current_order)

        # Near order is the current order with 2 cities randomly interchanged
        near_order = current_order.copy()
        i, j = random.sample(range(len(cities)), 2) # 2 randomly generated nnumbers between 0 and n-1
        near_order[i], near_order[j] = near_order[j], near_order[i]
        near_distance = distance(cities, near_order)

        # Diff in distances
        delta_distance = near_distance - current_distance

        # The part where we update the current order if less than or based on probability
        if delta_distance < 0 or np.random.random_sample() < np.exp(-delta_distance / temp):
            current_order = near_order.copy()
            current_distance = near_distance

        # Updating the Best Distance
        if current_distance < best_distance:
            best_order = current_order.copy()
            best_distance = current_distance

        # Decreasing the temp to reduce the probability
        temp = temp * decayrate
        order_list.append(current_order)
        print(f"Progress: {int((k+1) * 100 / iterations)}%", end='\r')

    # Iteration variable for the animation
    ii = 0

    # Function for Animation
    def plot(frame):
        nonlocal cities, ii

        # Transpose to get the x and y coordinates
        new_cities = cities.transpose()
        x_order = new_cities[0][order_list[ii*50]]
        y_order = new_cities[1][order_list[ii*50]]

        ax.clear()
        # Plotting the data
        xall = np.append(x_order, x_order[0])
        yall = np.append(y_order, y_order[0])
        ax.plot(xall, yall, 'ko', markersize=5)
        ax.plot(xall, yall, 'g-')
        ii += 1

    # To save the animation as a gif
    writer = PillowWriter(fps=30)
    ani = FuncAnimation(fig, plot, frames=int(iterations/50) - 1, interval=10, repeat=False)
    ani.save("Animation.gif", writer=writer)
    print(f"Percentage Improvement: {(initial_distance-best_distance)*100/initial_distance}%")

    return best_order


# Function for distance between two points
def distcost(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# Function for calculating the total distance in the closed path
def distance(cities, cityorder):
    totaldistance = 0
    cities = cities.transpose()
    x = cities[0][cityorder]
    y = cities[1][cityorder]
    for i in range(len(x)):
        totaldistance += distcost(x[i - 1], y[i - 1], x[i], y[i])
    return totaldistance



print(tsp(pathname))
