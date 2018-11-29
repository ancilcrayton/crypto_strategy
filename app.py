import pandas as pd
import pandas_datareader as pdr
import numpy as np
import plotly.graph_objs as go
from utils import compute_bollinger
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # Add State later
# Remove indentation to avoid markdown not rendering
from textwrap import dedent

# Cryptocurrencies data
cryptos = pd.read_csv('data/cryptos.csv')

# Set dates
start_date = pd.datetime(2018,1,1)
end_date = pd.datetime.today()

# Set window size and number of standard deviations (can make an input later!)
window_size = 7
no_std_devs = 2

# Initialize the app
app = dash.Dash()

# Set up the app
app.layout = html.Div([
                html.H1('Exploring the Cryptocurrency Market',
                    style={'textAlign':'center'}),
                html.Div([
                    dcc.Dropdown(id='stock_plot_value', options=[dict(label=cryptos['name'][i], value=cryptos['code'][i]) for i in range(len(cryptos))], multi=True, value=['BTC-USD'])
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Dropdown(id='bollinger_plot_value', options=[dict(label=cryptos['name'][i], value=cryptos['code'][i]) for i in range(len(cryptos))], value='BTC-USD')
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Graph(id='stock_plot')
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Graph(id='bollinger_plot')
                ], style=dict(width='50%', display='inline-block')),
                html.Div([
                    dcc.Markdown(id='bollinger_performance')
                ], style={"width":'50%', "display":'inline-block', "float":'right', "text-align":'center'})
])

# Add interactivity for stock comparison graph
@app.callback(Output('stock_plot', 'figure'),
                [Input('stock_plot_value', 'value')])
def stock_graph(values):
    traces = []
    for value in values:
        stock = pdr.get_data_yahoo(value, start_date, end_date)
        stock_open = stock['Open']
        trace = go.Scatter(x=stock_open.index, y = stock_open,
                          mode='lines', name=value)
        traces.append(trace)
    layout = go.Layout(title='Cryptocurrencies in 2018')
    fig = go.Figure(data=traces, layout=layout)
    return fig

# Add interactivity for Bollinger graph
@app.callback(Output('bollinger_plot', 'figure'),
                [Input('bollinger_plot_value', 'value')])
def bollinger_graph(value):
    stock = pdr.get_data_yahoo(value, start_date, end_date)
    stock_open = stock['Open']
    bollinger_low, bollinger_high = compute_bollinger(stock_open, window_size, no_std_devs)
    trace1 = go.Scatter(x=stock_open.index, y = stock_open,
                      mode='lines', name=value)
    trace2 = go.Scatter(x=stock_open.index, y = bollinger_low,
                      line=dict(dash='dash'), name='Bollinger Low')
    trace3 = go.Scatter(x=stock_open.index, y = bollinger_high,
                      line=dict(dash='dash'), name='Bollinger High')
    data = [trace1, trace2, trace3]
    layout = go.Layout(title='{} with Bollinger Bands'.format(value))
    fig = go.Figure(data=data, layout=layout)
    return fig

@app.callback(Output('bollinger_performance', 'children'),
                [Input('bollinger_plot_value', 'value')])
def strategy_performance(value):
    text = """
    ### {value} Performance
    **Average Daily Return**:

    **Average Monthly Return**:

    **Cumulative Return**:
    """.format(value=value)
    return dedent(text)

# Add the server clause
if __name__ == '__main__':
    app.run_server()
