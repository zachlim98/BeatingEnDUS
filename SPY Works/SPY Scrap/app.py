from tda import auth, client
import selenium
import json
import datetime
import pandas as pd
 
# boilerplate to load account
token_path = R'.\token.pickle'
api_key = 'DRSMU4TL964FO3QNBQHVL78X9SUPGGIL@AMER.OAUTHAP'
redirect_uri = "http://localhost"
try:
    c = auth.client_from_token_file(token_path, api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, api_key, redirect_uri, token_path)

print("1. Account Loaded...")

# finding options chains
para = c.Options
chains = c.get_option_chain(symbol="SPY", 
    contract_type=para.ContractType.PUT, 
    to_date=datetime.date.today() + datetime.timedelta(weeks=1))
initial = pd.json_normalize(chains.json())

# explode the json to get the table of options
explode = []
for i in initial.columns:
    try: 
        explode.append(pd.json_normalize(initial[i].explode()))
    except:
        pass
complete = pd.concat(explode)

print("2. Option Chain Pulled...")

# select the option closes to 6 delta with a 3 DTE
delta = 0.06
dte = 4
complete["delta"] = complete["delta"].astype('float')
complete.reset_index(inplace=True)
idx = complete[complete["daysToExpiration"] == dte]["delta"].add(delta).abs().idxmin()

# build the short strike first 
short_strike = dict(
    symbol=complete.iloc[[idx]]["symbol"],
    strike=complete.iloc[[idx]]["strikePrice"],
    delta=complete.iloc[[idx]]["delta"],
    bid=complete.iloc[[idx]]["bid"],
    expd=complete.iloc[[idx]]["expirationDate"],
)

from tda.orders.options import OptionSymbol

# get all the info for the long strike then build the long strike dict next
ls_strike = str(int((short_strike["strike"]-10)))
ls_symbol = OptionSymbol('SPY', datetime.datetime.fromtimestamp(float(short_strike["expd"])/1000, 
tz=datetime.timezone(datetime.timedelta(0))), 'P', ls_strike).build()
ls_ask = c.get_quote(ls_symbol).json()[ls_symbol]['askPrice']
ls_delta = c.get_quote(ls_symbol).json()[ls_symbol]['delta']

long_strike = dict(
    symbol=ls_symbol, 
    strike=ls_strike,
    ask = ls_ask,
    delta= ls_delta,
)

print("3. Strikes Built...")

from tda.orders.options import bull_put_vertical_open

# place the order from a bull put vertical, using the information from the 
c.place_order(220535376, bull_put_vertical_open(str(long_strike["symbol"]), 
short_strike["symbol"].iloc[0], 1, round(float(short_strike["bid"]-long_strike["ask"]),2)).build())

print("4. Order Sent!")
