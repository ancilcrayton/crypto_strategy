import pandas as pd

def compute_bollinger(df, window_size, no_std_devs):
    """This function computes the Bollinger bands.

    Parameters
    ----------
    df : df column
        This should be the stock price column of a Pandas dataframe.
    window_size : int
        This should be the number of days to calculate the rolling mean and standard deviation.
    no_std_devs : int
        Number of standard deviations to calculate the Bollinger bands.

    Returns
    -------
    dataframe columns
        The function returns a tuple of the bollinger bands, both low and high.

    """
    # Calculate rolling mean and standard deviation
    df_mean = df.rolling(window_size).mean()
    df_std = df.rolling(window_size).std()
    # Calculate bollinger bands
    bollinger_low = df_mean - (df_std*no_std_devs)
    bollinger_high = df_mean + (df_std*no_std_devs)
    return bollinger_low, bollinger_high

def bollinger_strategy(df, window_size, no_std_devs):
    """This function performs the Bollinger Strategy and returns a dataframe that includes the relevant positions.

    Parameters
    ----------
    df : DataFrame
        Dataframe which includes stock price.

    Returns
    -------
    DataFrame
        Returns a DataFrame which includes the position based on the Bollinger Strategy.

    """
    # Compute Bollinger bands using above function
    df['Bollinger Low'], df['Bollinger High'] = compute_bollinger(df=df, window_size=window_size, no_std_devs=no_std_devs)

    # Initialize an empty Position column to fill in
    df['Position'] = None

    # Set initial status to open and iterate over each row index
    mode = 'open'
    for index in range(len(df)):
        if index == 0:
            continue

        # Grab current and previous row
        row = df.iloc[index]
        prev_row = df.iloc[index-1]

        # Hold long position
        if mode == 'open' and row['Open'] < row['Bollinger Low'] and prev_row['Open'] > prev_row['Bollinger Low']:
            df.iloc[index, df.columns.get_loc('Position')] = 1
            mode = 'close'

        # Hold a short position
        if mode == 'close' and row['Open'] > row['Bollinger High'] and prev_row['Open'] < prev_row['Bollinger High']:
            df.iloc[index, df.columns.get_loc('Position')] = -1
            mode = 'open'

    return df
