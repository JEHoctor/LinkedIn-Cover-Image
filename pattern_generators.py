from math import sin, cos, pi, sqrt

import numpy as np


def random_pattern(s, t):
    return np.random.rand()


class PerlinNoise:
    def __init__(self, sampling_scale=0.3):
        rot_60 = np.array([[cos(pi/3), -sin(pi/3)],
                           [sin(pi/3),  cos(pi/3)]])

        self.sample_placement_wrt_s = sampling_scale*np.array([1.0, 0.0])
        self.sample_placement_wrt_t = rot_60 @ self.sample_placement_wrt_s

        self.gradients = {}

    def _closest_gradients(self, point):

    def _sample(self, point):

    def __call__(self, s, t):
        sampling_point = self.sample_placement_wrt_s*s + self.sample_placement_wrt_t*t
        return self._sample(sampling_point)


class CA:
    def __init__(self):
        self.run(steps=100)

    def _run(self, steps):
        raise NotImplementedError()

    def __call__(self, s, t):
        raise NotImplementedError()
