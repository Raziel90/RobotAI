# ----------
# Part Four
#
# Again, you'll track down and recover the runaway Traxbot.
# But this time, your speed will be about the same as the runaway bot.
# This may require more careful planning than you used last time.
#
# ----------
# YOUR JOB
#
# Complete the next_move function, similar to how you did last time.
#
# ----------
# GRADING
#
# Same as part 3. Again, try to catch the target in as few steps as possible.

from math import *

from matrix import *
from robot import *


def next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER=None):
    # This function will be called after each time the target moves.
    if not OTHER:  # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings)  # now I can keep track of history
    else:  # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER  # now I can always refer to these variables

    if len(measurements) < 3:
        heading_to_target = get_heading(hunter_position, target_measurement)
        heading_difference = heading_to_target - hunter_heading
        turning = heading_difference  # turn towards the target
        distance = distance_between(hunter_position, target_measurement)  # full speed ahead!
    else:
        step_tgt = [distance_between(measurements[-1], measurements[-2])]
        turning_tgt = []
        for i in range(1, len(measurements) - 1):
            step_tgt += [distance_between(measurements[i - 1], measurements[i])]
            turning_tgt += [
                get_heading(measurements[i + 1], measurements[i]) - get_heading(measurements[i], measurements[i - 1])]
        step_tgt = sum(step_tgt) / len(step_tgt)
        turning_tgt = sum(turning_tgt) / len(turning_tgt)
        heading = get_heading(measurements[-2], measurements[-1]) % (2 * pi)
        tgt_robot = robot(target_measurement[0], target_measurement[1], heading)
        tgt_robot.move(distance=step_tgt, turning=turning_tgt)
        predicted_steps = 1
        tgt_goal = tgt_robot.sense()
        while predicted_steps * max_distance < distance_between(tgt_goal, hunter_position) and predicted_steps < 20:
            tgt_robot.move(distance=step_tgt, turning=turning_tgt)
            tgt_goal = tgt_robot.sense()
            predicted_steps += 1
        # tgt_robot.move(distance=step_tgt, turning=turning_tgt)

        distance = distance_between(hunter_position, tgt_goal)
        heading_to_target = get_heading(hunter_position, tgt_goal)
        turning = heading_to_target - hunter_heading
        distance = min(max_distance, distance)
        # draw_chase(hunter_position, hunter_heading, distance, turning, target_measurement, heading, step_tgt,
        #            turning_tgt, tgt_goal)

    # The OTHER variable is a place for you to store any historical information about
    # the progress of the hunt (or maybe some localization information). Your return format
    # must be as follows in order to be graded properly.

    return turning, distance, OTHER


def draw_chase(hunter_position, hunter_heading, hunter_step, hunter_turning, target_measurement, target_heading,
               target_step, target_turning, target_future):
    import matplotlib.pyplot as plt
    dist = distance_between(hunter_position, target_measurement)
    plt.figure(0)
    plt.text(-14, 29, 'step=' + str(round(hunter_step, 2)) + ', turning=' + str(round(hunter_turning, 2)))
    plt.text(2., 29, 'target: step=' + str(round(target_step, 2)) + ', turning=' + str(round(target_turning, 2)))
    plt.text(-5, 27, 'distance: ' + str(round(dist, 3)))
    plt.scatter(hunter_position[0], hunter_position[1])
    plt.scatter(target_measurement[0], target_measurement[1], marker='^')
    plt.text(target_measurement[0], target_measurement[1],
             (round(target_measurement[0], 2), round(target_measurement[1], 2)))
    plt.scatter(target_future[0], target_future[1], marker='*')
    plt.text(target_future[0], target_future[1], (round(target_future[0], 2), round(target_future[1], 2)))
    plt.text(hunter_position[0], hunter_position[1], (round(hunter_position[0], 2), round(hunter_position[1], 2)))
    plt.arrow(hunter_position[0], hunter_position[1], hunter_step * cos(hunter_turning + hunter_heading),
              hunter_step * sin(hunter_turning + hunter_heading), head_width=0.15)
    plt.arrow(target_measurement[0], target_measurement[1], target_step * cos(target_turning + target_heading),
              target_step * sin(target_turning + target_heading), head_width=0.15)
    plt.xlim([-15, 15])
    plt.ylim([0, 30])
    plt.show()


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def demo_grading(hunter_bot, target_bot, next_move_fcn, OTHER=None):
    """Returns True if your next_move_fcn successfully guides the hunter_bot
    to the target_bot. This function is here to help you understand how we
    will grade your submission."""
    max_distance = 0.98 * target_bot.distance  # 0.98 is an example. It will change.
    separation_tolerance = 0.02 * target_bot.distance  # hunter must be within 0.02 step size to catch target
    caught = False
    ctr = 0

    # We will use your next_move_fcn until we catch the target or time expires.
    while not caught and ctr < 1000:

        # Check to see if the hunter has caught the target.
        hunter_position = (hunter_bot.x, hunter_bot.y)
        target_position = (target_bot.x, target_bot.y)
        separation = distance_between(hunter_position, target_position)
        if separation < separation_tolerance:
            print("You got it right! It took you ", ctr, " steps to catch the target.")
            caught = True

        # The target broadcasts its noisy measurement
        target_measurement = target_bot.sense()

        # This is where YOUR function will be called.
        turning, distance, OTHER = next_move_fcn(hunter_position, hunter_bot.heading, target_measurement, max_distance,
                                                 OTHER)

        # Don't try to move faster than allowed!
        if distance > max_distance:
            distance = max_distance

        # We move the hunter according to your instructions
        hunter_bot.move(turning, distance)

        # The target continues its (nearly) circular motion.
        target_bot.move_in_circle()

        ctr += 1
        if ctr >= 1000:
            print("It took too many steps to catch the target.")
    return caught


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi


def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading


def naive_next_move(hunter_position, hunter_heading, target_measurement, max_distance, OTHER):
    """This strategy always tries to steer the hunter directly towards where the target last
    said it was and then moves forwards at full speed. This strategy also keeps track of all
    the target measurements, hunter positions, and hunter headings over time, but it doesn't
    do anything with that information."""
    if not OTHER:  # first time calling this function, set up my OTHER variables.
        measurements = [target_measurement]
        hunter_positions = [hunter_position]
        hunter_headings = [hunter_heading]
        OTHER = (measurements, hunter_positions, hunter_headings)  # now I can keep track of history
    else:  # not the first time, update my history
        OTHER[0].append(target_measurement)
        OTHER[1].append(hunter_position)
        OTHER[2].append(hunter_heading)
        measurements, hunter_positions, hunter_headings = OTHER  # now I can always refer to these variables

    heading_to_target = get_heading(hunter_position, target_measurement)
    heading_difference = heading_to_target - hunter_heading
    turning = heading_difference  # turn towards the target
    distance = max_distance  # full speed ahead!
    return turning, distance, OTHER


target = robot(0.0, 10.0, 0.0, 2 * pi / 30, 1.5)
measurement_noise = .05 * target.distance
target.set_noise(0.0, 0.0, measurement_noise)

hunter = robot(-10.0, -10.0, 0.0)

print(demo_grading(hunter, target, next_move))
