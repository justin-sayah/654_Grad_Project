"""
Module defining the Ornstein-Uhlenbeck (OU) process.

The OU process generates random noise which aids in exploration by the Actor.
The noise is sampled from a correlated normal distribution. For more information,
see: https://www.wikipedia.org/wiki/Ornstein-Uhlenbeck_process.
"""
import numpy as np


class OUNoise:
    """
    Ornstein-Uhlenbeck (OU) process.
    """

    def __init__(self, mean, std_deviation, theta=0.15, dt=1e-2, x_initial=None):
        """
        Initialize OU process.

        Args:
            mean: mu parameter
            std_deviation: sigma parameter
            theta: theta parameter
            dt: dt term
            x_initial: initial x_t term
        """
        self.theta = theta
        self.mean = mean
        self.std_dev = std_deviation
        self.dt = dt
        self.x_initial = x_initial
        self.x_prev = self.x_initial
        self.reset()

    def __call__(self):
        """
        Runs one iteration of the OU process.

        Returns:
            The value of the OU process.
        """
        x = self.x_prev + \
            self.theta * (self.mean - self.x_prev) * self.dt + \
            self.std_dev * np.sqrt(self.dt) * \
            np.random.normal(size=self.mean.shape)
        self.x_prev = x
        return x

    def reset(self):
        """
        Resets the x_t term for the OU process.
        """
        if self.x_initial is not None:
            self.x_prev = self.x_initial
        else:
            self.x_prev = np.zeros_like(self.mean)
