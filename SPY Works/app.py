import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd 
import yfinance as yf
import plotly.express as px

# import SPY data for plotting


# prepare the app for plotting
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("This is an app"),
    dcc.Input(id="input", type="text"),
    html.Br(),
    html.Div(id="outputs"),
    dcc.Graph(id='example')])

@app.callback(
    Output("outputs", "children"),
    Output('example', 'figure'),
    Input("input", "value"))
def return_value(value):
    ticker = value
    SPY =yf.download(ticker)
    SPY['Adj Close'] = SPY['Adj Close'].pct_change()*100
    SPY.reset_index(inplace=True)
    SPY['Date_str'] = SPY['Date'].astype(str)
    fig = px.violin(SPY.reset_index(), x = 'Adj Close', orientation='h')
    return(value, fig)

if __name__ == '__main__':
    app.run_server(debug=True) 
