from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# import login details
infile = open("login_dets",'rb')
info = pickle.load(infile)
infile.close()

# create function to retrieve table
def parse_html_table(table):
            n_columns = 0
            n_rows=0
            column_names = []
    
            # Find number of rows and columns
            # we also find the column titles if we can
            for row in table.find_all('tr'):
                
                # Determine the number of rows in the table
                td_tags = row.find_all('td')
                if len(td_tags) > 0:
                    n_rows+=1
                    if n_columns == 0:
                        # Set the number of columns for our table
                        n_columns = len(td_tags)
                        
                # Handle column names if we find them
                th_tags = row.find_all('th') 
                if len(th_tags) > 0 and len(column_names) == 0:
                    for th in th_tags:
                        column_names.append(th.get_text())
    
            # Safeguard on Column Titles
            if len(column_names) > 0 and len(column_names) != n_columns:
                raise Exception("Column titles do not match the number of columns")
    
            columns = column_names if len(column_names) > 0 else range(0,n_columns)
            df = pd.DataFrame(columns = columns,
                              index= range(0,n_rows))
            row_marker = 0
            for row in table.find_all('tr'):
                column_marker = 0
                columns = row.find_all('td')
                for column in columns:
                    df.iat[row_marker,column_marker] = column.get_text()
                    column_marker += 1
                if len(columns) > 0:
                    row_marker += 1
                    
            # Convert to float if possible
            for col in df:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass
            
            return df

# create driver to access tdameritrade
driver = webdriver.Chrome()

driver.get(r"https://invest.tdameritrade.com.sg/tdaa/index.html#!/accountLobby/statements/confirms")

# wait for all javascript elements to load
driver.implicitly_wait(20)

# input login details and access account page
email_box = driver.find_element_by_xpath(R'//*[@id="username"]')
email_box.send_keys(info["username"])

password_box = driver.find_element_by_xpath('//*[@id="password"]')
password_box.send_keys(info["password"])

login = driver.find_element_by_xpath('//*[@id="loginForm"]')
login.click()

account = driver.find_element_by_xpath('//*[@id="accountCode"]/option[2]')
account.click()

account_btn = driver.find_element_by_xpath('//*[@id="tradeConfirmationSearchForm"]')
account_btn.click()

# retrieve html info
tags = driver.find_element_by_class_name('account-summary-table')
html = tags.get_attribute('innerHTML')
soup = BeautifulSoup(html, "html.parser")

# Retrive table
transc_df = parse_html_table(soup)
transc_df["Net Amt"] = transc_df["Net Amt"].str.replace(",","").astype(float)
# convert those there were sold to negative amounts
transc_df["amt"] = np.where(transc_df["B/S"] == '   Sold  ', transc_df["Net Amt"] , -transc_df["Net Amt"])

# create p/l dataframe, grouping by the symbol and using agg to retain date
pl_df = transc_df.groupby(['Symbol']).agg({'amt': ['sum', 'count'], 'Date': 'last'}).reset_index()
# split it up to get unique dates so we can group again later
pl_df[["ticker", "Month", "Day", "Year", "Strike", "Type"]] = pl_df["Symbol"].str.split(' ', 0, expand=True).dropna().iloc[:,3:9]
pl_df["Exp"] = pl_df["Month"] + pl_df["Day"] + pl_df["Year"]

# rename the columns after flattening the multiindex hierarchy
pl_df.columns = pl_df.columns.get_level_values(0)
pl_df.columns = ['Symbol', 'value', 'count', 'Date', 'ticker', 'Month', 'Day', 'Year',
       'Strike', 'Type', 'Exp']

# create new df and group by exp
plexp_df = pl_df[pl_df["count"] >= 2].groupby(['ticker','Exp']).agg({'value' : 'sum', "Date" : 'last'})
# sort by date
plexp_df["Date"] = pd.to_datetime(plexp_df["Date"])
# create plotting dataframe
plot_df = plexp_df.sort_values("Date").groupby("Date").agg({'value': 'sum'}).reset_index().set_index("Date")

# create a plot
ax = (plot_df["value"]+4998).plot(linewidth=1.5, color="red")
ax.set_ylabel("Account Value")
plt.savefig("funk.png")