"""TODO: Description
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
import tensorflow as tf

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

SERIAL_X_DIM = 0
SERIAL_Y_DIM = 1

class AmazingBallSystemEnv(py_environment.PyEnvironment):

    def __init__(self, port='/dev/ttyUSB0', calibrate=True, seed=None):
        self._action_spec = array_spec.BoundedArraySpec(shape=(2, ),
                                                        dtype=np.float16,
                                                        minimum=0,
                                                        maximum=1,
                                                        name='action')
        self._observation_spec = array_spec.BoundedArraySpec(shape=(2, ),
                                                             dtype=np.uint16,
                                                             name='observation')
        self._state = [0, 0]

        self._x_range = [0, 0]
        self._y_range = [0, 0]
        self._serial = serial.Serial(port=port)

        self._calibration_file_path = Path(__file__).parent.resolve() / 'calibration.csv'
        if calibrate:
            self._calibration()
        else:
            self._load_calibration()
        print(f'ABS calibrated: x:{self._x_range} y:{self._y_range}')

        self._seed = seed
        self._goal = [0, 0]

        self._reset()

    def _calibration(self):
        # set ball location (bottom left)
        self._send_comm(SERIAL_X_DIM, 0)
        self._send_comm(SERIAL_Y_DIM, 0)
        # wait for ball to move
        sleep(3)
        # measure
        x = self._send_comm(SERIAL_X_DIM, 0)
        y = self._send_comm(SERIAL_Y_DIM, 0)
        self._x_range[0] = x
        self._y_range[0] = y

        # set ball location (top left)
        self._send_comm(SERIAL_X_DIM, 1)
        self._send_comm(SERIAL_Y_DIM, 0)
        sleep(3)
        x = self._send_comm(SERIAL_X_DIM, 1)
        y = self._send_comm(SERIAL_Y_DIM, 0)
        self._x_range[1] = x
        # take more conservative estimate
        if self._y_range[0] < y:
            self._y_range[0] = y

        # set ball location (top right)
        self._send_comm(SERIAL_X_DIM, 1)
        self._send_comm(SERIAL_Y_DIM, 1)
        sleep(3)
        x = self._send_comm(SERIAL_X_DIM, 1)
        y = self._send_comm(SERIAL_Y_DIM, 1)
        if self._x_range[1] > x:
            self._x_range[1] = x
        self._y_range[1] = y

        # set ball location (top right)
        self._send_comm(SERIAL_X_DIM, 0)
        self._send_comm(SERIAL_Y_DIM, 1)
        sleep(3)
        x = self._send_comm(SERIAL_X_DIM, 0)
        y = self._send_comm(SERIAL_Y_DIM, 1)
        if self._x_range[0] < x:
            self._x_range[0] = x
        if self._y_range[1] > y:
            self._y_range[1] = y

        header = ['x-min', 'x-max', 'y-min', 'y-max']
        data = [self._x_range[0], self._x_range[1], self._y_range[0], self._y_range[1]]
        with open(self._calibration_file_path, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)

    def _load_calibration(self):
         with open(self._calibration_file_path, 'r', encoding='UTF8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self._x_range[0] = int(row['x-min'])
                self._x_range[1] = int(row['x-max'])
                self._y_range[0] = int(row['y-min'])
                self._y_range[1] = int(row['y-max'])
                break

    def _random_goal(self):
        if self._seed is not None:
            random.seed(self._seed)

        min_x = self._x_range[0]
        max_x = self._x_range[1]
        min_y = self._y_range[0]
        max_y = self._y_range[1]

        self._goal = [random.randint(min_x, max_x),
                      random.randint(min_y, max_y)]

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._state = [0, 0]
        self._random_goal()
        self._send_comm(SERIAL_X_DIM, 0)
        self._send_comm(SERIAL_Y_DIM, 0)
        sleep(3)
        return ts.restart(np.array([self._state], dtype=np.float16))

    def _step(self, action):
        # send action to ABS and wait for reponse
        x = self._send_comm(SERIAL_X_DIM, action[0])
        y = self._send_comm(SERIAL_Y_DIM, action[1])

        if x < self._x_range[0]:
            x = self._x_range[0]
        elif x > self._x_range[1]:
            x = self._x_range[1]

        if y < self._y_range[0]:
            y = self._y_range[0]
        elif y > self._y_range[1]:
            y = self._y_range[1]

        reward = -math.dist([x, y], self._goal)

        return ts.transition(np.array([self._state], dtype=np.uint16), reward)

    def _send_comm(self, dimension, duty_percent):
        sleep(0.011)
        duty = (int)(900 + (duty_percent * 1200))
        lowBitsSend, highBitsSend = (duty & 0xFFFFFFFF).to_bytes(2, 'big')
        testSend = [0, dimension, lowBitsSend, highBitsSend]
        byteSend = bytearray(testSend)
        self._serial.write(byteSend)
        lowByteRead = self._serial.read()
        highByteRead = self._serial.read()
        allBytes = lowByteRead + highByteRead
        dimensionRead = int.from_bytes(allBytes, 'big')
        return np.uint16(dimensionRead)


# TEST 1:
env_timelimit = wrappers.TimeLimit(env=env, duration=100)
# num_episodes = 3

# rewards = []
# steps = []

# for _ in range(num_episodes):
#     time_step = env_timelimit.reset()
#     episode_reward = 0
#     episode_steps = 0
#     while not time_step.is_last():
#         action = np.random.random((2, 1))
#         time_step = env_timelimit.step(action)
#         episode_steps += 1
#         episode_reward += time_step.reward
#     rewards.append(episode_reward)
#     steps.append(episode_steps)

# num_steps = np.sum(steps)
# avg_length = np.mean(steps)
# avg_reward = np.mean(rewards)

# print('num_episodes:', num_episodes, 'num_steps:', num_steps)
# print('avg_length', avg_length, 'avg_reward:', avg_reward)
