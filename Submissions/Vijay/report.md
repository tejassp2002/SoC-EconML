## Double Auctions with Learning for Energy Markets

### Introduction
We implement a double auction system for energy markets, in which neither the buyers nor sellers know their true valuations but attempt to find them through an iterative process.
## Task 1: Determination of True Valuation of Buyers and Sellers in Energy Markets
We determine the factors that are of pertinence to participants when participating in energy markets. The true valuation of each seller and buyer is calculated using a weighted sum of contract length, volume, flexibility of payment, renewable energy availability, and market conditions. 
The weights are randomly assigned to simulate different preferences among participants.

An illustration is: Smaller companies, both sellers and buyers, would be more influenced by factors such as market conditions and flexibility of payment, however larger companies would care more about renewable energy availability and contract length.

## Task 2: Simulation of the auction using LCB and UCB estimates
1) The code defines two classes, Sellers and Buyers, representing sellers and buyers in the auction. Each seller and buyer has attributes such as true valuation, current valuation, number of rounds participated, average deal, learning rate ( alpha ), and regret.
2) Not knowing their true valuations, the participants' first bid at random. We implement a matching algorithm that determines the participants in the market. The average price mechanism determines the price of the trade at each round.
3) The regret of each seller and buyer is calculated based on the difference between the optimal deal price and the optimal price. The regret is updated after each iteration of the auction.
The optimal price is defined as the price when each buyer and seller would've known and bid the true valuation.
4) The auction system is run for a specified number of iterations (we set the default to 9). The run_auction() function performs the auction, updating sellers' and buyers' valuations, round participation, and regrets.
After each round, the buyers and sellers update their bids according to confidence-bound algorithms post-feedback from the previous round, attempting to discover the true valuation.
