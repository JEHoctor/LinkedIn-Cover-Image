# third party libraries
import numpy as np
from sklearn import gaussian_process as gp


def random_pattern(sample_points):
    return np.random.rand(len(sample_points))


def gaussian_process_pattern(sample_points, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState()
    kernel = 1.0 * gp.kernels.Matern(length_scale=20.0, length_scale_bounds="fixed")
    gpr = gp.GaussianProcessRegressor(kernel=kernel)
    samples = gpr.sample_y(sample_points, random_state=random_state).flatten()
    samples_min, samples_max = samples.min(), samples.max()
    scaled = (samples - samples_min) / (samples_max - samples_min)
    return scaled
