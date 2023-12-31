# -*- coding: utf-8 -*-
"""Cartpole_QLearning

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GOVIYFcl7lP1lmpuI-cAwRCbKEmbINJV
"""

import gym
import numpy as np
import matplotlib.pyplot as plt

# Function to generate Fourier basis features
def fourier_basis(state, num_bases):
    state = np.array(state)
    basis = []
    for i in range(num_bases):
        angle = np.pi * i * state / 2
        basis.extend(np.cos(angle))
    return np.array(basis)

# Q-learning parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Epsilon-greedy exploration
num_episodes = 1000

# Fourier basis parameters
num_bases = 20

# Initialize Q-table
env = gym.make('CartPole-v1')
state_dim = len(fourier_basis(env.reset(), num_bases))
action_dim = env.action_space.n
Q = np.zeros((state_dim, action_dim))

# Lists to store rewards for plotting
episode_rewards = []

def state_to_index(state_basis):
    return np.argmax(state_basis.dot(np.arange(state_dim)))

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        # Select action using epsilon-greedy policy
        if np.random.rand() < epsilon:
            action = env.action_space.sample()
        else:
            state_basis = fourier_basis(state, num_bases)
            state_index = state_to_index(state_basis)
            action = np.argmax(Q[state_index, :])

        # Take the chosen action
        next_state, reward, done, _ = env.step(action)

        # Update Q-value using Q-learning
        next_state_basis = fourier_basis(next_state, num_bases)
        next_state_index = state_to_index(next_state_basis)
        Q[state_index, action] += alpha * (reward + gamma * np.max(Q[next_state_index, :]) - Q[state_index, action])

        state = next_state
        total_reward += reward

    episode_rewards.append(total_reward)

env.close()

# Plot the rewards per episode
plt.plot(episode_rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Q-Learning with Linear Function Approximation')
plt.show()

def run_policy_with_learned_Q(Q, num_bases):
    env = gym.make('CartPole-v1',render_mode='human')
    episode_reward = 0

    for _ in range(10):  # Run for a fixed number of episodes
        state = env.reset()
        done = False

        while not done:
            state_basis = fourier_basis(state, num_bases)
            action = np.argmax(Q[state_to_index(state_basis), :])
            state, reward, done, _ = env.step(action)
            episode_reward += reward
            env.render()  # Render the environment (you may need to adjust this)

    env.close()
    return episode_reward

# Assuming you have the Q-table (Q) and num_bases learned from Q-learning
total_reward = run_policy_with_learned_Q(Q, num_bases)
print("Total reward from the learned policy:", total_reward)