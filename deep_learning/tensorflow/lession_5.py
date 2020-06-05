import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import gym
import time


def random_policy(n):
    return np.random.randint(0, n)


def function_1():
    env_name = 'Breakout-v4'
    env = gym.make(env_name)
    obs = env.reset()
    env.render()
    for step in range(1000):
        action = random_policy(4)
        obs, reward, done, info = env.step(action)
        env.render()
        time.sleep(0.03)
        if done:
            img = env.render(mode='rgb_array')
    plt.imshow(img)
    plt.show()
    print(step)


if __name__ == '__main__':
    function_1()




