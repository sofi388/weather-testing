import matplotlib.pyplot as plt
from matplotlib import colors
import csv


def read_csv(filename):
    with open(filename, newline='') as f_input:
        return [list(map(float, row)) for row in csv.reader(f_input)]


data = read_csv('wind.csv')

#############################################################################
# Color palette for different wind strength (based on windy.com)
#############################################################################
cmap = colors.ListedColormap(
    ['#6271b7', '#39619f', '#4a94a9', '#4d8d7b', '#53a553', '#359f35', '#a79d51', '#9f7f3a', '#b83c17', '#813a4e',
     '#af5088', '#754a93', '#6d61a3'])
bounds = [1.0, 3.0, 5.0, 7.0, 9.0, 11.0, 13.0, 15.0, 17.0, 19.0, 21.0, 23.0, 25.0, 27.0]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(data, cmap=cmap, norm=norm)
plt.show()
data = read_csv('wind.csv')
