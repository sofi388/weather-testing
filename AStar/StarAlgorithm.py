import numpy as np
import heapq
import matplotlib.pyplot as plt
import csv


##############################################################################
# plot grid
##############################################################################

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
    a = 18
    for row1 in arrayDepth:
        l_replace2 = [1 if (i == 9999.0 or i < depth) else 0 for i in row1]
        mas.append(l_replace2)
    return mas


# Make more wind
def make_more_wind(filename, fileres, param):
    global l_replace2
    arrayDepth = read_csv(filename)
    mas = []
    a = 18
    for row1 in arrayDepth:
        l_replace2 = [i + param for i in row1]
        mas.append(l_replace2)
    with open(fileres, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(mas)
    return mas


# Make a grid for algorithm
res = make_grid('depth.csv', 2)
print(res)

# Make new grid with more wind
result_wind = make_more_wind('wind1hour.csv', 'wind2hour.csv', 3)
result_wind2 = make_more_wind('wind2hour.csv', 'wind3hour.csv', 4)
result_wind3 = make_more_wind('wind3hour.csv', 'wind4hour.csv', -1)

#############################################################################
# Get ready for the algorithm
#############################################################################

mydata = res  # pd.read_csv("grid31x10.csv")
grid = np.array(mydata)

# start point and goal

start = (0, 0)
goal = (11, 8)


#############################################################################
# heuristic function for path scoring
#############################################################################

# Можно здесь поменять эвристику на формулу скорости в каждой точке
def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


##############################################################################
# path finding function
##############################################################################

def astar(array, start, goal):

    # Окрестность. Можно попытаться модифицировать именно здесь и расширить до 16/24. Или перебирать
    # окрестности в зависимости от ситуации

    # Окрестность 8 соседей
    neighbors16 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Окрестность 16 соседей
    neighbors = [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (2, -2), (-2, 2), (-2, -2), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1 or array[neighbor[0]-1][neighbor[1]] == 1 \
                            or array[neighbor[0]][neighbor[1]-1] == 1 or array[neighbor[0]-1][neighbor[1]-1] == 1:
                            #or array[neighbor[0]+1][neighbor[1]-1] or array[neighbor[0]+1][neighbor[1]+1] \
                            #or array[neighbor[0]-1][neighbor[1]+1]:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return False


route = astar(grid, start, goal)
route = route + [start]
route = route[::-1]
print(route)


##############################################################################
# plot the path
##############################################################################

# extract x and y coordinates from route list
x_coords = []
y_coords = []
for i in (range(0, len(route))):
    x = route[i][0]
    y = route[i][1]
    x_coords.append(x)
    y_coords.append(y)
# plot map and path
fig, ax = plt.subplots(figsize=(20, 20))
ax.imshow(grid, cmap=plt.cm.tab20c)
ax.scatter(start[1], start[0], marker="*", color="blue", s=200)
ax.scatter(goal[1], goal[0], marker="*", color="red", s=200)
ax.plot(y_coords, x_coords, color="black")
plt.show()
