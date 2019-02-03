# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']  # Use these when creating your policy grid.


# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid, goal, cost_step, collision_cost, success_prob):
    isvalid = lambda x, y: 0 <= x < len(grid) and 0 <= y < len(grid[0])  # and grid[x][y] == 0
    failure_prob = (1.0 - success_prob) / 2.0  # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    err_prob = [success_prob, (1 - success_prob) / 2]

    done = False
    while not done:
        done = True
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if [x, y] == goal:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'
                        done = False

                elif grid[x][y] == 0:

                    for dir, move in enumerate(delta):
                        c2 = 0
                        for err in [-1, 1, 0]:
                            x2, y2 = (x + delta[(dir + err) % 4][0], y + delta[(dir + err) % 4][1])
                            if isvalid(x2, y2):
                                c2 += (value[x2][y2] + cost_step) * err_prob[int(abs(err))]
                            else:
                                c2 += (collision_cost + cost_step) * err_prob[int(abs(err))]
                        # here x2 and y2 have err == 0
                        if value[x][y] > c2:
                            value[x][y] = c2
                            policy[x][y] = delta_name[dir]
                            done = False




    return value, policy


# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0]) - 1]  # Goal is in top right corner
cost_step = 1
collision_cost = 1000
success_prob = 0.5

value, policy = stochastic_value(grid, goal, cost_step, collision_cost, success_prob)
for row in value:
    print(row)

for row in policy:
    print(row)


# Expected outputs:
#
# [471.9397246855924, 274.85364957758316, 161.5599867065471, 0],
# [334.05159958720344, 230.9574434590965, 183.69314862430264, 176.69517762501977],
# [398.3517867450282, 277.5898270101976, 246.09263437756917, 335.3944132514738],
# [700.1758933725141, 1000, 1000, 668.697206625737]


#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']
