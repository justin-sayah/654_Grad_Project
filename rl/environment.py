"""Module containing Amazing Ball System RL environment
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from time import sleep
import csv
from pathlib import Path
import random
import math
import numpy as np
import serial

from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts

SERIAL_X_DIM = 0
SERIAL_Y_DIM = 1


class AmazingBallSystemEnv(py_environment.PyEnvironment):
    """Amazing Ball System RL environment
    """

    def __init__(self, port='/dev/ttyUSB0', calibrate=True, seed=None):
        """Initialize Amazing Ball System environment
        """
        self._action_spec = array_spec.BoundedArraySpec(shape=(2, ),
                                                        dtype=np.float16,
                                                        minimum=0,
                                                        maximum=1,
                                                        name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(2, ),
                                                             dtype=np.uint16,
                                                             name='observation')
        self._state = [0, 0]
        self._goal = [0, 0]

        self._board_x_range = [0, 0]
        self._board_y_range = [0, 0]

        self._serial = serial.Serial(port=port)

        self._calibration_file_path = Path(__file__).parent.resolve() / 'calibration.csv'
        if calibrate:
            self._calibration()
        else:
            self._load_calibration()

        print(f'ABS calibrated: x:{self._board_x_range} y:{self._board_y_range}')

        if seed is not None:
            random.seed(seed)

        self._reset()

    def _calibration(self):
        """
        Calibrate the Amazing Ball System board ranges.

        The more conservative values for the x and y range will be used.

        For example if the min x is found to be 100 and 110 at two locations,
        the value of 110 is used.
        """
        min_x, min_y = self._calibrate_corner(x_duty=0, y_duty=0)
        self._board_x_range[0] = min_x
        self._board_y_range[0] = min_y

        max_x, min_y = self._calibrate_corner(x_duty=1, y_duty=0)
        self._board_x_range[1] = max_x
        if min_y > self._board_y_range[0]:
            self._board_y_range[0] = min_y

        max_x, max_y = self._calibrate_corner(x_duty=1, y_duty=1)
        if max_x < self._board_x_range[1]:
            self._board_x_range[1] = max_x
        self._board_y_range[1] = max_y

        min_x, max_y = self._calibrate_corner(x_duty=0, y_duty=1)
        if min_x > self._board_x_range[0]:
            self._board_x_range[0] = min_x
        if max_y < self._board_y_range[1]:
            self._board_y_range[1] = max_y

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
        data = [self._board_x_range[0], self._board_x_range[1],
                self._board_y_range[0], self._board_y_range[1]]
        with open(self._calibration_file_path, 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerow(data)

    def _load_calibration(self):
        """
        Load a board calibration saved in `calibration.csv`.
        """
        with open(self._calibration_file_path, 'r', encoding='UTF8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self._board_x_range[0] = int(row['x-min'])
                self._board_x_range[1] = int(row['x-max'])
                self._board_y_range[0] = int(row['y-min'])
                self._board_y_range[1] = int(row['y-max'])
                break

    def _random_position(self):
        """Generate a random position on the board.

        Returns:
            A random position on the board.
        """
        return [random.randint(self._board_x_range[0], self._board_x_range[1]),
                random.randint(self._board_y_range[0], self._board_y_range[1])]

    def action_spec(self):
        """
        Defines the actions that should be provided to `step()`.

        Returns:
            The action specification corresponding to `action_spec()`.
        """
        return self._action_spec

    def observation_spec(self):
        """
        Defines the observations that that are returned by `step()`.

        Returns:
            The observation specification corresponding to `observation_spec()`.
        """
        return self._observation_spec

    def _reset(self):
        """
        Start a new RL sequence.

            Returns:
                The initial TimeStep of the environment.
        """
        # The default location of the ball on the board is (min x, min y)
        self._state = [self._board_x_range[0], self._board_y_range[0]]
        self._uart_comm(SERIAL_X_DIM, 0)
        self._uart_comm(SERIAL_Y_DIM, 0)
        # wait for ball to reach default location
        sleep(3)
        # A new random goal is created
        self._goal = self._random_position()
        return ts.restart(np.array([self._state], dtype=np.float16))

    def _step(self, action):
        """
        Update the environment according to an action.

        Args:
            action: The action to take corresponding to `action_spec()`.

        Returns:
            The next TimeStep of the environment.
        """
        motor_x_command = action[0]
        motor_y_command = action[1]

        ball_position_x = self._uart_comm(SERIAL_X_DIM, motor_x_command)
        ball_position_y = self._uart_comm(SERIAL_Y_DIM, motor_y_command)

        # keep ball position in range of board
        ball_position_x = max(
            min(self._board_x_range[1], ball_position_x), self._board_x_range[0])
        ball_position_y = max(
            min(self._board_y_range[1], ball_position_y), self._board_y_range[0])

        reward = -math.dist([ball_position_x, ball_position_y], self._goal)

        return ts.transition(np.array([self._state], dtype=np.uint16), reward)

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
        sleep(0.011)

        duty = (int)(900 + (duty_percent * 1200))
        duty_low_bits, duty_high_bits = (duty & 0xFFFFFFFF).to_bytes(2, 'big')
        message = [0, dimension, duty_low_bits, duty_high_bits]
        message_bytes = bytearray(message)
        self._serial.write(message_bytes)

        response_low_bytes = self._serial.read()
        response_high_bytes = self._serial.read()
        response_bytes = response_low_bytes + response_high_bytes
        response = int.from_bytes(response_bytes, 'big')

        return np.uint16(response)
