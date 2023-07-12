import csv
import heapq

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

#############################################################################
# Polar diagram for elan sailboat
#############################################################################
elan_speed = [[2, 2.5, 4.2, 4.8, 4.9, 4.2, 3, 2],  # 1 m/s
              [2, 2.5, 4.2, 4.8, 4.9, 4.2, 3, 2],  # 2 m/s
              [3, 3.9, 6, 5.8, 5.5, 4, 3.5, 3.3],  # 3 m/s
              [3, 3.9, 6, 5.8, 5.5, 4, 3.5, 3.3],  # 4 m/s
              [5, 6, 7, 7.9, 7.5, 7, 5.5, 3.9],  # 5 m/s
              [5, 6, 7, 7.9, 7.5, 7, 5.5, 3.9],  # 6 m/s
              [5.5, 6, 7, 8.2, 8.2, 7.7, 6.9, 5.6],  # 7 m/s
              [5.5, 6, 7, 8.2, 8.2, 7.7, 6.9, 5.6],  # 8 m/s
              [6.3, 7.2, 8.3, 8.5, 9, 9.6, 8.5, 7.8],  # 9 m/s
              [6.3, 7.2, 8.3, 8.5, 9, 9.6, 8.5, 7.8],  # 10 m/s
              [6.4, 7.5, 8.5, 9.5, 10.2, 11, 9.5, 8.8],  # 11 m/s
              [6.4, 7.5, 8.5, 9.5, 10.2, 11, 9.5, 8.8],  # 12 m/s
              [6.9, 7.8, 8.7, 9.9, 10.2, 12, 11.4, 10.2],  # 13 m/s
              [6.9, 7.8, 8.7, 9.9, 10.2, 12, 11.4, 10.2], ]  # 14 m/s


#############################################################################
# Some functions
#############################################################################

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

res = make_grid('100x100/wind_strength_more.csv', 1)
mydata = res
grid = np.array(mydata)

data = read_csv('100x100/wind_strength_more.csv')


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

wind_dir = read_csv('100x100/wind_direction.csv')
wind_strength = read_csv('100x100/wind_strength_more.csv')

##############################################################################
# Path finding function
##############################################################################
wind_vec_path = []


def astar(array, start_point, goal_point, vessel_type, max_wind, min_wind, hybrid):
    # Neighborhood. You can try to modify it here and expand to 16/24.
    # Or iterate over the neighborhood depending on the situation

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
            strong_wind_flag = 0
            light_wind_flag = 0
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
                if wind_strength[neighbour[0]][neighbour[1]] >= max_wind:
                    strong_wind_flag = 1
                else:
                    strong_wind_flag = 0

                if wind_strength[neighbour[0]][neighbour[1]] <= min_wind:
                    light_wind_flag = 1
                else:
                    light_wind_flag = 0
            if wind_strength[neighbour[0]][neighbour[1]] >= 24:
                surface = 1
            else:
                surface = 0
            if above_wind != 1 or (hybrid == 1 and light_wind_flag == 1):  # not death zone with headwind
                if strong_wind_flag != 1 or vessel_type == 0:  # not crucial wind
                    if surface != 1:
                        if vessel_type == 1 and hybrid == 0:  # vessel is a sailboat, hybrid no
                            tentative_g_score = g_score[current] + wind_heuristic(current, neighbour,
                                                                                  wind_strength)
                        if vessel_type == 1 and hybrid == 1:  # vessel is a sailboat, hybrid yes
                            if light_wind_flag != 1:
                                tentative_g_score = g_score[current] + wind_heuristic(current, neighbour,
                                                                                      wind_strength)
                            else:
                                tentative_g_score = g_score[current] + heuristic(current, neighbour)
                        if vessel_type == 0:  # vessel is a motorboat
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
                        continue
                else:

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
# Starting point and goal point, other parameters

# case 1: avoid strong wind
# start = (3, 3)
# goal = (10, 40)

# case 2: upwind story
# start = (3, 3)
# goal = (30, 3)

# case 3: 100x100 upwind
# start = (6, 6)
# goal = (61, 6)

# case 4: 100x100 avoid strong wind
start = (6, 6)
goal = (18, 80)

# case 5: 100x100 обходим остров
# start = (7, 7)
# goal = (40, 7)

##############################################################################
# Parameters
##############################################################################
motor_speed = 15  # 15 knt
map_scale = 1.1  # 1 cell is 1.1 mile
max_wind = 14
min_wind = 2

##############################################################################
# calculate sailing route
##############################################################################
s_route = astar(grid, start, goal, 1, max_wind, min_wind, 0)
s_route = s_route + [start]
s_route = s_route[::-1]
print(s_route)

# extract x and y coordinates from 1 route list
x_coordinates = []
y_coordinates = []
for i in (range(0, len(s_route))):
    x = s_route[i][0]
    y = s_route[i][1]
    x_coordinates.append(x)
    y_coordinates.append(y)

##############################################################################
# calculate power route
##############################################################################
m_route = astar(grid, start, goal, 0, max_wind, min_wind, 0)
m_route = m_route + [start]
m_route = m_route[::-1]
print(m_route)

# extract x and y coordinates from 2 route list
x2_coordinates = []
y2_coordinates = []
for i in (range(0, len(m_route))):
    x = m_route[i][0]
    y = m_route[i][1]
    x2_coordinates.append(x)
    y2_coordinates.append(y)

##############################################################################
# calculate hybrid route
##############################################################################
h_route = astar(grid, start, goal, 1, max_wind, min_wind, 1)
h_route = h_route + [start]
h_route = h_route[::-1]
print(h_route)

# extract x and y coordinates from 2 route list
x3_coordinates = []
y3_coordinates = []
for i in (range(0, len(h_route))):
    x = h_route[i][0]
    y = h_route[i][1]
    x3_coordinates.append(x)
    y3_coordinates.append(y)

##############################################################################
# Plot the path
##############################################################################
# метод "совмещенной карты"
data = read_csv('100x100/wind_strength_more.csv')
cmap = colors.ListedColormap(
    ['#6e6e6e', '#5069AB', '#39619f', '#427DA4', '#4a94a9', '#4C9094', '#4d8d7b', '#509969', '#53a553', '#46A246',
     '#359f35', '#7C9E44', '#a79d51', '#A38E46', '#9f7f3a', '#AC632C', '#b83c17', '#813a4e',
     '#af5088', '#754a93', '#6d61a3', '#beb887'])
bounds = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 19.0, 21.0, 22.0,
          23.0, 9998.0]
norm2 = colors.BoundaryNorm(bounds, cmap.N)
fig, ax = plt.subplots(figsize=(100, 100))
ax.imshow(data, cmap=cmap, norm=norm2)
ax.scatter(start[1], start[0], marker="*", color="blue", s=200)
ax.scatter(goal[1], goal[0], marker="*", color="red", s=200)
ax.plot(y_coordinates, x_coordinates, color="black")  # sail
ax.plot(y2_coordinates, x2_coordinates, color="yellow")  # motor
ax.plot(y3_coordinates, x3_coordinates, color="black")  # hybrid
plt.show()

print(x2_coordinates)
print(y2_coordinates)
print(x3_coordinates)
print(y3_coordinates)

res = 0
time = 0
for index in range(len(x_coordinates) - 1):
    dist = np.sqrt(
        (x_coordinates[index] - x_coordinates[index + 1]) * (x_coordinates[index] - x_coordinates[index + 1]) + (

                y_coordinates[index] - y_coordinates[index + 1]) * (
                y_coordinates[index] - y_coordinates[index + 1]))
    res += dist
    time += dist / elan_speed[int(wind_strength[x_coordinates[index + 1]][y_coordinates[index + 1]]) - 1][
        int(90 / 22.5) - 1]

# Pick size 200 km x 200 km
# cell = 1,1 miles
print("\n Sail distance: ")
print(res * map_scale)
print(" miles")

print("\n Sail time: ")
print(time)
print(" hours")

res = 0
time = 0
for index in range(len(x2_coordinates) - 1):
    dist = np.sqrt(
        (x2_coordinates[index] - x2_coordinates[index + 1]) * (x2_coordinates[index] - x2_coordinates[index + 1]) + (
                y2_coordinates[index] - y2_coordinates[index + 1]) * (
                y2_coordinates[index] - y2_coordinates[index + 1]))
    res += dist
    time += dist / motor_speed

print("\n Power distance: ")
print(res * map_scale)
print(" miles")

print("\n Power time: ")
print(time)
print(" hours")

# make_more_wind('100x100/wind_strength.csv', '100x100/wind_strength2.csv', 1)
