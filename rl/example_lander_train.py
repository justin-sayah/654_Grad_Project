"""
Module containing example DDPG training: LunarLanderContinuous-v2 environment.
"""
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import gym

import tensorflow as tf
import numpy as np
from ou_noise import OUNoise
from replay_buffer import ReplayBuffer
import ddpg
from models import get_actor, get_critic

def main():
    """
    Example DDPG training for LunarLanderContinuous-v2 environment.
    """
    #####################################
    ######### Environment Setup #########
    #####################################
    env = gym.make("LunarLanderContinuous-v2")

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
    std_dev = 0.2
    ou_noise = OUNoise(mean=np.zeros(1), std_deviation=float(std_dev) * np.ones(1))

    actor_model = get_actor(num_states, num_actions, lower_bound, upper_bound)
    critic_model = get_critic(num_states, num_actions)

    target_actor = get_actor(num_states, num_actions, lower_bound, upper_bound)
    target_critic = get_critic(num_states, num_actions)

    # Making the weights equal initially
    target_actor.set_weights(actor_model.get_weights())
    target_critic.set_weights(critic_model.get_weights())

    # Learning rate for actor-critic models
    critic_lr = 0.002
    actor_lr = 0.001

    critic_optimizer = tf.keras.optimizers.Adam(critic_lr)
    actor_optimizer = tf.keras.optimizers.Adam(actor_lr)

    total_episodes = 10

    # Discount factor for future rewards
    gamma = 0.99
    # Used to update target networks
    tau = 0.005

    buffer_capacity = 50000
    batch_size = 64
    buffer = ReplayBuffer(num_states, num_actions, buffer_capacity, batch_size)

    save_dir = 'results/lander'

    render = False

    ############################
    ######### Training #########
    ############################
    ddpg.train(
        env=env,
        actor=actor_model,
        critic=critic_model,
        target_actor=target_actor,
        target_critic=target_critic,
        actor_optimizer=actor_optimizer,
        critic_optimizer=critic_optimizer,
        ou_noise=ou_noise,
        replay_buffer=buffer,
        episodes=total_episodes,
        gamma=gamma,
        tau=tau,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        results_dir=save_dir,
        render=render)

if __name__ == '__main__':
    main()
