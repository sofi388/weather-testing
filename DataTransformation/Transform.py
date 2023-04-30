import csv

##############################################################################
# transform smth
##############################################################################


# with open("grid31x10.csv") as csvfile:
#   reader = csv.reader(csvfile, quoting=csv.QUOTE_NON-NUMERIC) # change contents to floats
# for row in reader: # each row is a list
#     results.append(row)

#  grid = np.array(row)

#results = []
#mydata = pd.read_csv("depth.csv")


def read_csv(filename):
    with open(filename, newline='') as f_input:
        return [list(map(float, row)) for row in csv.reader(f_input)]


def make_grid(filename, depth):
    global l_replace2
    arrayDepth = read_csv(filename)
    mas = []
    for row1 in arrayDepth:
        l_replace2 = [1 if (i == 9999.0) else 0 for i in row1]
        mas.append(l_replace2)
    return mas


# print(l_replace2)

res = make_grid('../AStar/depth.csv', 2)
print(res)

