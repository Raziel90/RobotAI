import random
from math import sqrt, pi

from robot import robot


class ParticleFilterTheta:

    def __init__(self, robot_pos, step_size, heading, N=500, distance_noise=0.0, measurement_noise=0.0,
                 turning_noise=0.0):

        self.particles = []
        self.__num_particles = 500
        self.weights = [1.] * N
        self.turning_noise = turning_noise
        self.distance_noise = distance_noise
        self.measurement_noise = measurement_noise

        for i in range(N):
            x = robot_pos[0]  # initial x position
            y = robot_pos[1]  # initial y position
            orientation = random.random() * 2 * pi  # initial orientation
            turning = random.random() * 2 * pi - pi
            step = step_size
            r = robot(x, y, orientation, turning=turning, distance=step)
            r.set_noise(turning_noise, distance_noise, measurement_noise)
            self.particles += [r]

    def move(self, turning=None, distance=None):

        # if the parameters are scalar, make them vector for every particle
        if type(turning) is not list and turning is not None:
            turning = [turning] * self.__num_particles

        if type(distance) is not list and distance is not None:
            distance = [distance] * self.__num_particles

        for i in range(self.__num_particles):
            # if none use the values assigned to the particle
            if turning is None:
                turn = self.particles[i].turning
            else:
                turn = turning[i]
            if distance is None:
                dist = self.particles[i].distance
            else:
                dist = distance[i]

            self.particles[i].move(turn, dist)

    def compute_weights(self, position):

        for i in range(self.__num_particles):
            predicted_measurement = self.particles[i].sense()
            error_distance = sqrt(
                (position[0] - predicted_measurement[0]) ** 2 + (position[1] - predicted_measurement[1]) ** 2)
            error = 1.0

            error *= error_distance  # (exp(- (error_distance ** 2) / (self.distance_noise ** 2) / 2.0) / sqrt(2.0 * pi * (self.distance_noise ** 2)))
            self.weights[i] *= error

    def resampling(self):
        new_particles = []
        index = int(random.random() * self.__num_particles)
        beta = 0.0
        mw = max(self.weights)
        for i in range(self.__num_particles):
            beta += random.random() * 2.0 * mw
            while beta > self.weights[index]:
                beta -= self.weights[index]
                index = (index + 1) % self.__num_particles
            new_particles.append(self.particles[index])
        self.particles = new_particles

    def set_position(self, position, orientation):

        for i in range(self.__num_particles):
            self.particles[i].x = position[0]
            self.particles[i].y = position[1]
            self.particles[i].heading = orientation

    def get_position(self):
        x = 0.0
        y = 0.0
        orientation = 0.0
        for i in range(self.__num_particles):
            x += self.particles[i].x
            y += self.particles[i].y
            # orientation is tricky because it is cyclic. By normalizing
            # around the first particle we are somewhat more robust to
            # the 0=2pi problem
            orientation += (((self.particles[i].heading - self.particles[0].heading + pi) % (2.0 * pi))
                            + self.particles[0].heading - pi)
        return [x / self.__num_particles, y / self.__num_particles, orientation / self.__num_particles]

    def update(self, measurement):
        self.compute_weights(position=measurement)
        self.resampling()

    def run(self, new_groundtruth, turning=None, distance=None):

        self.move(turning=turning, distance=distance)
        self.compute_weights(position=new_groundtruth)
        self.resampling()
        return self.get_position()
