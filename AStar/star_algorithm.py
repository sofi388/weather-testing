import csv
import heapq

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

results = []


# Read csv
def read_csv(filename):
    with open(filename, newline='') as f_input:
        return [list(map(float, row)) for row in csv.reader(f_input)]


# Make a grid for algorithm
def make_grid(filename, depth):
    global l_replace2
    arrayDepth = read_csv(filename)
    mas = []
    for row1 in arrayDepth:
        l_replace2 = [1 if (i == 9999.0 or i < depth) else 0 for i in row1]
        mas.append(l_replace2)
    return mas


# Make more wind
def make_more_wind(filename, file_res, param):
    global l_replace2
    arrayDepth = read_csv(filename)
    mas = []
    for row1 in arrayDepth:
        l_replace2 = [i + param for i in row1]
        mas.append(l_replace2)
    with open(file_res, 'w', newline='') as file:
        my_writer = csv.writer(file, delimiter=',')
        my_writer.writerows(mas)
    return mas


# Make one combined map with wind & surface
def wind_and_surface(file_wind, file_surface):
    global l_replace
    arrayWind = read_csv(file_wind)
    arraySurface = read_csv(file_surface)
    mas = []
    for row in arraySurface:
        for i in row:
            if i == 9999:
                var = arrayWind[i] == 9999


#############################################################################
# Get ready for the algorithm
#############################################################################

res = make_grid('50x50/wind_strength.csv', 1)
print(res)
mydata = res
grid = np.array(mydata)

data = read_csv('50x50/wind_strength.csv')

# Starting point and goal point

start = (3, 3)
goal = (13, 3)


#############################################################################
# Heuristic function for path scoring
#############################################################################

# Change the heuristic here to the speed formula at each point
# a - current, b - neighbour

def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def wind_heuristic(a, b, wind_str):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) + 1 / wind_str[b[0]][b[1]]


#############################################################################
# Load wind direction data
#############################################################################

wind_dir = read_csv('50x50/wind_direction.csv')
wind_strength = read_csv('50x50/wind_strength.csv')


##############################################################################
# Path finding function
##############################################################################

def astar(array, start_point, goal_point, vessel_type, max_wind, min_wind):
    # Neighborhood. You can try to modify it here and expand to 16/24.
    # Or iterate over the neighborhood depending on the situation

    neighbors8 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    neighbours16 = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (2, -2), (-2, 2), (-2, -2), (-1, 2), (1, 2), (2, 1),
                    (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]

    close_set = set()
    came_from = {}
    g_score = {start_point: 0}
    f_score = {start_point: heuristic(start_point, goal_point)}
    o_heap = []
    heapq.heappush(o_heap, (f_score[start_point], start_point))

    while o_heap:
        current = heapq.heappop(o_heap)[1]
        if current == goal_point:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        close_set.add(current)
        for i, j in neighbours16:
            neighbour = current[0] + i, current[1] + j
            above_wind = 0
            bad_wind_flag = 0
            # upwind restrictions for 16 neighbours
            if vessel_type == 1:
                if i == -2 and j == 0 and wind_dir[neighbour[0]][neighbour[1]] == 0 or \
                        i == -2 and j == 2 and wind_dir[neighbour[0]][neighbour[1]] == 45 or \
                        i == 0 and j == 2 and wind_dir[neighbour[0]][neighbour[1]] == 90 or \
                        i == 2 and j == 2 and wind_dir[neighbour[0]][neighbour[1]] == 135 or \
                        i == 2 and j == 0 and wind_dir[neighbour[0]][neighbour[1]] == 180 or \
                        i == 2 and j == -2 and wind_dir[neighbour[0]][neighbour[1]] == 225 or \
                        i == 0 and j == -2 and wind_dir[neighbour[0]][neighbour[1]] == 270 or \
                        i == -2 and j == -2 and wind_dir[neighbour[0]][neighbour[1]] == 315:
                    above_wind = 1
                else:
                    above_wind = 0
                if wind_strength[neighbour[0]][neighbour[1]] <= min_wind or wind_strength[neighbour[0]][neighbour[1]] >= max_wind:  # TEST THIS!!!!!!!!!
                    bad_wind_flag = 1
                else:
                    bad_wind_flag = 0
            if above_wind != 1:  # not death zone with headwind
                if bad_wind_flag != 1:  # not zero wind or not crucial wind
                    if vessel_type == 1:  # vessel is a sailboat
                        tentative_g_score = g_score[current] + wind_heuristic(current, neighbour,
                                                                              wind_strength)  # heuristic(current, neighbour)
                    else: # vessel is a motorboat
                        tentative_g_score = g_score[current] + heuristic(current, neighbour)
                    if 0 <= neighbour[0] < array.shape[0]:
                        if 0 <= neighbour[1] < array.shape[1]:  # избегать препятствия "внутри окрестностей"
                            if array[neighbour[0]][neighbour[1]] == 1 or array[neighbour[0] - 1][neighbour[1]] == 1 \
                                    or array[neighbour[0]][neighbour[1] - 1] == 1 or array[neighbour[0]][
                                neighbour[1]] == 1 or array[neighbour[0] + 1][neighbour[1] - 1] == 1 or \
                                    array[neighbour[0] + 1][neighbour[1] + 1] == 1 \
                                    or array[neighbour[0] - 1][neighbour[1] + 1] == 1:
                                continue
                        else:
                            # array bound y walls
                            continue
            else:
                # array bound x walls
                continue

            # Compare f
            if neighbour in close_set and tentative_g_score >= g_score.get(neighbour, 0):
                continue
            if tentative_g_score < g_score.get(neighbour, 0) or neighbour not in [i[1] for i in o_heap]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(neighbour, goal_point)
                heapq.heappush(o_heap, (f_score[neighbour], neighbour))
    return False


##############################################################################
# Calculate route
##############################################################################
# parameters: grid, start, goal, vessel_type, max_wind, min_wind
route = astar(grid, start, goal, 1, 10, 2)
route = route + [start]
route = route[::-1]
print(route)

##############################################################################
# Plot the path
##############################################################################

# extract x and y coordinates from route list
x_coordinates = []
y_coordinates = []
for i in (range(0, len(route))):
    x = route[i][0]
    y = route[i][1]
    x_coordinates.append(x)
    y_coordinates.append(y)
# plot map and path


# необходимо сделать метод "совмещенной карты"
data = read_csv('50x50/wind_strength.csv')
# '#6271b7'
cmap = colors.ListedColormap(
    ['#6e6e6e', '#5069AB', '#39619f', '#427DA4', '#4a94a9', '#4C9094', '#4d8d7b', '#509969', '#53a553', '#46A246',
     '#359f35', '#7C9E44', '#a79d51', '#A38E46', '#9f7f3a', '#AC632C', '#b83c17', '#813a4e',
     '#af5088', '#754a93', '#6d61a3', '#6a513c'])
bounds = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 19.0, 21.0, 23.0,
          25.0, 27.0, 9998.0]
norm2 = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(50, 50))
ax.imshow(data, cmap=cmap, norm=norm2)
ax.scatter(start[1], start[0], marker="*", color="blue", s=200)
ax.scatter(goal[1], goal[0], marker="*", color="red", s=200)
ax.plot(y_coordinates, x_coordinates, color="black")
plt.show()
