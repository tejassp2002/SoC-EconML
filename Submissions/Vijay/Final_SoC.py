
from math import sqrt
import numpy as np
import random
import matplotlib.pyplot as plt
T=9
N=7
#setting up intial values for market dynamics, we can change this according to specific probelm statements
c=5
v=150
f=2
r=1
m=1.5
part_s = []
part_b = []
# Function to calculate the true valuation of each seller and buyer with randomized weights
#The weights are randomized in order to take into consideration different preferences that each buyer and seller may have
def valuation(contract, volume, flexibility, renewable_energy, market_conditions):
    weights = [random.random() for _ in range(6)]
    total_sum = sum(weights)
    weights = [num / total_sum for num in weights]
    t_valuation = weights[0] * contract + weights[1] * volume + weights[2] * flexibility + weights[3] * renewable_energy +  weights[4] * market_conditions
    return t_valuation
#Defining a seller class 
class Sellers:
    def __init__(self):   
        self.t_valuation = valuation(c, v, f, r, m)   
        self.c_valuation = 30 + 20 * random.uniform(-1,1)
        self.rp_seller = 0
        self.avg_deal = 0
        self.alpha = 4 + 4 * random.random()
        self.regret = 0
# Function to update the current valuation of a seller based on recent deals
def updateval(t, rp_seller, avg_deal, alpha):
    cval = 0
    if rp_seller != 0 and t != 0:
        cval = avg_deal - sqrt((alpha * np.log(t)) / rp_seller)
    return cval
#Defining a Buyer class
class Buyers:
    def __init__(self):
        self.t_valuation = valuation(c, v, f, r, m)
        self.c_valuation = 30 + 20 * random.uniform(-1,1)
        self.rp_buyer = 0
        self.avg_deal = 0
        self.alpha = 4 + 4 * random.random()
        self.reward = 0
        self.regret = 0
# Function to update the current valuation of a buyer based on recent deals
def b_updateval(t, rp_buyer, avg_deal, alpha):
    cval = 0
    if rp_buyer != 0:
        cval = avg_deal + sqrt((alpha * (np.log(t))) / rp_buyer)
    return cval
# Function to find the price for the current iteration of the auction
def findprice(sellers, buyers):
    arr = []
    for seller in sellers:
        arr.append(seller)
    arr1 = []
    for buyer in buyers:
        arr1.append(buyer)
    arr.sort(key=lambda x: x.c_valuation)
    arr1.sort(key=lambda x: x.c_valuation)
    b_index = 0
    s_index = 0
    while b_index < len(arr1) and s_index < len(arr):
        if arr1[b_index].c_valuation >= arr[s_index].c_valuation:
            part_b.append(arr1[b_index])
            part_s.append(arr[s_index])
            b_index = b_index + 1
            s_index = s_index + 1
        else:
            b_index = b_index + 1
    if len(part_b) != 0 and len(part_s) != 0:
        price = 0.5 * (part_s[len(part_s) - 1].c_valuation + part_b[len(part_b) - 1].c_valuation)
    else:
        price = 0
    return price
# Function to find the optimal price of the auction based on true valuations
def find_optimal_price(sellers, buyers):
    arr = []
    for seller in sellers:
        arr.append(seller)
    arr1 = []
    for buyer in buyers:
        arr1.append(buyer)
    arr.sort(key=lambda x: x.t_valuation)
    arr1.sort(key=lambda x: x.t_valuation)
    b_index = 0
    s_index = 0
    while b_index < len(arr1) and s_index < len(arr):
        if arr1[b_index].t_valuation >= arr[s_index].t_valuation:
            part_b.append(arr1[b_index])
            part_s.append(arr[s_index])
            b_index = b_index + 1
            s_index = s_index + 1
        else:
            b_index = b_index + 1
    if len(part_b) != 0 and len(part_s) != 0:
        price = 0.5 * (part_s[len(part_s) - 1].t_valuation + part_b[len(part_b) - 1].t_valuation)
    else:
        price = 0
    return price    
b_regrets=[]
s_regrets=[]
# Function to run the auction for T iterations
def run_auction(sellers, buyers, T=9):
    for t in range(T):
        p = findprice(sellers, buyers)
        p1 = find_optimal_price(sellers, buyers)
        if p != 0:
            for i in range(len(part_s)):
                part_s[i].rp_seller = part_s[i].rp_seller + 1
                if t == 0:
                    part_s[i].avg_deal = p
                else:
                    part_s[i].avg_deal = (part_s[i].avg_deal * (part_s[i].rp_seller - 1) + p) / part_s[i].rp_seller
                part_s[i].c_valuation = updateval(t, part_s[i].rp_seller, part_s[i].avg_deal, part_s[i].alpha)
                f=p - p1 + random.random()
                part_s[i].regret = part_s[i].regret + f
                s_regrets.append(f)
            for i in range(len(part_b)):
                part_b[i].rp_buyer = part_b[i].rp_buyer + 1
                if t == 0:
                    part_b[i].avg_deal = p
                else:
                    part_b[i].avg_deal = (part_b[i].avg_deal * (part_b[i].rp_buyer - 1) + p) / part_b[i].rp_buyer
                part_b[i].c_valuation = b_updateval(t + 1, part_b[i].rp_buyer, part_b[i].avg_deal, part_b[i].alpha)
                f= p1 - p + random.random()
                part_b[i].regret = part_b[i].regret + f
                b_regrets.append(f)
        part_b.clear()
        part_s.clear()
#Seller and Buyer lists - we can modify and create specific seller and buyer attributes if we wish to
sellers = [Sellers(), Sellers(), Sellers(), Sellers(), Sellers(), Sellers(), Sellers()]
buyers = [Buyers(), Buyers(), Buyers(), Buyers(), Buyers(), Buyers(), Buyers()]
run_auction(sellers, buyers)
total_regret = 0
for i in range(N):
    total_regret = total_regret + sellers[i].regret + buyers[i].regret
print(total_regret)