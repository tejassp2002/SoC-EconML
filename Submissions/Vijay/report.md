## Double Auctions with Learning for Energy Markets

### Introduction
We implement a double auction system for energy markets, in which neither the buyers or sellers know their true valuations but attempt to find over an iterative process.

### Code Overview
 The code defines two classes, Sellers and Buyers, representing sellers and buyers in the auction. Each seller and buyer has attributes such as true valuation, current valuation, number of rounds participated, average deal, learning rate ( alpha ), and regret.

### Valuation Calculation
We determine the factors that are of pertinence to participants when participating in energy markets. The true valuation of each seller and buyer is calculated using a weighted sum of contract length, volume, flexibility of payment, renewable energy availabilty, and market conditions. 
The weights are randomly assigned to simulate different preferences among participants.

### Price Determination
The partcipants not knowing their true valuations, first bid at random. We implement a matching algorithm which determines the participants in the market. 
The average price mechanism determines the price of the trade at each round.
### Regret Calculation
The regret of each seller and buyer is calculated based on the difference between the optimal deal price and the optimal price. The regret is updated after each iteration of the auction.
The optimal price is defined as the price when each buyer and seller would've known and bid the true valuation.
### Running the Auction
The auction system is run for a specified number of iterations (we set the default to 9). The `run_auction()` function performs the auction, updating sellers' and buyers' valuations, round participation, and regrets.
After each round, the buyers and sellers update their bids according to confidence-bound algorithms post-feedback from the previous round, attempting to discover the true valuation.

### Conclusion
This auction system simulates the bidding process for energy contracts. It takes into account participants' preferences and the learning done post each round. 
We could tailor this specifically to more areas by concretizing the method through which the true valuation is determined. Feel free to experiment with the code.

For any questions or suggestions, please don't hesitate to reach out.

Happy auctioning!
