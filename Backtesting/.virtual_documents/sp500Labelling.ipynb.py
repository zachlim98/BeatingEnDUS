import pandas as pd
import numpy as np
from tiingo import TiingoClient

client = TiingoClient({'api_key' : '9c884b918420c9220dcf832c83a6ba8025711e1e'})


datalist = ['A', 'AABA', 'AAL', 'AAMRQ', 'AAP']

start_date = '2000-01-01'
end_date = '2020-12-05'


# spy_data = client.get_dataframe("SPY",
#                                     frequency='daily',
#                                     startDate=start_date,
#                                     endDate=end_date)

# spy_data = spy_data.tz_convert(None)
# dfdates = pd.DataFrame(index=spy_data.index)

# for i in range(len(datalist)):
#     try:
#         data = client.get_dataframe(datalist[i],
#                                             frequency='daily',
#                                             startDate=start_date,
#                                             endDate=end_date)

#         data = data.tz_convert(None)
#         data2 = dfdates.join(data, how='left').fillna(0)
#         data3 = data2.join(sphist, how='left').fillna(method='ffill')
#         data3['inSPY'] = 0
#         for t in range(len(data3)):
#             if datalist[i] in (data3['tickers'][t]):
#                 data3['inSPY'][t] = 1
#             else:
#                 data3['inSPY'][t] = 0
#         data3.drop('tickers',axis=1).to_csv("data/{}.csv".format(datalist[i]))
#         print(f"{i}/{len(datalist)} finished")
        
#     except:
#         print(f'{datalist[i]} not found')


sp500hist = pd.read_csv("sp500_hist.csv")


sphist = sp500hist.set_index(sp500hist['date']).drop('date', axis=1)


import datetime as datetime


index = pd.date_range(start='2000-1-1',end='2020-1-6')
columns = ['A']


spy_data = client.get_dataframe("SPY",
                                    frequency='daily',
                                    startDate=start_date,
                                    endDate=end_date)

spy_data = spy_data.tz_convert(None)
blank = pd.DataFrame(index=spy_data.index)


sphist = blank.join(sphist, how='left').fillna(method='ffill')


everwas = []

for i in range(len(sphist)):
    x = sphist.iloc[i,0].split(',')
    everwas = sorted(np.unique(everwas + x))


splitno = int((len(everwas)/3))

everwas1 = everwas[:splitno]
everwas2 = everwas[(splitno):(splitno*2)]
everwas3 = everwas[(splitno*2):]


len(everwas)


datalist = ["SPY", "VEU", "BIL", "AGG"]


start_date = '2000-01-01'
end_date = '2020-12-05'

spy_data = client.get_dataframe("SPY",
                                    frequency='daily',
                                    startDate=start_date,
                                    endDate=end_date)

spy_data = spy_data.tz_convert(None)
dfdates = pd.DataFrame(index=spy_data.index)

for i in range(len(datalist)):
    try:
        data = client.get_dataframe(datalist[i],
                                            frequency='daily',
                                            startDate=start_date,
                                            endDate=end_date)

        data = data.tz_convert(None)
        data2 = dfdates.join(data, how='left').fillna(0)
        data3 = data2.join(sphist, how='left').fillna(method='ffill')
        data3['inSPY'] = 0
        for t in range(len(data3)):
            if datalist[i] in (data3['tickers'][t]):
                data3['inSPY'][t] = 1
            else:
                data3['inSPY'][t] = 0
        data3.drop('tickers',axis=1).to_csv("data/ETFs/{}.csv".format(datalist[i]))
        print(f"{i}/{len(datalist)} finished")
    except:
        print(f"{datalist[i]} was not found")



