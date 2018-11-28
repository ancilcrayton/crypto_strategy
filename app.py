import pandas as pd
import pandas_datareader as pdr
import numpy as np
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html

# Initialize the app
app = dash.Dash()

# Set up the app
app.layout = html.Div([
                html.H1('Cryptocurrency Dashboard')
])

# Add the server clause
if __name__ == '__main__':
    app.run_server()
