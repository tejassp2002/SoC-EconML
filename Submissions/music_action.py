import numpy as np

class MusicRightsAuction():
    def __init__(self, num_buyers, num_sellers, true_valuation_buyers, true_valuation_sellers):
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        
        self.true_valuation_buyers = true_valuation_buyers
        self.true_valuation_sellers = true_valuation_sellers

        self.buyer_bids = np.random.rand(num_buyers) * true_valuation_buyers
        self.seller_asking_price = true_valuation_sellers + np.random.rand(num_sellers) * true_valuation_sellers 
        
    def step(self):
        participating_buyers, participating_sellers, market_price = self.auctioneer(self.buyer_bids, self.seller_asking_price)
        
        buyer_rewards = np.zeros(self.num_buyers)
        seller_rewards = np.zeros(self.num_sellers)
        
        for buyer in participating_buyers:
            buyer_rewards[buyer] = self.buyer_bids[buyer] - market_price + np.random.normal(0, 1)

        for seller in participating_sellers:
            seller_rewards[seller] = market_price - self.seller_asking_price[seller] + np.random.normal(0, 1)

        self.update_buyer(participating_buyers, buyer_rewards)
        self.update_seller(participating_sellers, seller_rewards)
        
        return len(participating_buyers), buyer_rewards, seller_rewards, market_price

    def update_buyer(self, participating_buyers, buyer_rewards):
        for buyer in range(self.num_buyers):
            if buyer in participating_buyers:
                self.true_valuation_buyers[buyer] -= 0.1 * buyer_rewards[buyer]
            else:
                self.true_valuation_buyers[buyer] *= 1.2

            if (self.buyer_bids[buyer] - buyer_rewards[buyer] * 0.2) < self.true_valuation_buyers[buyer]:
                self.buyer_bids[buyer] -= buyer_rewards[buyer] * 0.2
            else:
                self.buyer_bids[buyer] = self.true_valuation_buyers[buyer]

    def update_seller(self, participating_sellers, seller_rewards):
        for seller in range(self.num_sellers):
            if seller in participating_sellers:
                self.true_valuation_sellers[seller] += 0.1 * seller_rewards[seller]
            else:
                self.true_valuation_sellers[seller] *= 0.8
            
            if (self.seller_asking_price[seller] - seller_rewards[seller] * 0.2) > self.true_valuation_sellers[seller]:
                self.seller_asking_price[seller] -= seller_rewards[seller] * 0.2
            else:
                self.seller_asking_price[seller] = self.true_valuation_sellers[seller]

    def auctioneer(self, buyer_bids, seller_asking_price):
        buyer_ids = np.argsort(buyer_bids)[::-1]
        seller_ids = np.argsort(seller_asking_price)[::-1]

        breakeven_index = 0
        for i in range(min(self.num_buyers, self.num_sellers)):
            if buyer_bids[buyer_ids[i]] < seller_asking_price[seller_ids[i]]:
                breakeven_index = i
            else:
                break

        participating_buyers = buyer_ids[:breakeven_index]
        participating_sellers = seller_ids[:breakeven_index]
        
        price = (buyer_bids[buyer_ids[breakeven_index - 1]] + seller_asking_price[seller_ids[breakeven_index - 1]]) / 2

        return participating_buyers, participating_sellers, price

def music_rights_auction_simulation(horizon):
    num_buyers = 10
    num_sellers = 10
    true_valuation_buyers = abs(10 * np.random.normal(0, 1, num_buyers))
    true_valuation_sellers = abs(10 * np.random.normal(0, 1, num_sellers))
    
    music_auction = MusicRightsAuction(num_buyers, num_sellers, true_valuation_buyers, true_valuation_sellers)
    
    buyer_rewards = np.zeros(num_buyers)
    seller_rewards = np.zeros(num_sellers)
    regret = np.zeros(horizon)
    
    for i in range(horizon):
        participants, b_reward, s_reward, market_price = music_auction.step()
        
        buyer_rewards = np.add(buyer_rewards, b_reward)
        seller_rewards = np.add(seller_rewards, s_reward)
        
        buyer_valuations = music_auction.true_valuation_buyers
        seller_valuations = music_auction.true_valuation_sellers
        
        buyer_regret = np.dot(buyer_valuations - market_price, np.ones(num_buyers))
        seller_regret = np.dot(market_price - seller_valuations, np.ones(num_sellers))
        
        regret[i] = buyer_regret + seller_regret
        
        print("Round", i + 1)
        print("Participants:", participants)
        print("Buyer rewards:", buyer_rewards)
        print("Seller rewards:", seller_rewards)
        print("Market price:", market_price)
        print("Regret:", regret[i])
        print("---------------------------")
        
    return regret

music_rights_auction_simulation(10)
import numpy as np

class MusicRightsAuction():
    def __init__(self, num_buyers, num_sellers, true_valuation_buyers, true_valuation_sellers):
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        
        self.true_valuation_buyers = true_valuation_buyers
        self.true_valuation_sellers = true_valuation_sellers
        
    def step(self, buyer_bids, seller_asking_price):
        # use algorithm to determine the participanting buyers and sellers 
        participating_buyers, participating_sellers, market_price = self.auctioneer(buyer_bids, seller_asking_price)
        
        buyer_rewards = np.zeros(self.num_buyers)
        seller_rewards = np.zeros(self.num_sellers)
        
        for buyer in participating_buyers:
            buyer_rewards[buyer] = self.true_valuation_buyers[buyer] - market_price + np.random.normal(0, 1)
            
        for seller in participating_sellers:
            seller_rewards[seller] = market_price - self.true_valuation_sellers[seller] + np.random.normal(0, 1)
            
        return buyer_rewards, seller_rewards, market_price 
            
    def auctioneer(self, buyer_bids, seller_asking_price):
        # use algorithm to determine the participanting buyers and sellers 
        # descending order of buyers and sellers by bids and asking price
        buyer_ids = np.argsort(buyer_bids)[::-1]
        seller_ids = np.argsort(seller_asking_price)
        
        #  breakeven index
        breakeven_index = 0
        for i in range(self.num_buyers):
            if buyer_bids[buyer_ids[i]] < seller_asking_price[seller_ids[i]]:
                breakeven_index = i
                break
        
        participating_buyers = buyer_ids[:breakeven_index]
        participating_sellers = seller_ids[:breakeven_index]
        
        price = (buyer_bids[buyer_ids[breakeven_index-1]] + seller_asking_price[seller_ids[breakeven_index-1]]) / 2
        
        return participating_buyers, participating_sellers, price
        

def music_rights_auction_simulation(horizon):
    music_auction = MusicRightsAuction(10, 10, 10*np.random.normal(0, 1, 10), 10*np.random.normal(0, 1, 10))
    buyer_rewards = np.zeros(10)
    seller_rewards = np.zeros(10)
    regret = np.zeros(horizon)
    
    # Table 
    works_data = [
        {"title": "Four Jolly Smiths", "composer": "Henry Leslie", "prices": [(1868, 5.25), (1889, 265), (1892, 261), (1895, 182.7), (1896, 156.8)]},
        {"title": "Fairy Barque", "composer": "W. Smallwood", "prices": [(1891, 1008), (1896, 1810.50), (1904, 1424.50), (1912, 730), (1931, 494)]}
    ]
    
    for i in range(horizon):
       
        buyer_bids = np.random.rand(10) * music_auction.true_valuation_buyers
        seller_asking_price = music_auction.true_valuation_sellers + np.random.rand(10) * music_auction.true_valuation_sellers
        
        b_reward, s_reward, market_price = music_auction.step(buyer_bids, seller_asking_price)
        
        buyer_rewards = np.add(buyer_rewards, b_reward)
        seller_rewards = np.add(seller_rewards, s_reward)
        
        # regret 
        buyer_valuations = music_auction.true_valuation_buyers
        seller_valuations = music_auction.true_valuation_sellers
        
        buyer_regret = np.dot(buyer_valuations - market_price, np.ones(10))
        seller_regret = np.dot(market_price - seller_valuations, np.ones(10))
        
        regret[i] = buyer_regret + seller_regret
        
        print("Round", i + 1)
        print("Participants:", len(buyer_bids), "buyers,", len(seller_asking_price), "sellers")
        print("Buyer rewards:", buyer_rewards)
        print("Seller rewards:", seller_rewards)
        print("Market price:", market_price)
        print("Regret:", regret[i])
        print("---------------------------")
        
       
    return regret


music_rights_auction_simulation(10)
