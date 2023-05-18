"""Manage the tilings"""

import abc
from collections.abc import Iterator
from math import cos, pi, sin, sqrt

import numpy as np


def rot_matrix(theta):
    return np.array([[cos(theta), -sin(theta)], [sin(theta),  cos(theta)]])


class Shape(abc.ABC):

    def __init__(
        self,
        scale: float,
        padding_factor: float,
        out_width: int,
        out_height: int,
    ) -> None:
        self.scale = scale
        self.padding_factor = padding_factor
        self.out_width = out_width
        self.out_height = out_height

    def __call__(self) -> Iterator[list[tuple[float, float]]]:
        """Generate polygons of the image"""
        side_length = self.scale
        for vertices in self.generate_units():
            yield [(x * side_length, y * side_length) for x, y in vertices]

    @abc.abstractmethod
    def generate_units(self) -> Iterator[list[tuple[float, float]]]:
        """Generate unit polygons"""
        raise NotImplementedError()

class Hexagon(Shape):

    def generate_units(self) -> Iterator[list[tuple[float, float]]]:
        """Generate hexagons one unit wide"""
        units = self.scale * self.padding_factor
        y_start = 0
        y_end = self.out_height / units * 2 / sqrt(3)
        x_start = y_end / 2
        x_end = self.out_width / units
        rot_60 = rot_matrix(pi/3)
        placement_wrt_s = self.padding_factor * np.array([1, 0])
        placement_wrt_t = rot_60 @ placement_wrt_s
        for s in range(-int(x_start), 1 + int(x_end)):
            for t in range(y_start, 1 + int(y_end)):
                base_point = placement_wrt_s*s + placement_wrt_t*t
                offset = np.array([0.5, 0.5/sqrt(3)])
                yield [base_point + np.linalg.matrix_power(rot_60, i) @ offset for i in range(6)]

class Triangle(Shape):

    def generate_units(self):
        """Generate triangles of side length one unit"""
        units = self.scale * self.padding_factor
        x_end = self.out_width / units
        y_end = self.out_height / units * 2 / sqrt(3)
        rot_60 = rot_matrix(pi/3)
        rot_120 = rot_matrix(2*pi/3)
        placement_wrt_s = self.padding_factor * np.array([1, 0])
        placement_wrt_t = self.padding_factor * np.array([0, sqrt(3) / 2])
        for t in range(0, 2 + int(y_end)):
            for s in range(0, 2 + int(x_end)):
                s = s if t % 2 else s - 0.5  # horizontal offset on odd rows
                base_point = placement_wrt_s*s + placement_wrt_t*t
                offset = np.array([0.5, 0.5/sqrt(3)])
                yield [base_point + np.linalg.matrix_power(rot_120, i) @ offset for i in range(3)]

                base_point += self.padding_factor * np.array([0.5, 1/sqrt(3) - sqrt(3)/2])
                offset = rot_60 @ offset
                yield [base_point + np.linalg.matrix_power(rot_120, i) @ offset for i in range(3)]
