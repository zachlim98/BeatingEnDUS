import dash
from dash_bootstrap_components._components.Jumbotron import Jumbotron
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
fig = px.line(df, x="Date", y="AAPL.Close")

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Jumbotron([html.H1("Choose your parameters", className="display-3")]),
            html.Br()
        ], width={"size":8})
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id="slide-time",
                min=0,
                max=60,
                step=5,
                value=50,
                dots=True
            ),
            html.P(id="time-output", style={"fontSize":50}),
            html.Br(),
            dcc.Slider(
                id="slide-risk",
                min=1,
                max=10,
                step=1,
                value=5,
                dots=True
            ),
            html.P(id="risk-output", style={"fontSize":50}),
        ], width={"size":6})
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            dbc.Jumbotron([html.P("Given these parameters, our recommended portfolio for you is:"),
                        html.P("MySyfe", style={"color": "#0384fc", "textAlign":"center" , "font-size":40}),
            html.P("SAFE",  style={"color": "#fc8403", "textAlign":"center" , "font-size":50})], className="display-4"),
                    dcc.Markdown("Performance over the last **10 years**", 
        style={"textAlign":"center" , "font-size":40, "background-color":"lightpurple"}),
        ], width={"size":8})
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            html.P("Annual Return: 6%", style={"textAlign":"center" , "font-size":40, "background-color":"powderblue"})
        ]),
        dbc.Col([
            html.P("Sharpe Ratio: 1.23", style={"textAlign":"center" , "font-size":40, "background-color":"powderblue"})
        ])
    ]),

    dbc.Row([
        dbc.Col([dcc.Graph(id="graph1", figure=fig)])
    ])
])

@app.callback(
    Output('time-output', 'children'),
    Output('risk-output', 'children'),
    Input('slide-time', 'value'),
    Input('slide-risk', 'value')
)
def update_slider(time, risk):
    return "You want to invest for {} years".format(time), "You have a risk value of {}".format(risk)

if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", debug=False)