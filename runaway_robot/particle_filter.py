import random
from math import *

from robot import robot


class ParticleFilterTheta:

    def __init__(self, robot_pos, heading, N=500, distance_noise=0.0, measurement_noise=0.0,
                 turning_noise=0.0):

        self.particles = []
        self.__num_particles = N
        self.weights = [1. / N] * N
        self.turning_noise = turning_noise
        self.distance_noise = distance_noise
        self.measurement_noise = measurement_noise

        for i in range(N):
            x = random.gauss(robot_pos[0], measurement_noise)  # initial x position
            y = random.gauss(robot_pos[1], measurement_noise)  # initial y position

            orientation = random.gauss(heading, measurement_noise)  # /(1+(x/y)**2))
            turning = random.random() * 2 * pi - pi  # initial orientation
            step = random.random() * 5  # random.gauss(step_size, measurement_noise)
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

            self.particles[i].move(
                random.gauss(turn, self.turning_noise),
                random.gauss(dist, self.distance_noise))

    def compute_weights(self, position):

        for i in range(self.__num_particles):
            predicted_measurement = self.particles[i].sense()
            error_distance = sqrt(
                (position[0] - predicted_measurement[0]) ** 2 + (position[1] - predicted_measurement[1]) ** 2)

            uncert = lambda err, sigma: (exp(- (err ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2)))
            self.weights[i] *= max(uncert(error_distance, 0.1), 1e-10)
        s = sum(self.weights)
        self.weights = [w / s for w in self.weights]


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
            x = self.particles[index].x
            y = self.particles[index].y
            heading = self.particles[index].heading
            turning = self.particles[index].turning
            distance = self.particles[index].distance
            self.weights[i] = self.weights[index]
            new_particles.append(robot(x, y, heading, turning, distance))
        self.particles = new_particles
        # self.weights = [1.] * self.__num_particles

    def Gaussian(self, mu, sigma, x):
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def set_position(self, position, orientation):

        for i in range(self.__num_particles):
            self.particles[i].x = random.gauss(position[0], self.measurement_noise)
            self.particles[i].y = random.gauss(position[1], self.measurement_noise)
            self.particles[i].heading = random.gauss(orientation, self.measurement_noise)

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

    def get_turning_distance(self):
        theta = 0.0
        r = 0.0
        orientation = 0.0
        for i in range(self.__num_particles):
            r += self.particles[i].distance
            # orientation is tricky because it is cyclic. By normalizing
            # around the first particle we are somewhat more robust to
            # the 0=2pi problem
            orientation += (((self.particles[i].turning - self.particles[0].turning + pi) % (2.0 * pi))
                            + self.particles[0].turning - pi)
        return [r / self.__num_particles, orientation / self.__num_particles]

    def update(self, measurement):
        self.compute_weights(position=measurement)
        self.resampling()

    def run(self, new_groundtruth, turning=None, distance=None):

        self.move(turning=turning, distance=distance)
        self.compute_weights(position=new_groundtruth)
        self.resampling()
        return self.get_position()
