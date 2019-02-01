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



delta_name = ['^', '<', 'v', '>']

def search(grid, init, goal, cost):
    # ----------------------------------------
    # insert code here
    # ----------------------------------------
    delta = [[-1, 0],  # go up
             [0, -1],  # go left
             [1, 0],  # go down
             [0, 1]]  # go right

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
    if path[-1] == goal:
        return path
    else:
        return 'fail'


path = search(grid, init, goal, cost)
print(path)