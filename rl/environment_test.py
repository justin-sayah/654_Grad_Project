"""
Module containing tests for the AmazingBallSystemEnv environment.
"""
from environment import AmazingBallSystemEnv

PORT = '/dev/cu.usbserial-1420'
CALIBRATE = True
DURATION = 100

def main():
    """
    Tests
    """
    env = AmazingBallSystemEnv(port=PORT, calibrate=CALIBRATE, duration=DURATION)
    env.reset()
    while True:
        # Take a random action
        action = env.action_space.sample()
        _, _, done, _ = env.step(action)

        # Render the game
        # env.render()

        if done is True:
            break

    env.close()

if __name__ == '__main__':
    main()
