import csv

import matplotlib.pyplot as plt
from matplotlib import colors


def read_csv(filename):
    with open(filename, newline='') as f_input:
        return [list(map(float, row)) for row in csv.reader(f_input)]


#############################################################################
# Any grid view in color (based on windy.com)
#############################################################################

def color_view(file):
    data = read_csv(file)
    cmap = colors.ListedColormap(
        ['#6271b7', '#5069AB', '#39619f', '#427DA4', '#4a94a9', '#4C9094', '#4d8d7b', '#509969', '#53a553', '#46A246',
         '#359f35', '#7C9E44', '#a79d51', '#A38E46', '#9f7f3a', '#AC632C', '#b83c17', '#813a4e',
         '#af5088', '#754a93', '#6d61a3', '#6a513c'])
    bounds = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 19.0, 21.0,
              23.0, 25.0, 27.0, 9998.0]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(data, cmap=cmap, norm=norm)
    plt.show()


color_view('wind_strength.csv')
