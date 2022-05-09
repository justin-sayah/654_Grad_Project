"""
Module containing Amazing Ball System RL environment.

Actions:
Two real values from 0 to 1. The first number is the x-motor
duty percentage. The second number is the y-motor duty percentage.

Observations:
Two real values. The first number is the x-position of the ball.
The second number is the y-position of the ball.
"""
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import gym
    from gym import spaces

import math
import csv
import random
from time import sleep
from pathlib import Path
import serial
import numpy as np

SERIAL_X_DIM = 0
SERIAL_Y_DIM = 1

class AmazingBallSystemEnv(gym.Env):
    """
    Amazing Ball System RL environment.
    """

    def __init__(self, port, calibrate=True, duration=100):
        """
        Initialize Amazing Ball System environment.

        Args:
            port: USB port connected to Amazing Ball System.
            calibrate: If `True`, run board calibration and save results to `calibration.csv`,
                       if `False`, load saved calibration in `calibration.csv` (default=`False`).
            duration: The number if steps in an episode (default=`100`).
        """
        super(AmazingBallSystemEnv, self).__init__()

        self.action_space = spaces.Box(low=0, high=1, shape=(2,), dtype=np.float16)

        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0

        self.serial = serial.Serial(port=port)
        self.calibration_file_path = Path(__file__).parent.resolve() / 'calibration.csv'
        if calibrate:
            self._calibration()
        else:
            self._load_calibration()

        self.observation_space = spaces.Box(low=np.array([self.x_min, self.y_min]),
                                            high=np.array([self.x_max, self.y_max]),
                                            dtype=np.float16)

        self.duration = duration
        self.steps = 0
        self.done = False
        self.goal = [(self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2]

        self.distance_max = math.dist([self.x_min, self.y_min], self.goal)
        self.distance_max = max(self.distance_max, math.dist([self.x_min, self.y_max], self.goal))
        self.distance_max = max(self.distance_max, math.dist([self.x_max, self.y_max], self.goal))
        self.distance_max = max(self.distance_max, math.dist([self.x_max, self.y_min], self.goal))

        print(f'ABS calibrated: x:[{self.x_min},  {self.x_max}], y:[{self.y_min}, {self.y_max}]')

    def _calibration(self):
        """
        Calibrate the Amazing Ball System board ranges.

        The more conservative values for the x and y range will be used.

        For example if the min x is found to be 100 and 110 at two locations,
        the value of 110 is used.
        """
        x_min, y_min = self._calibrate_corner(x_duty=0, y_duty=0)
        self.x_min = x_min
        self.y_min = y_min

        x_max, y_min = self._calibrate_corner(x_duty=1, y_duty=0)
        self.x_max = x_max
        if y_min > self.y_min:
            self.y_min = y_min

        x_max, y_max = self._calibrate_corner(x_duty=1, y_duty=1)
        if x_max < self.x_max:
            self.x_max = x_max
        self.y_max = y_max

        min_x, max_y = self._calibrate_corner(x_duty=0, y_duty=1)
        if min_x > self.x_min:
            self.x_min = min_x
        if max_y < self.y_max:
            self.y_max = max_y

        self._save_calibration()

    def _calibrate_corner(self, x_duty, y_duty):
        """
        Move ball to a desired corner of the Amazing Ball System for calibration.

        Args:
            x_duty: The duty percentage of the x motor (for corners, 0 or 1).
            y_duty: The duty percentage of the y motor (for corners, 0 or 1).

        Returns:
            The ball's position in the desired corner.
        """
        self._uart_comm(SERIAL_X_DIM, x_duty)
        self._uart_comm(SERIAL_Y_DIM, y_duty)

        # wait for ball to move to the corner
        sleep(3)

        # send the same command to sample the ball's position
        ball_position_x = self._uart_comm(SERIAL_X_DIM, x_duty)
        ball_position_y = self._uart_comm(SERIAL_Y_DIM, y_duty)
        return ball_position_x, ball_position_y

    def _save_calibration(self):
        """
        Save a board calibration saved in `calibration.csv`.
        """
        header = ['x-min', 'x-max', 'y-min', 'y-max']
        data = [self.x_min, self.x_max, self.y_min, self.y_max]
        with open(self.calibration_file_path, 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerow(data)

    def _load_calibration(self):
        """
        Load a board calibration saved in `calibration.csv`.
        """
        with open(self.calibration_file_path, 'r', encoding='UTF8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.x_min = int(row['x-min'])
                self.x_max = int(row['x-max'])
                self.y_min = int(row['y-min'])
                self.y_max = int(row['y-max'])
                break

    def _random_position(self):
        """Generate a random position on the board.

        Returns:
            A random position on the board.
        """
        return [random.randint(self.x_min, self.x_max),
                random.randint(self.y_min, self.y_max)]

    def _reward(self, ball_position):
        distance = math.dist(ball_position, self.goal)
        distance_normalized = distance / self.distance_max
        reward = - distance_normalized
        return reward

    def _uart_comm(self, dimension, duty_percent):
        """
        Send command to Amazing Ball System Motor over UART.

        Args:
            dimension: The motor dimension (SERIAL_X_DIM, or SERIAL_X_DIM).
            duty_percent: The motor duty cycle as a percentage.

        Returns:
            The position of the ball in the `dimension` dimension.
        """
        # give touchscreen time to switch sample direction
        sleep(0.01)

        duty = (int)(900 + (duty_percent * 1200))
        duty_low_bits, duty_high_bits = (duty & 0xFFFFFFFF).to_bytes(2, 'big')
        message = [0, dimension, duty_low_bits, duty_high_bits]
        message_bytes = bytearray(message)
        self.serial.write(message_bytes)

        response_low_bytes = self.serial.read()
        response_high_bytes = self.serial.read()
        response_bytes = response_low_bytes + response_high_bytes
        response = int.from_bytes(response_bytes, 'big')

        return np.uint16(response)

    def reset(self, seed=None):
        """
        Start a new RL sequence.

            Returns:
                The initial TimeStep of the environment.
        """
        super().reset(seed=seed)

        self.done = False

        # The default location of the ball on the board is (mid x, mid y)
        # self._uart_comm(SERIAL_X_DIM, 0.5)
        # self._uart_comm(SERIAL_Y_DIM, 0.5)

        # Wait for ball to reach default location
        # sleep(1.5)

        self.steps = 0

        return self.step(np.zeros(self.action_space.shape))

    def step(self, action):
        """
        Update the environment according to an action.

        Args:
            action: The action to take corresponding to `action_spec()`.

        Returns:
            The next TimeStep of the environment.
        """
        self.steps += 1
        if self.steps == self.duration:
            self.done = True

        motor_x_command = action[0]
        motor_y_command = action[1]

        ball_position_x = self._uart_comm(SERIAL_X_DIM, motor_x_command)
        ball_position_y = self._uart_comm(SERIAL_Y_DIM, motor_y_command)
        state = np.array([ball_position_x, ball_position_y])

        # keep ball position in range of board
        ball_position_x = max(min(self.x_max, ball_position_x), self.x_min)
        ball_position_y = max(min(self.y_max, ball_position_y), self.y_min)

        reward = self._reward([ball_position_x, ball_position_y])

        return state, reward, self.done, []
