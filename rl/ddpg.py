"""
Module defining trainer
"""
from pathlib import Path
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt

@tf.function
def update_target(target_weights, weights, tau):
    """
    Update the target network weights according to the DDPG algorithm.

    Args:
        target_weights: new weights for target model.
        weights: new weights for model.
        tau: update target weights slowly based on tau which is much less than 1.
    """
    for (target_weight, weight) in zip(target_weights, weights):
        target_weight.assign(weight * tau + target_weight * (1 - tau))

@tf.function
def update_critic(critic, target_actor, target_critic, gamma, optimizer, minibatch_transitions):
    """
    Update critic model weights according to the DDPG algorithm.

    Args:
        critic: Critic model.
        target_actor: Target actor model.
        target_critic: Target critic model.
        gamma: Reward decay.
        optimizer: Critic model optimizer.
        minibatch_transitions: Minibatch of transitions.
    """
    state_batch = minibatch_transitions[0]
    action_batch = minibatch_transitions[1]
    reward_batch = minibatch_transitions[2]
    next_state_batch = minibatch_transitions[3]

    with tf.GradientTape() as tape:
        target_actor_output = target_actor(next_state_batch, training=True)
        y = reward_batch + gamma * target_critic([next_state_batch, target_actor_output], training=True)
        critic_output = critic([state_batch, action_batch], training=True)
        loss = tf.math.reduce_mean(tf.math.square(y - critic_output))

    gradient = tape.gradient(loss, critic.trainable_variables)
    optimizer.apply_gradients(zip(gradient, critic.trainable_variables))

@tf.function
def update_actor(actor, critic, optimizer, minibatch_transitions):
    """
    Update actor model weights according to the DDPG algorithm.

    Args:
        actor: Actor model.
        critic: Critic model.
        optimizer: Actor model optimizer.
        minibatch_transitions: Minibatch of transitions.
    """
    state_batch = minibatch_transitions[0]

    with tf.GradientTape() as tape:
        actions = actor(state_batch, training=True)
        critic_output = critic([state_batch, actions], training=True)
        # Use `-value` to maximize the value given by the critic for our actions
        loss = -tf.math.reduce_mean(critic_output)

    gradient = tape.gradient(loss, actor.trainable_variables)
    optimizer.apply_gradients(zip(gradient, actor.trainable_variables))

def train(env,
        actor,
        critic,
        target_actor,
        target_critic,
        actor_optimizer,
        critic_optimizer,
        ou_noise,
        replay_buffer,
        episodes,
        gamma,
        tau,
        lower_bound,
        upper_bound,
        results_dir='results',
        render=False):
    """
    Train according to the DDPG algorithm.

    Args:
        env: Environment.
        actor: Actor model.
        critic: Critic model.
        target_actor: Target actor model.
        target_critic: Target critic model.
        actor_optimizer: Actor model optimizer.
        critic_optimizer: Critic model optimizer.
        ou_noise: `OUNoise` object.
        replay_buffer: `ReplayBuffer` object.
        episodes: Number of training episodes.
        gamma: Reward decay.
        tau: Target model learning parameter.
        lower_bound: Lower bound on actor predictions.
        upper_bound: Upper bound on actor predictions.
        results_dir: Directory to save trained models (`default='results'`).
        render: If true, call `env.render()` during each step (`default=False`).
    """
    # To store reward history of each episode
    reward_list = []
    # To store average reward history of last few episodes
    avg_reward_list = []

    for episode in range(episodes):
        # UNCOMMENT LINE FOR ABS ENVIRONMENT
        # prev_state, _, _, _ = env.reset()
        # UNCOMMENT LINE FOR GYM ENVIRONMENTS
        prev_state = env.reset()
        episodic_reward = 0
        while True:
            if render:
                env.render()

            prev_state = tf.expand_dims(tf.convert_to_tensor(prev_state), 0)

            action = tf.squeeze(actor(prev_state)).numpy() + ou_noise()
            action = (((action + 1) * (upper_bound - lower_bound)) / 2) + lower_bound
            # action = np.clip(action, lower_bound, upper_bound)
            if not isinstance(action, np.ndarray):
                action = np.array([action])

            state, reward, done, info = env.step(action)
            
            episodic_reward += reward

            replay_buffer.record((prev_state, action, reward, state))
            minibatch_transitions = replay_buffer.batch()

            update_critic(critic, target_actor, target_critic, gamma, critic_optimizer, minibatch_transitions)
            update_actor(actor, critic, actor_optimizer, minibatch_transitions)

            update_target(target_actor.variables, actor.variables, tau)
            update_target(target_critic.variables, critic.variables, tau)

            if done:
                break

            prev_state = state

        reward_list.append(episodic_reward)

        # Mean of last 40 episodes
        avg_reward = np.mean(reward_list[-40:])
        print(f"Episode * {episode} * Avg Reward is ==> {avg_reward}")
        avg_reward_list.append(avg_reward)

    # Plotting graph
    # Episodes versus Avg. Rewards
    plt.plot(avg_reward_list)
    plt.xlabel("Episode")
    plt.ylabel("Avg. Epsiodic Reward")
    plt.show()

    # Save the weights

    save_path = (Path(__file__).parent / results_dir).resolve()
    save_path.mkdir(parents=True, exist_ok=True)

    actor.save_weights(save_path / "actor.h5")
    critic.save_weights(save_path / "critic.h5")

    target_actor.save_weights(save_path / "target_actor.h5")
    target_critic.save_weights(save_path / "target_critic.h5")

def test(env,
        actor,
        episodes,
        lower_bound,
        upper_bound,
        results_dir='results',
        render=False):
    """
    Test trained actor model.

    Args:
        env: Environment.
        actor: Actor model.
        episodes: Number of test episodes.
        lower_bound: Lower bound on actor predictions.
        upper_bound: Upper bound on actor predictions.
        results_dir: Directory to save trained models (`default='results'`).
        render: If true, call `env.render()` during each step (`default=False`).
    """
    load_path = (Path(__file__).parent / results_dir).resolve()

    actor.load_weights(load_path / "actor.h5")
    # To store reward history of each episode
    reward_list = []
    # To store average reward history of last few episodes
    avg_reward_list = []

    for episode in range(episodes):
        prev_state = env.reset()
        episodic_reward = 0
        while True:
            if render:
                env.render()

            prev_state = tf.expand_dims(tf.convert_to_tensor(prev_state), 0)

            action = tf.squeeze(actor(prev_state)).numpy()
            action = np.clip(action, lower_bound, upper_bound)
            if not isinstance(action, np.ndarray):
                action = np.array([action])

            state, reward, done, info = env.step(action)
            episodic_reward += reward

            if done:
                break

            prev_state = state

        reward_list.append(episodic_reward)

        # Mean of last 40 episodes
        avg_reward = np.mean(reward_list[-40:])
        print(f"Episode * {episode} * Avg Reward is ==> {avg_reward}")
        avg_reward_list.append(avg_reward)

    # Plotting graph
    # Episodes versus Avg. Rewards
    plt.plot(avg_reward_list)
    plt.xlabel("Episode")
    plt.ylabel("Avg. Epsiodic Reward")
    plt.show()
