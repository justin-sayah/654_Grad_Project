from environment import AmazingBallSystemEnv
from tf_agents.environments import wrappers

PORT = '/dev/cu.usbserial-1410'
CALIBRATE = True 

def main():
    env = AmazingBallSystemEnv(port=PORT, calibrate=CALIBRATE, seed=None)

if __name__ == '__main__':
    main()
