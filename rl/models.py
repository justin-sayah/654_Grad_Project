"""
Module containing definitions for actor and critic models.
"""
import tensorflow as tf

def get_actor(num_states, num_actions, lower_bound, upper_bound):
    """
    Create an actor model.

    Args:
        num_states: shape of state.
        num_actions: shape of actions.
        lower_bound: lower bound of action output.
        upper_bound: upper bound of action output.

    Returns:
        An actor model.
    """
    # Initialize weights between -3e-3 and 3-e3
    last_init = tf.random_uniform_initializer(minval=-0.003, maxval=0.003)

    inputs = tf.keras.layers.Input(shape=(num_states,))
    out = tf.keras.layers.Dense(256, activation="relu")(inputs)
    out = tf.keras.layers.Dense(256, activation="relu")(out)
    outputs = tf.keras.layers.Dense(num_actions, activation="tanh", kernel_initializer=last_init, use_bias=False, activity_regularizer=tf.keras.regularizers.L2(1e-5))(out)

    # outputs: old range (-1, 1) -> new range (lower_bound, upper_bound)
    # https://math.stackexchange.com/questions/1205733/how-to-convert-or-transform-from-one-range-to-another
    outputs = (((outputs + 1) * (upper_bound - lower_bound)) / 2) + lower_bound

    model = tf.keras.Model(inputs, outputs)

    return model

def get_critic(num_states, num_actions):
    """
    Create a critic model.

    Args:
        num_states: shape of state.
        num_actions: shape of actions.

    Returns:
        A critic model.
    """
    # State as input
    state_input = tf.keras.layers.Input(shape=(num_states))
    state_out = tf.keras.layers.Dense(16, activation="relu")(state_input)
    state_out = tf.keras.layers.Dense(32, activation="relu")(state_out)

    # Action as input
    action_input = tf.keras.layers.Input(shape=(num_actions))
    action_out = tf.keras.layers.Dense(32, activation="relu")(action_input)

    # Both are passed through seperate layer before concatenating
    concat = tf.keras.layers.Concatenate()([state_out, action_out])

    out = tf.keras.layers.Dense(512, activation="relu")(concat)
    out = tf.keras.layers.Dense(512, activation="relu")(out)
    outputs = tf.keras.layers.Dense(1)(out)

    # Outputs single value for give state-action
    model = tf.keras.Model([state_input, action_input], outputs)

    return model
