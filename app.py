import pandas as pd
import pandas_datareader as pdr
import numpy as np
import plotly.graph_objs as go
from utils import compute_bollinger
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # Add State later

# Set dates
start_date = pd.datetime(2018,1,1)
end_date = pd.datetime.today()

# Cryptocurrencies data
cryptos = pd.read_csv('data/cryptos.csv')

# Get Bitcoin data
btc = pdr.get_data_yahoo('BTC-USD', start_date, end_date)

# Save the open price
btc_open = btc['Open']

# Set window size and number of standard deviations (can make an input later!)
window_size = 5
no_std_devs = 2

# Empirical mean and standard deviation
btc_mean = btc_open.rolling(window_size).mean()
btc_std = btc_open.rolling(window_size).std()

# Calculate the Bollinger bands
bollinger_low = btc_mean - (btc_std*no_std_devs)
bollinger_high = btc_mean + (btc_std*no_std_devs)

# Create graph object
trace1 = go.Scatter(x=btc_open.index, y = btc_open,
                  mode='lines', name='BTC-USD')
trace2 = go.Scatter(x=btc_open.index, y = bollinger_low,
                  line=dict(dash='dash'), name='Bollinger Low')
trace3 = go.Scatter(x=btc_open.index, y = bollinger_high,
                  line=dict(dash='dash'), name='Bollinger High')

# Save figures and set layout
data = [trace1, trace2, trace3]
layout = go.Layout(title='Bitcoin with Bollinger bands, USD 2018')

fig = go.Figure(data=data, layout=layout)

# Initialize the app
app = dash.Dash()

# Set up the app
app.layout = html.Div([
                html.H1('Cryptocurrency Dashboard',
                    style={'textAlign':'center'}),
                html.Div([
                    dcc.Dropdown(id='stock_plot_value', options=[dict(label=cryptos['name'][i], value=cryptos['code'][i]) for i in range(len(cryptos))], multi=True, value='BTC-USD')
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Dropdown(id='bollinger_plot_value', options=[dict(label=cryptos['name'][i], value=cryptos['code'][i]) for i in range(len(cryptos))])
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Graph(id='stock_plot',figure=fig)
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Graph(id='bollinger_plot',figure=fig)
                ], style=dict(width='50%', display='inline-block'))
])

# Add the server clause
if __name__ == '__main__':
    app.run_server()
