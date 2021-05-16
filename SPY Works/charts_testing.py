##
import numpy as np
print("Hello")

np.random.binomial(100, p=0.7, size=10)
##

##
import pandas as pd
from sklearn import datasets 
import matplotlib.pyplot as plt
%matplotlib

iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)

import plotly.express as px 

fig = px.scatter(x=[0,1,2,3,4], y=[0,1,4,9,16])
df.head()
##

##
import yfinance as yf

spy_data = yf.download('SPY')
spy_data.head()

fig = px.scatter(spy_data, y='Close', x=spy_data.index)
fig.show()
##
