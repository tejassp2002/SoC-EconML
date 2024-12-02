"""
This python code file implements the multi-arm bandit exp3.p algorithm.
Comments are added at suitable places to enable the reader to get insights from the code.
Graphs are created to show the efficiency and accuracy of the results so obtained.
There are various versions of exp3.p. This version has been taken from http://rob.schapire.net/papers/AuerCeFrSc01.pdf. 
"""

# To create visual charts, matplotlib is the best python library.
import matplotlib.pyplot as plt

# Numpy is generally used for fast calculations and array handling.
import numpy as np

# Contains useful mathematical functions
import math

def exp3_algorithm(num_arms, gamma, T):
    """
    This is the main function implementing exp3 algorithm.
    It takes 3 arguments. num_arms denotes the number of arms in the multi-armed bandit problem.
    gamma is the probability of exploration versus exploitation.
    T are the number of rounds which we have to run.
    """
    regret = []
    # Higher alpha means more exploration. The below value of alpha is the optimal value so as to bound the regret in some delta radius.
    # alpha = math.sqrt(2 * math.log(num_arms) / (num_arms * T))
    alpha = 0
    weights = np.zeros(num_arms)        # Initializing the weights. 
    probabilities = np.ones(num_arms)/num_arms      # Initializing the probabilities. 
    weights = np.ones(num_arms)*np.exp(alpha*gamma*(pow(T/num_arms, 1/2))/3)
    for t in range(T):                              # Number of rounds.
        # Update for each arm.
        probabilities = (1-gamma)*(weights)/(np.sum(weights)) + gamma/num_arms    
        arm = np.random.choice(np.arange(num_arms), p = probabilities)      # Choosing an arm on the basis of probabilities.
        rewards = simulate_rewards(num_arms)                    # Simulating rewards after each round.
        regret.append(max(rewards)-rewards[arm])
                
        for j in range(num_arms):                               # Changing the rewards suitably.
            if j == arm:
                rewards[j] = rewards[j]/probabilities[j]
            else:
                rewards[j] = 0
        weights*=np.exp((gamma/(3*num_arms))*(rewards+alpha/(probabilities*pow(num_arms*T, 1/2))))             # Updating weights.
        
    return sum(regret)              # Returning normalized weights.
def exp3p_algorithm(num_arms, gamma, T):
    """
    This is the main function implementing exp3 algorithm.
    It takes 3 arguments. num_arms denotes the number of arms in the multi-armed bandit problem.
    gamma is the probability of exploration versus exploitation.
    T are the number of rounds which we have to run.
    """
    regret = []
    # Higher alpha means more exploration. The below value of alpha is the optimal value so as to bound the regret in some delta radius.
    alpha = math.sqrt(2 * math.log(num_arms) / (num_arms * T))
    # alpha = 0
    weights = np.zeros(num_arms)        # Initializing the weights. 
    probabilities = np.ones(num_arms)/num_arms      # Initializing the probabilities. 
    weights = np.ones(num_arms)*np.exp(alpha*gamma*(pow(T/num_arms, 1/2))/3)
    for t in range(T):                              # Number of rounds.
        # Update for each arm.
        probabilities = (1-gamma)*(weights)/(np.sum(weights)) + gamma/num_arms    
        arm = np.random.choice(np.arange(num_arms), p = probabilities)      # Choosing an arm on the basis of probabilities.
        rewards = simulate_rewards(num_arms)                    # Simulating rewards after each round.
        regret.append(max(rewards)-rewards[arm])
                
        for j in range(num_arms):                               # Changing the rewards suitably.
            if j == arm:
                rewards[j] = rewards[j]/probabilities[j]
            else:
                rewards[j] = 0
        weights*=np.exp((gamma/(3*num_arms))*(rewards+alpha/(probabilities*pow(num_arms*T, 1/2))))             # Updating weights.
        
    return sum(regret)              # Returning normalized weights.

def simulate_rewards(num_arms):
    """Randomly chosing reward values for each arm."""
    rewards = np.random.uniform(0, 1, num_arms)
    return rewards

gamma = 0.6
num_arms = 10
range_num_arms = np.arange(100, 10000, 10)
regret_exp3 = [exp3_algorithm(num_arms, gamma, i) for i in range_num_arms]
regret_exp3p= [exp3p_algorithm(num_arms, gamma, i) for i in range_num_arms]
plt.subplot(1,2,1)
plt.plot(range_num_arms, regret_exp3)
plt.xlabel("Number of Rounds")
plt.ylabel("Regret Obtained")
plt.title("EXP3")

plt.subplot(1,2,2)
plt.plot(range_num_arms, regret_exp3p)
plt.xlabel("Number of Rounds")
plt.ylabel("Regret Obtained")
plt.title("EXP3.P")
plt.show()
# plt.savefig("EXP3.png")