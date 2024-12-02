import random
import matplotlib.pyplot as plt

class StockExchange:
    def __init__(self, num_buyers, num_sellers, market_sentiment):
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        self.buyers = []
        self.sellers = []
        self.trading_prices = {}
        self.rewards = []
        self.stock_prices = {}
        self.market_sentiment = market_sentiment

    def add_buyer(self, buyer):
        self.buyers.append(buyer)
    
    def add_seller(self, seller):
        self.sellers.append(seller)
    
    def set_stock_prices(self, stock_prices):
        self.stock_prices = stock_prices
    
    def run_auction(self, num_rounds):
        for t in range(num_rounds):
            sorted_buyer_bids = sorted(self.buyers, key=lambda x: x.estimate, reverse = True)
            sorted_seller_bids = sorted(self.sellers, key = lambda x: x.estimate)
            sorted_buyer_bids = [x for x in sorted_buyer_bids if x.participating]
            sorted_seller_bids = [y for y in sorted_seller_bids if y.participating]
            K=0
            
            while K<min(len(sorted_buyer_bids),len(sorted_seller_bids)) and sorted_buyer_bids[K].estimate >= sorted_seller_bids[K].estimate:
                K+=1

            participating_buyers = sorted_buyer_bids[:K]
            participating_sellers = sorted_seller_bids[:K]
            trading_prices = {}
            
            for stock, price in self.stock_prices.items():
                trading_price = (participating_buyers[-1].estimate + participating_sellers[-1].estimate)/2
                trading_prices[stock] = trading_price
            self.trading_prices[t] = trading_prices

            for buyer in participating_buyers:
                if t>10 and buyer.long_only == False:
                    buyer.participating = False
                if market_sentiment[t]:
                    buyer.target += 2
                    buyer.stoploss -= 2
                else:
                    buyer.target -=2
                    buyer.stoploss += 2
                if buyer.target<trading_prices[buyer.stock] or buyer.stoploss > trading_prices[buyer.stock]:
                    buyer.participating = False
            sum=0
            for buyer, seller in zip(participating_buyers, participating_sellers):
            
                if buyer.stock == seller.stock:
                    buyer.utility.append(buyer.estimate + buyer.random_variable-trading_prices[buyer.stock])
                    seller.utility.append(trading_prices[seller.stock]-seller.estimate + seller.random_variable)
                    sum += (buyer.estimate + buyer.random_variable-trading_prices[buyer.stock] + trading_prices[seller.stock]-seller.estimate + seller.random_variable)
            self.rewards.append(sum)
                    




    def print_results(self):
        print("Trading Prices:")
        for t, trading_prices in self.trading_prices.items():
            print("Round", t+1)
            for stock, price in trading_prices.items():
                print("Stock:", stock, "Trading Price:", price)
        print("Buyers:")
        for buyer in self.buyers:
            print("Buyer:", buyer.id, "Stock:", buyer.stock, "Utility:", buyer.utility)
        print("Sellers:")
        for seller in self.sellers:
            print("Seller:", seller.id, "Stock:", seller.stock, "Utility:", seller.utility)
        

class Participant:
    def __init__(self, id, type, participating, cash_in_hand, stock, estimate, stock_quantity, random_variable, long_only, target, stoploss):
        self.id = id
        self.type = type
        self.participating = participating
        self.cash_in_hand = cash_in_hand
        self.stock = stock
        self.estimate = estimate
        self.stock_quantity = stock_quantity
        self.random_variable = random_variable
        self.long_only = long_only
        self.bid = None
        self.utility = []
        self.target = target
        self.stoploss = stoploss


market_sentiment = [True, True, False, False, False, True, False, True, True, True, True, False, False, False, False, False, True, True, True, True, False, True, True, False, True, False, True, True, False, False]

exchange = StockExchange(7, 8, market_sentiment)

random_variable = random.gauss(0,1)

buyer1 = Participant(1, "buyer", True, 1000,  "Stock A", 110, 5, random_variable, False, 120, 105)
buyer2 = Participant(2, "buyer", True, 1500, "Stock A", 120, 10, random_variable, True, 130, 95)
buyer3 = Participant(3, "buyer", True, 700, "Stock A", 115, 5, random_variable, False, 125, 100)
buyer4 = Participant(4, "buyer", True, 1000, "Stock A", 90, 15, random_variable, True, 100, 85)
buyer5 = Participant(5, "buyer", True, 900, "Stock A", 130, 5, random_variable, False, 140, 110)
buyer6 = Participant(6, "buyer", True, 1300, "Stock A", 110, 10, random_variable, True, 120, 90)
buyer7 = Participant(7, "buyer", True, 1000, "Stock A", 105, 7, random_variable, False, 120, 95)

seller1 = Participant(1, "seller", True, 500, "Stock A", 100, 15, random_variable, True, 110, 90)
seller2 = Participant(2, "seller", True, 600, "Stock A", 110, 5, random_variable, True, 110, 90)
seller3 = Participant(3, "seller", True, 500, "Stock A", 115, 5, random_variable, True, 110, 90)
seller4 = Participant(4, "seller", True, 700, "Stock A", 93, 25, random_variable, True, 110, 90)
seller5 = Participant(5, "seller", True, 500, "Stock A", 105, 5, random_variable, True, 110, 90)
seller6 = Participant(6, "seller", True, 500, "Stock A", 98, 15, random_variable, True, 110, 90)
seller7 = Participant(7, "seller", True, 900, "Stock A", 120, 5, random_variable, True, 110, 90)
seller8 = Participant(8, "seller", True, 500, "Stock A", 110, 5, random_variable, True, 110, 90)

exchange.add_buyer(buyer1)
exchange.add_buyer(buyer2)
exchange.add_buyer(buyer3)
exchange.add_buyer(buyer4)
exchange.add_buyer(buyer5)
exchange.add_buyer(buyer6)
exchange.add_buyer(buyer7)

exchange.add_seller(seller1)
exchange.add_seller(seller2)
exchange.add_seller(seller3)
exchange.add_seller(seller4)
exchange.add_seller(seller5)
exchange.add_seller(seller6)
exchange.add_seller(seller7)
exchange.add_seller(seller8)

stock_prices = {"Stock A": 100.0}
exchange.set_stock_prices(stock_prices)

T = 30
exchange.run_auction(T)

exchange.print_results()

plt.figure(figsize=(12, 4))

y_values = [price for trading_prices in exchange.trading_prices.values() for price in trading_prices.values()]
plt.subplot(1,3,1)
plt.plot(range(T), y_values)
plt.xlabel("Round")
plt.ylabel("Trading Price")
plt.title("Trading Prices over Rounds")

plt.subplot(1,3,2)
plt.plot(range(T), exchange.rewards)
plt.xlabel("Round")
plt.ylabel("Reward")
plt.title("Rewards earned by the model over rounds")

plt.subplot(1,3,3)
plt.plot(range(T), market_sentiment)
plt.xlabel("Round")
plt.ylabel("Market Benchmark")
plt.title("Behaviour of Market over time")

plt.tight_layout()
plt.show()