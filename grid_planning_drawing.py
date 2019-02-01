# ----------
# User Instructions:
#
# Define a function, search() that returns a list
# in the form of [optimal path length, row, col]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space


grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]


init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']

def search(grid, init, goal, cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------


    m = len(grid)
    n = len(grid[0])
    path = []
    visited = dict()
    path_cost = 0
    node_queue = [init]
    while len(node_queue) > 0:
        node = node_queue.pop()
        if node == goal:
            path.append(node)
            break
        for action in delta:
            newpos = [node[0] + action[0], node[1] + action[1]]
            if (newpos[0] >= 0 and newpos[0] < m and newpos[1] >= 0 and newpos[1] < n) \
                    and grid[newpos[0]][newpos[1]] == 0 \
                    and sum([1 if newpos == nn else 0 for nn in path])==0:
                node_queue.append(newpos)
        path.append(node)
        path_cost += cost
    #print(path_cost)
    return path


def path_to_drawing(grid,path):
    decisions = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    for i in range(len(path[:-1])):
        c_x, c_y = path[i]
        n_x, n_y = path[i + 1]
        cact = [n_x - c_x, n_y - c_y]
        for action, name in zip(delta, delta_name):
            if cact == action:
                decisions[c_x][c_y] = name
                break
    decisions[path[-1][0]][path[-1][1]] = '*'
    return decisions


path = search(grid, init, goal, cost)
drawing = path_to_drawing(grid, path)
[print(i) for i in drawing]