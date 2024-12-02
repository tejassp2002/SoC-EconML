"""
This python code file implements the multi-arm stochastic bandit moss algorithm.
MOSS stands for  Minimax Optimal Strategy in the Stochastic case.
Comments are added at suitable places to enable the reader to get insights from the code.
Graphs are created to show the efficiency and accuracy of the results so obtained.
There are various versions of moss. This version has been taken from https://tor-lattimore.com/downloads/book/book.pdf and https://www.di.ens.fr/willow/pdfscurrent/COLT09a.pdf.
"""

# To create visual charts, matplotlib is the best python library.
import matplotlib.pyplot as plt

# Numpy is generally used for fast calculations and array handling.
import numpy as np


def log_plus(x):
    """This function is required in the algorithm code."""
    return np.log(max(1,x))

def simulate_rewards(num_arms):
    """Randomly chosing reward values for each arm."""
    rewards = np.random.uniform(0, 1, num_arms)
    return rewards

def moss_algorithm(num_arms, num_rounds):
    """This is the main algorithm funcion. It takes two arguments: number of rounds and number of arms. It will return the value of total regret after specified number of rounds."""
    weight_index = np.zeros(num_arms)       #Initializing the weights to be used in the function.
    mean_reward = simulate_rewards(num_arms)            # This is the array which will store the mean rewards of each arm.
    arm_counts = np.ones(num_arms)                      # Number of times each arm is chosen.
    regret = 0                                          # The total regret suffered.

    for t in range(num_rounds):
        for i in range(num_arms):
            # Updating the weight index.
            weight_index[i] = mean_reward[i] + pow(((4/arm_counts[i])*log_plus(num_rounds/(num_arms*arm_counts[i]))),1/2)

        arm = np.argmax(weight_index)           # Chosing the arm having the largest weight_index.
        rewards = simulate_rewards(num_arms)        # Drawing rewards.
        regret += np.max(rewards)-rewards[arm]      # Updating Regret.
        arm_counts[arm] += 1                        # Increasing the number of counts of that arm.
        mean_reward[arm] = (mean_reward[arm]*(arm_counts[arm]-1)+rewards[arm])/arm_counts[arm]      # Updating the mean reward.
    return regret

num_arms = 10
num_rounds = 1000
x = range(num_rounds)
y = [moss_algorithm(num_arms, j) for j in range(num_rounds)]
plt.plot(x, y)
plt.xlabel("Rounds")
plt.ylabel("Regret")
plt.title("Regret vs. Rounds")
plt.show()