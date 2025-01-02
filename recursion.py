# create elevation grid
elevation     = ((3.8, 1.5, 2.2, 4.4, 1.6, 4.5, 3.7, 4.3, 6.0, 5.3),
                 (6.9, 5.8, 3.5, 2.0, 3.2, 5.7, 5.0, 5.2, 5.4, 7.0),
                 (7.8, 8.9, 7.7, 5.3, 4.9, 4.3, 3.2, 4.3, 4.1, 5.8),
                 (6.0, 6.7, 5.7, 4.9, 5.8, 3.5, 2.3, 2.3, 3.8, 5.4),
                 (2.9, 3.1, 4.6, 3.5, 4.5, 3.4, 1.5, 1.7, 2.8, 3.5),
                 (4.3, 2.8, 2.7, 5.0, 3.6, 2.2, 2.4, 4.0, 4.2, 6.0),
                 (3.4, 4.6, 3.7, 6.0, 3.3, 4.5, 3.1, 2.7, 3.6, 3.0),
                 (1.1, 2.5, 4.5, 3.4, 4.2, 2.3, 3.2, 1.7, 2.2, 1.0),
                 (0.6, 1.1, 2.7, 2.7, 1.1, 3.8, 2.5, 1.3, 0.9, 1.7),
                 (1.5, 1.6, 0.0, 1.9, 2.7, 4.4, 3.7, 2.1, 1.0, 0.6))

# create precipitation grid
precipitation = ((0.2, 1.9, 1.9, 2.0, 1.6, 0.0, 0.3, 0.7, 0.2, 1.4),
                 (1.5, 0.2, 1.4, 0.5, 0.0, 1.6, 1.6, 1.2, 1.7, 1.4),
                 (0.3, 0.7, 0.7, 1.6, 1.6, 0.3, 0.2, 0.0, 1.8, 0.6),
                 (1.2, 1.5, 0.7, 0.9, 1.1, 1.9, 0.1, 1.8, 0.9, 0.8),
                 (0.2, 1.1, 0.1, 0.1, 0.0, 1.6, 1.5, 1.2, 0.2, 0.5),
                 (1.7, 0.5, 0.1, 1.5, 0.1, 0.5, 0.2, 0.4, 0.4, 1.1),
                 (1.5, 1.9, 1.3, 0.3, 1.9, 1.9, 1.2, 1.9, 0.5, 0.8),
                 (1.6, 1.2, 2.0, 1.1, 1.1, 1.8, 1.8, 1.2, 0.9, 0.2),
                 (0.2, 1.9, 1.9, 2.0, 1.6, 0.0, 0.3, 0.7, 0.2, 1.4),
                 (1.3, 0.6, 0.1, 1.8, 1.3, 0.8, 0.9, 0.7, 0.3, 1.3))

'''
Create a function that uses recursion to create a flow accumulation map.

A flow accumulation map is a two dimensional matrix of floats derived from a precipitation map and an
elevation map. For any cell in the matrix, the amount of water flowing through it equals the
precipitation at its location plus the precipitation of all upstream cells. One cell is upstream of a
second cell if the first cell is a neighboring cell that is lower in elevation than both the second
cell and all of its other neighboring cells. To calculate flow accumulation at any particular
location, sum the precipitation values at that location and at all upstream locations.

Once you have created the recursive flow accumulation function, use it on the elevation and
precipitation maps provided above. Then, print its output, which should be a matrix with dimensions
equal to those of the input matrices, each cell of which corresponds to the same cell in the input
matrices.

For additional points, you may also create a matrix that records which basin each cell is in and a
table recording the location of each basin's sink and the sink's flow accumulation value. A basin is a
group of cells that are all recursively upstream of the same cell, which is its sink. The sink's flow
accumulation value should equal the sum of the precipitation at all cells in the basin. You may name
the basins by simply numbering them.
'''

# record dimensions of grids
width  = len(elevation)
height = len(elevation[0])

# define directions
#   - y +
# - 6 7 8
# x 5 0 1
# + 4 3 2
directions = (( 0, 0),
              ( 0, 1),
              ( 1, 1),
              ( 1, 0),
              ( 1,-1),
              ( 0,-1),
              (-1,-1),
              (-1, 0),
              (-1, 1))

# define function to list adjacent cells
def adjacent(x, y):
    if x == 0:
        if y == 0:
            directions = (1, 2, 3)
        elif y == height - 1:
            directions = (3, 4, 5)
        else:
            directions = (1, 2, 3, 4, 5)
    elif x == width - 1:
        if y == 0:
            directions = (7, 8, 1)
        elif y == height - 1:
            directions = (5, 6, 7)
        else:
            directions = (5, 6, 7, 8, 1)
    else:
        if y == 0:
            directions = (7, 8, 1, 2, 3)
        elif y == height - 1:
            directions = (3, 4, 5, 6, 7)
        else:
            directions = (1, 2, 3, 4, 5, 6, 7, 8)
    return directions

# define function to determine flow direction of each cell
def direct(x, y):
    neighborhood = adjacent(x, y)
    least_neighbor_height = elevation[x][y]
    least_neighbor = 0
    for direction in range(len(directions)):
        if direction in neighborhood:
            neighbor_elevation = elevation[x + directions[direction][0]][y + directions[direction][1]]
            if neighbor_elevation < least_neighbor_height:
                least_neighbor_height = neighbor_elevation
                least_neighbor = direction
    return least_neighbor

# create grid of flow directions
flow = []
for x in range(width):
    flow += [[]]
    for y in range(height):
        flow[x] += [direct(x, y)]

# create accumulation grid
accumulation = []
for x in range(width):
    accumulation += [[]]
    for y in range(height):
        accumulation[x] += [0]

# create grid that records whether runoff in any cell has already been accumulated
coverage = []
for x in range(width):
    coverage += [[]]
    for y in range(height):
        coverage[x] += [0]

# define function to recursively accumulate precipitation from upstream cells
def accumulate(x, y):
    accumulation[x][y] += precipitation[x][y]
    neighborhood = adjacent(x, y)
    for direction in range(len(directions)):
        if direction in neighborhood:
            to_neighbor = directions[direction]
            neighbor_flow = flow[x + to_neighbor[0]][y + to_neighbor[1]]
            if direction > 4:
                inverse_direction = range(len(directions))[direction - 4]
            else:
                inverse_direction = range(len(directions))[direction + 4]
            if neighbor_flow == inverse_direction:
                    accumulation[x][y] += accumulate(x + to_neighbor[0], y + to_neighbor[1])
    coverage[x][y] = basin
    accumulation[x][y] = round(accumulation[x][y], 2)
    return accumulation[x][y]

# sort cells by depth
cells = []
for x in range(width):
    for y in range(height):
        cells += [[elevation[x][y], (x, y)]]
def sort_key(cell):
    return cell[0]
cells.sort(key = sort_key)

# accumulate precipitation
basins = []
basin = 1
for cell in cells:
    x = cell[1][0]
    y = cell[1][1]
    if coverage[x][y] == 0:
        accumulate(x, y)
        outflow = accumulation[x][y]
        basins += [[basin, outflow, (x, y)]]
        basin += 1

# print products
print('width:', width)
print('height:', height)
print()
print('elevation:')
for x in range(width):
    print(elevation[x])
print()
print('flow direction codes:')
print('  - y +')
print('- 6 7 8')
print('x 5 0 1')
print('+ 4 3 2')
print()
print('flow directions:')
for x in range(width):
    print(flow[x])
print()
print('precipitation:')
for x in range(width):
    print(precipitation[x])
print()
print('accumulation:')
for x in range(width):
    print(accumulation[x])
print()
print('basins:')
for x in range(width):
    print(coverage[x])
print()
print('basin outflows and sink locations:')
for x in basins:
    print(x)
