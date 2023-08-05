import math
import numpy as np
from math import log
from matplotlib import pyplot as plt

def Buyers_valuation(luxury,urgency,tour_length, time):
  bid= 24*tour_length + np.random.uniform(0,10)
  if luxury==True:
    bid+=50
  if urgency==True:
    bid+=40
  if time in [8,11] or time in [16.5,19.5]:
    bid+=70
  else:
    bid+=20

  # bid+= np.random.uniform(0,20)
  return bid

def Sellers_valuation(car_type, time, tour_length):
  if car_type == 'mini':
    bid= 20*tour_length + np.random.uniform(0,10)
  elif car_type == 'prime sedan':
    bid= 24*tour_length + np.random.uniform(0,10)
  elif car_type == 'prime SUV':
    bid= 29*tour_length + np.random.uniform(0,10)

  if time in [8,11] or time in [16.5,19.5]:
    bid+=70
  elif time in [0,4]:
    bid+=110
  else:
    bid+=20

  # bid+= np.random.uniform(0,20)
  return bid

class DoubleAuction():
    def __init__(self, num_buyers, num_sellers, true_valuation_buyers, true_valuation_sellers):
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers

        self.true_valuation_buyers = true_valuation_buyers
        self.true_valuation_sellers = true_valuation_sellers

    def step(self, buyer_bids, seller_asking_price):
        # use algorithm to determine the participanting buyers and sellers
        particating_buyers, participating_sellers, market_price = self.auctioneer(buyer_bids, seller_asking_price)

        buyer_rewards = np.zeros(self.num_buyers)
        seller_rewards = np.zeros(self.num_sellers)

        for buyer in particating_buyers:
            buyer_rewards[buyer] = self.true_valuation_buyers[buyer] - market_price + np.random.normal(0, 1)

        for seller in participating_sellers:
            seller_rewards[seller] = market_price - self.true_valuation_sellers[seller] + np.random.normal(0, 1)

        # print(self.true_valuation_buyers)
        # print(self.true_valuation_sellers)
        # print(market_price,buyer_rewards,seller_rewards)
        return buyer_rewards, seller_rewards, market_price , participating_sellers , particating_buyers

    def auctioneer(self, buyer_bids, seller_asking_price):
        # use algorithm to determine the participanting buyers and sellers
        # descending order of buyers and sellers by bids and asking price
        buyer_ids = np.argsort(buyer_bids)[::-1]
        seller_ids = np.argsort(seller_asking_price)


        # find breakeven index
        breakeven_index = 0
        for i in reversed(range(min(self.num_buyers,self.num_sellers))):
            if buyer_bids[buyer_ids[i]] <= seller_asking_price[seller_ids[i]]:
                breakeven_index = i
                break

        participating_buyers = buyer_ids[:breakeven_index]
        participating_sellers = seller_ids[:breakeven_index]

        price = (buyer_bids[buyer_ids[breakeven_index - 1]] + seller_asking_price[seller_ids[breakeven_index - 1]]) / 2

        return participating_buyers, participating_sellers, price


def algorithm(horizon,N=5,M=4):
    buyers_valuation = []
    sellers_valuation=[]

    for i in range(N):
      buyers_valuation.append(Buyers_valuation(np.random.choice([True,False]),np.random.choice([True,False]),np.random.uniform(0,15), np.random.uniform(0,24)))
    for i in range(M):
      sellers_valuation.append(Sellers_valuation(np.random.choice(['mini','prime sedan','prime SUV']), np.random.uniform(0,24), np.random.uniform(0,15)))

    # buyers_valuation=[40,30,20,5,2]
    # sellers_valuation=[2,3,4,7]

    for i in range(N):
      buyers_valuation[i] = buyers_valuation[i]/max(buyers_valuation)
    for i in range(M):
      sellers_valuation[i] = sellers_valuation[i]/max(sellers_valuation)

    double_auction = DoubleAuction(N, M, buyers_valuation,sellers_valuation ) # change this, take input from part 1 valuations
    buyer_rewards = np.zeros(N)
    seller_rewards = np.zeros(M)
    n_buyer = np.zeros(N)+1
    n_seller = np.zeros(M)+1
    average_buyer_reward = np.zeros(N)
    average_seller_reward = np.zeros(M)

    buyer_bids = np.zeros(N)
    seller_asking_price = np.zeros(M)
    _, _, _,participating_sellers, participating_buyers = double_auction.step(double_auction.true_valuation_buyers, double_auction.true_valuation_sellers)
    social_welfare_regret = 0
    for i in participating_buyers:
        social_welfare_regret += double_auction.true_valuation_buyers[i]

    for i in range(M):
      if i not in participating_sellers:
        social_welfare_regret += double_auction.true_valuation_sellers[i]

    social_welfare_regret = social_welfare_regret*horizon


    for round in range(1,horizon):
        # each buyer and seller bids and asks
        # this is designed by the algorithm (check paper)
        # No participant knows of their valuation apriori and learn it while repeatedly
        # participating in the market over T rounds.


        for j in range(N):
            buyer_bids[j] =  average_buyer_reward[j]+math.sqrt(8*log(round)/n_buyer[j])# write code
        for k in range(M):
            seller_asking_price[k] =  average_seller_reward[k]-math.sqrt(8*log(round)/n_seller[k]) # write code

        if round==1:
            buyer_bids = np.zeros(N)
            seller_asking_price = np.zeros(M)

        b_reward, s_reward, market_price, participating_sellers, participating_buyers = double_auction.step(buyer_bids, seller_asking_price)
        # print(b_reward,s_reward,market_price)

        # for i in participating_buyers:
        #   b_reward[i] = b_reward[i]+market_price
        # for i in participating_sellers:
        #   s_reward[i] = market_price-s_reward[i]

        b_reward = b_reward+market_price
        s_reward = market_price-s_reward

        # print(participating_sellers,participating_buyers,b_reward,s_reward)
        buyer_rewards = np.add(buyer_rewards, b_reward)
        seller_rewards = np.add(seller_rewards, s_reward)
        for i in participating_buyers:
            n_buyer[i]+=1
        for i in participating_sellers:
            n_seller[i]+=1
        for i in range(N):
            average_buyer_reward[i] = buyer_rewards[i]/n_buyer[i]
        for i in range(M):
            average_seller_reward[i] = seller_rewards[i]/n_seller[i]

        # print(average_buyer_reward,average_seller_reward)

        # print(participating_buyers,participating_sellers)
        for i in participating_buyers:
            social_welfare_regret -= double_auction.true_valuation_buyers[i]

        for i in range(M):
          if i not in participating_sellers:
            social_welfare_regret -= double_auction.true_valuation_sellers[i]
        # write code to calculate regret!

    return social_welfare_regret


if __name__ == "__main__":
    horizons = np.linspace(100,1000,100)
    # horizons = [100]
    regrets = []
    for horizon in horizons:
        regret = algorithm(int(horizon),15,12)
        # print(regret)
        regrets.append(regret)
        
    plt.plot(horizons,regrets)
    plt.show()
