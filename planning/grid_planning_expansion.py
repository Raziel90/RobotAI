# -----------
# User Instructions:
#
# Modify the function search so that it returns
# a table of values called expand. This table
# will keep track of which step each node was
# expanded.
#
# Make sure that the initial cell in the grid
# you return has the value 0.
# ----------

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]


init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost):
    # ----------------------------------------
    # modify code below
    # ----------------------------------------

    delta = [[-1, 0],  # go up
             [0, -1],  # go left
             [1, 0],  # go down
             [0, 1]]  # go right
    m = len(grid[0])
    n = len(grid)
    if init[0] < 0 or init[0] >= n or init[1] < 0 or init[1] >= m:
        return 'fail'
    expand = [[-1] * m for i in range(n)]
    node_queue = [init]
    iter = 0
    path = []
    while len(node_queue) > 0:
        node = node_queue.pop(0)
        if node == goal:
            expand[node[0]][node[1]] = iter
            path.append(node)
            break
        elif expand[node[0]][node[1]] == -1:
            for action in delta[::-1]:
                newpos = [node[0] + action[0], node[1] + action[1]]

                if newpos[0] >= 0 and newpos[0] < n and newpos[1] >= 0 and newpos[1] < m:
                    if grid[newpos[0]][newpos[1]] == 0:
                        node_queue += [newpos]

            expand[node[0]][node[1]] = iter
            path.append(node)
            iter += 1

    decisions = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    for i in range(len(path[:-1])):
        c_x, c_y = path[i]
        n_x, n_y = path[i+1]
        cact = [n_x - c_x, n_y - c_y]
        for action,name in zip(delta,delta_name):
            if cact == action:
                decisions[c_x][c_y] = name
                break

    return expand

ex = search(grid, init, goal, cost)
[print(i) for i in ex]
