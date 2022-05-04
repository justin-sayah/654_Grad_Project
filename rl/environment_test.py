"""
Module containing Amazing Ball System RL environment tests.
"""
from environment import AmazingBallSystemEnv
from tf_agents.environments import wrappers
import numpy as np

PORT = '/dev/cu.usbserial-1420'
CALIBRATE = True

def main():
    """
    Tests
    """
    environment = AmazingBallSystemEnv(port=PORT, calibrate=CALIBRATE, seed=None)

    duration = 100 # TimeSteps
    environment_timelimit = wrappers.TimeLimit(env=environment, duration=duration)

    num_episodes = 3

    rewards = []
    steps = []

    # randomly select actions for episode durations
    for _ in range(num_episodes):
        time_step = environment_timelimit.reset()
        episode_reward = 0
        episode_steps = 0
        while not time_step.is_last():
            action = np.random.random((2, 1))
            time_step = environment_timelimit.step(action)
            episode_steps += 1
            episode_reward += time_step.reward
        rewards.append(episode_reward)
        steps.append(episode_steps)

    num_steps = np.sum(steps)
    avg_length = np.mean(steps)
    avg_reward = np.mean(rewards)

    print('num_episodes:', num_episodes, 'num_steps:', num_steps)
    print('avg_length', avg_length, 'avg_reward:', avg_reward)

if __name__ == '__main__':
    main()
