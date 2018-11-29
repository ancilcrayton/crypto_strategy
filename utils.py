import pandas as pd

def compute_bollinger(df, window_size, no_std_devs):
    """Short summary.

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
