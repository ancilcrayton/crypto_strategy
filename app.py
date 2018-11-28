import pandas as pd
import pandas_datareader as pdr
import numpy as np
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # Add State later

# Set dates
start_date = pd.datetime(2018,1,1)
end_date = pd.datetime.today()

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
                  mode='lines', name='Bollinger Low')
trace3 = go.Scatter(x=btc_open.index, y = bollinger_high,
                  mode='lines', name='Bollinger High')

data = [trace1, trace2, trace3]
layout = go.Layout(title='Bitcoin with Bollinger bands, USD 2018')

fig = go.Figure(data=data, layout=layout)

# Initialize the app
app = dash.Dash()

# Set up the app
app.layout = html.Div([
                html.H1('Cryptocurrency Dashboard'),
                dcc.Graph(id='btc_plot',
                        figure=fig),

])

# Add the server clause
if __name__ == '__main__':
    app.run_server()
