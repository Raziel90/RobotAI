# ----------
# User Instructions:
#
# Create a function compute_value which returns
# a grid of values. The value of a cell is the minimum
# number of moves required to get from the cell to the goal.
#
# If a cell is a wall or it is impossible to reach the goal from a cell,
# assign that cell a value of 99.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]
grid = [[0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0]]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1  # the cost associated with moving from a cell to an adjacent one

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def compute_value(grid, goal, cost):
    # ----------------------------------------
    # insert code below
    # ----------------------------------------
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    value = [[-1 if grid[i][j] == 0 else 99 for j in range(len(grid[0]))] for i in range(len(grid))]
    expanded = [[0, -1, goal[0], goal[1]]]
    while len(expanded) > 0:
        expanded = sorted(expanded,reverse=True)
        c, a, x, y = expanded.pop()
        for idx, act in enumerate(delta):
            x2 = x + act[0]
            y2 = y + act[1]
            c2 = c + cost
            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]):
                if value[x2][y2] == -1:
                    expanded.append([c2,(idx-2)%4,x2, y2])
        value[x][y] = c
        if a == -1:
            policy[x][y] = '*'
        else:
            policy[x][y] = delta_name[a]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if value[i][j] == -1:
                value[i][j] = 99
    return value,policy

value,policy = compute_value(grid, goal, cost)
[print(v) for v in value]
[print(p) for p in policy]