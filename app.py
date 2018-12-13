import pandas as pd
import pandas_datareader as pdr
import numpy as np
import plotly.graph_objs as go
from utils import compute_bollinger, bollinger_strategy, get_news
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output # Add State later
# Remove indentation to avoid markdown not rendering
from textwrap import dedent

# Cryptocurrencies data
cryptos = pd.read_csv('data/cryptos.csv')

# url for news
url = 'https://newsapi.org/v2/everything?q=cryptocurrency&sortBy=publishedAt&apiKey=e3e38edf30814dc18ef7f21a7fb9e775'

# Get table of news data
headlines = get_news(url)

# Set dates
start_date = pd.datetime(2018,1,1)
end_date = pd.datetime.today()

# Set window size and number of standard deviations (can make an input later!)
window_size = 50
no_std_devs = 1.5

# Color scheme dictionary
color = {'background':'#C96567', 'text':'white', 'div':'314455', 'plot':'#373737'}

# Initialize the app
app = dash.Dash()

# Append W3 CSS
app.css.append_css({'external_url': 'https://www.w3schools.com/w3css/4/w3.css'})

# Set up the app
app.layout = html.Div([
                html.H1('Exploring the Cryptocurrency Market',
                    style={'textAlign':'center', 'fontFamily':'serif'}),
                html.Div([
                    html.Div([
                            dash_table.DataTable(
                                id='news_table',
                                columns=[{"name": i, "id": i} for i in headlines.columns],
                                data=headlines.to_dict("rows")
                            )
                    ], className='w3-container w3-cell'),
                    html.Div([
                    # Another column
                        html.Div([
                            dcc.Dropdown(id='stock_plot_value', options=[dict(label=cryptos['name'][i], value=cryptos['code'][i]) for i in range(len(cryptos))], multi=True, value=['BTC-USD'])
                ]),
                        html.Div([
                            dcc.Graph(id='stock_plot')
                ]),
                        html.Div([
                            dcc.Dropdown(id='bollinger_plot_value', options=[dict(label=cryptos['name'][i], value=cryptos['code'][i]) for i in range(len(cryptos))], value='BTC-USD')
                ]),
                        html.Div([
                            dcc.Graph(id='bollinger_plot')
                ]),
                        html.Div([
                            dcc.Markdown(id='bollinger_performance')
                ], style={"text-align":'center'})
                    ], className='w3-container w3-cell')
                ], className='w3-cell-row')
], style={'width':'100%', 'height':'100%', 'backgroundColor':color['background']})

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
    layout = go.Layout(title='Cryptocurrencies in 2018', paper_bgcolor=color['plot'], font=dict(color=color['text']))
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
    layout = go.Layout(title='{} with Bollinger Bands'.format(value), paper_bgcolor=color['plot'], font=dict(color=color['text']))
    fig = go.Figure(data=data, layout=layout)
    return fig

@app.callback(Output('bollinger_performance', 'children'),
                [Input('bollinger_plot_value', 'value')])
def strategy_performance(value):
    stock = pdr.get_data_yahoo(value, start_date, end_date)
    stock_data = bollinger_strategy(stock, window_size, no_std_devs)
    stock_data['Position'].fillna(method='ffill', inplace=True)
    stock_data['Market Return'] = stock_data['Open'].pct_change()
    stock_data['Strategy Return'] = stock_data['Market Return'] * stock_data['Position']
    avg_d_ret = stock_data['Strategy Return'].mean()
    avg_m_ret = stock_data['Strategy Return'].resample('M').mean().mean()
    cum_ret = stock_data['Strategy Return'].cumsum()[-1]
    # Report information
    text = """
    ### {value} Performance
    **Average Daily Return**: {avgdret}%

    **Average Monthly Return**: {avgmret}%

    **Cumulative Return**: {cumsum}%
    """.format(value=value, avgdret=round(avg_d_ret*100,2), avgmret=round(avg_m_ret*100,2), cumsum=round(cum_ret*100,2))
    return dedent(text)

# Add the server clause
if __name__ == '__main__':
    app.run_server()
