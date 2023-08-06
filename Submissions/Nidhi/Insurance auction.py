import random

class Purchase:
    def _init_(self, buyer_id, price, quantity):
        self.buyer_id = buyer_id
        self.price = price
        self.quantity = quantity

def double_auction(buyers_list, sellers_list):
    trades = []
    
    buyer_index = 0
    while buyer_index < len(buyers_list):
        seller_index = 0
        while seller_index < len(sellers_list):
            buyer = buyers_list[buyer_index]
            seller = sellers_list[seller_index]
            
            if seller.price <= buyer.price:
                trade_quantity = min(buyer.quantity, seller.quantity)
                
                if trade_quantity > 0:
                    trades.append((buyer.buyer_id, seller.seller_id, buyer.price, trade_quantity))
                    buyer.quantity -= trade_quantity
                    seller.quantity -= trade_quantity
                    if buyer.quantity == 0:
                        break
                
            seller_index += 1
        
        buyer_index += 1
    
    return trades

# Generate some random buyers and sellers for demonstration
buyers = [Purchase('B' + str(i), random.uniform(1, 10), random.randint(1, 10)) for i in range(1, 11)]
sellers = [Purchase('S' + str(i), random.uniform(5, 15), random.randint(1, 10)) for i in range(1, 11)]

# Simulate the double auction
trades = double_auction(buyers, sellers)

# Print the trades
print("Trades:")
for buyer_id, seller_id, price, quantity in trades:
    print(f"Buyer: {buyer_id} | Seller: {seller_id} | Price: {price} | Quantity: {quantity}")