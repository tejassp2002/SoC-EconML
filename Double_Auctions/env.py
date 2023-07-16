import numpy as np


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
            
        return buyer_rewards, seller_rewards, market_price 
            
    def auctioneer(self, buyer_bids, seller_asking_price):
        # use algorithm to determine the participanting buyers and sellers 
        # descending order of buyers and sellers by bids and asking price
        buyer_ids = np.argsort(buyer_bids)[::-1]
        seller_ids = np.argsort(seller_asking_price)[::-1]
        
        # find breakeven index
        breakeven_index = 0
        for i in range(self.num_buyers):
            if buyer_bids[buyer_ids[i]] < seller_asking_price[seller_ids[i]]:
                breakeven_index = i
                break
        
        participating_buyers = buyer_ids[:breakeven_index]
        participating_sellers = seller_ids[:breakeven_index]
        
        price = (buyer_bids[buyer_ids[breakeven_index-1]] + seller_asking_price[seller_ids[breakeven_index-1]]) / 2
        
        return participating_buyers, participating_sellers, price
        

def algorithm(horizon):
    double_auction = DoubleAuction(10, 10, 10*np.random.normal(0, 1, 10), 10*np.random.normal(0, 1, 10))
    buyer_rewards = np.zeros(10)
    seller_rewards = np.zeros(10)
    for i in range(horizon):
        # each buyer and seller bids and asks
        # this is designed by the algorithm (check paper)
        # No participant knows of their valuation apriori and learn it while repeatedly
        # participating in the market over T rounds.
        
        buyer_bids = # write code
        seller_asking_price = # write code
        
        b_reward, s_reward, market_price = double_auction.step(buyer_bids, seller_asking_price)
        
        buyer_rewards = np.add(buyer_rewards, b_reward)
        seller_rewards = np.add(seller_rewards, s_reward)
        
        # write code to calculate regret! 
        
        