# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D below.
#
# You are given a car in grid with initial state
# init. Your task is to compute and return the car's 
# optimal path to the position specified in goal; 
# the costs for each motion are as defined in cost.
#
# There are four motion directions: up, left, down, and right.
# Increasing the index in this array corresponds to making a
# a left turn, and decreasing the index corresponds to making a 
# right turn.

forward = [[-1, 0],  # go up
           [0, -1],  # go left
           [1, 0],  # go down
           [0, 1]]  # go right
forward_name = ['up', 'left', 'down', 'right']

# action has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

# EXAMPLE INPUTS:
# grid format:
#     0 = navigable space
#     1 = unnavigable space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]

init = [4, 3, 0]  # given in the form [row,col,direction]
# direction = 0: up
#             1: left
#             2: down
#             3: right

goal = [2, 0]  # given in the form [row,col]

cost = [2, 1, 20]  # cost has 3 values, corresponding to making


# a right turn, no turn, and a left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D with the given parameters should return 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
# ----------
cost = [1, 1, 14]
goal = [0, 1]
# goal = [2, 1]
# goal = [0, 3]

init = [4, 2, 0]

grid = [[0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1]]


# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D(grid, init, goal, cost):
    isvalid = lambda x, y: 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0
    value = [[[999 for k in range(len(forward))] for i in range(len(grid[0]))] for j in range(len(grid))]
    policy = [[[" " for k in range(len(forward))] for i in range(len(grid[0]))] for j in range(len(grid))]
    policy2D = [[" " for i in range(len(grid[0]))] for j in range(len(grid))]

    expanded = [[0, -1, goal[0], goal[1],i] for i in range(len(forward))]
    done = False
    while done is False:
        done = True
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for t in range(len(forward)):
                    if [x, y] == goal:
                        if value[x][y][t] > 0:
                            done = False
                            value[x][y][t] = 0
                            policy[x][y][t] = '*'
                    elif grid[x][y] == 0:
                        for act in action:
                            o = (t + act)%4
                            x2 = x + forward[o][0]
                            y2 = y + forward[o][1]
                            if isvalid(x2, y2):
                                c2 = value[x2][y2][o] + cost[act + 1]
                                if c2 < value[x][y][t]:
                                    done = False
                                    value[x][y][t] = c2
                                    policy[x][y][t] = action_name[act + 1]

    x, y, t = init
    policy2D[x][y] = policy[x][y][t]
    while [x, y] != goal:
        # print(x, y, t)
        if policy[x][y][t] == '#':
            o = t
            # print('#')
        elif policy[x][y][t] == 'L':
            o = (t + 1) % 4
            # print('L')
        elif policy[x][y][t] == 'R':
            o = (t - 1) % 4
            # print('R')
        # print(x, y, t, (o - t)%4)
        x = x + forward[o][0]
        y = y + forward[o][1]
        t = o
        policy2D[x][y] = policy[x][y][t]

    return policy2D



pol= optimum_policy2D(grid, init, goal, cost)
print([str(i) if i >=0 else " " for i in range(-1,len(pol[0]))])
[print([j]+p) for j,p in enumerate(pol)]