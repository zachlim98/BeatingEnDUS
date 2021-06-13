# BeatingEnDUS

## Introduction
The whole idea behind this repo started when someone showed me the returns from a particular robo-investing company in Singapore (hint: the name of the repo) and I started thinking of ways that I could beat their returns. There are different code sections within this repo that deal with different ways that I've experimented with (some more successfully than others).

## Account Tracking
How can we compare returns if we don't even know how our account has changed? Account Tracking attempts to use the TDAmeritrade API (in both Python and R) to track my account. Unlike Robinhood, there is no dedicated way for TDAmeritrade asers to see their account balance since the start of their account and this was hence a way to try to replicate that. I tried many methods for this including:
- Pulling account history using the TDA API
- Using Selenium to login to my TDA account history online and pulling the records 
- Simply using the manual records that I had kept (in Excel gasp!) and trying to change them into something usable

Each produced different results so feel free to try it out. 

## Backtesting
This was just a WHOLE folder of backtesting fun using **bt** and **backtester** - two popular backtesting libraries on Python. A whole host of different strategies that were designed to be minimial and easy to run (and hopefully beating the returns from the aforementioned robo-advisor)

## iFAST
Another investment company and my attempt to track my PnL using webscraping from a client's account (with permission)

## Screeners
The IBD50 is an amazing ETF that tracks the top 50 stocks in the market according to their analysis. It usually costs money but using a scraper, we can easily access the IBD50 list here. 

## Portfolio Simulation
This simulation was different from the Backtesting one in that it was aimed more at simulations of future portfolio returns (under the FIRE principle). 

## SPY Works
My experiments with using SPY options (which has since been moved to the new repo call Optiks since it involves more backtesting now). 

