"""
Module defining replay buffer.
"""
import numpy as np
import tensorflow as tf

class ReplayBuffer:
    """
    Replay buffer.
    """
    def __init__(self, num_states, num_actions, buffer_capacity=100000, batch_size=64):
        """
        Initialize replay buffer.

        Args:
            num_states: shape of state.
            num_actions: shape of actions.
            buffer_capacity: capacity of buffer.
            batch_size: batch size of buffer.
        """
        self.buffer_capacity = buffer_capacity
        self.batch_size = batch_size

        self.curr_buffer_size = 0

        self.state_buffer = np.zeros((self.buffer_capacity, num_states))
        self.action_buffer = np.zeros((self.buffer_capacity, num_actions))
        self.reward_buffer = np.zeros((self.buffer_capacity, 1))
        self.next_state_buffer = np.zeros((self.buffer_capacity, num_states))

    def record(self, transition):
        """
        Record a new transition into the replay buffer.

        Args:
            transition: A tuple of (state, action, reward, next state).
        """
        # Set index to zero if buffer_capacity is exceeded, replacing old records
        index = self.curr_buffer_size % self.buffer_capacity

        self.state_buffer[index] = transition[0]
        self.action_buffer[index] = transition[1]
        self.reward_buffer[index] = transition[2]
        self.next_state_buffer[index] = transition[3]

        self.curr_buffer_size += 1

    def batch(self):
        """
        Sample a random minibatch of transitions (state, action, reward, next state).

        Returns:
            A minibatch of transition.
        """
        # Get sampling range
        record_range = min(self.curr_buffer_size, self.buffer_capacity)
        # Randomly sample indices
        batch_indices = np.random.choice(record_range, self.batch_size)

        # Convert to tensors
        state_batch = tf.convert_to_tensor(self.state_buffer[batch_indices])
        action_batch = tf.convert_to_tensor(self.action_buffer[batch_indices])
        reward_batch = tf.convert_to_tensor(self.reward_buffer[batch_indices])
        reward_batch = tf.cast(reward_batch, tf.float32)
        next_state_batch = tf.convert_to_tensor(self.next_state_buffer[batch_indices])

        return (state_batch, action_batch, reward_batch, next_state_batch)
