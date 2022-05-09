"""
Module containing DDPG training: AmazingBallSystemEnv environment.
"""
from environment import AmazingBallSystemEnv
import tensorflow as tf
import numpy as np
import ddpg
from models import get_actor

def main():
    """
    Example DDPG testing for AmazingBallSystemEnv environment.
    """
    #####################################
    ######### Environment Setup #########
    #####################################
    port = '/dev/cu.usbserial-1410'
    calibrate = False
    episode_duration = 100
    env = AmazingBallSystemEnv(port=port, calibrate=calibrate, duration=episode_duration)

    num_states = env.observation_space.shape[0]
    print(f"Size of State Space ->  {num_states}")

    num_actions = env.action_space.shape[0]
    print(f"Size of Action Space ->  {num_actions}")

    upper_bound = env.action_space.high[0]
    print(f"Max Value of Action ->  {upper_bound}")

    lower_bound = env.action_space.low[0]
    print(f"Min Value of Action ->  {lower_bound}")

    ############################################
    ######### Training Hyperparameters #########
    ############################################
    actor_model = get_actor(num_states, num_actions, lower_bound, upper_bound)

    total_episodes = 10

    save_dir = 'results/abs'

    render = False

    total_episodes = 10

    ############################
    ######### Training #########
    ############################
    ddpg.test(
        env=env,
        actor=actor_model,
        episodes=total_episodes,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        results_dir=save_dir,
        render=render)

if __name__ == '__main__':
    main()
