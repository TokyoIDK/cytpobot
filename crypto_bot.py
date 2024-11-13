from pycoingecko import CoinGeckoAPI
import pandas as pd

cg = CoinGeckoAPI()

# Function to fetch crypto data
def fetch_crypto_data(crypto_ids, vs_currency='usd'):
    data = {}
    for crypto_id in crypto_ids:
        coin_data = cg.get_coin_market_chart_by_id(id=crypto_id, vs_currency=vs_currency, days=1)
        coin_df = pd.DataFrame(coin_data['prices'], columns=['timestamp', f'{crypto_id}_price'])
        coin_df['timestamp'] = pd.to_datetime(coin_df['timestamp'], unit='ms')
        data[crypto_id] = coin_df.set_index('timestamp')[f'{crypto_id}_price']
    
    # Combine the data into a single DataFrame
    df = pd.concat(data.values(), axis=1)
    return df

# Function to add technical indicators
def add_technical_indicators(df):
    df['BTC_SMA_50'] = df['bitcoin_price'].rolling(window=50).mean()
    df['ETH_SMA_50'] = df['ethereum_price'].rolling(window=50).mean()
    df['DOGE_SMA_50'] = df['dogecoin_price'].rolling(window=50).mean()
    df['BTC_SMA_200'] = df['bitcoin_price'].rolling(window=200).mean()
    df['ETH_SMA_200'] = df['ethereum_price'].rolling(window=200).mean()
    df['DOGE_SMA_200'] = df['dogecoin_price'].rolling(window=200).mean()
    
    df['BTC_RSI'] = calculate_rsi(df['bitcoin_price'])
    df['ETH_RSI'] = calculate_rsi(df['ethereum_price'])
    df['DOGE_RSI'] = calculate_rsi(df['dogecoin_price'])
    
    return df

# Function to calculate RSI
def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Generate signals based on technical indicators
def generate_signals(df):
    df['BTC_Signal'] = 0
    df.loc[df['bitcoin_price'] > df['BTC_SMA_50'], 'BTC_Signal'] = 1  # Buy signal
    df.loc[df['bitcoin_price'] < df['BTC_SMA_50'], 'BTC_Signal'] = -1  # Sell signal
    
    df['ETH_Signal'] = 0
    df.loc[df['ethereum_price'] > df['ETH_SMA_50'], 'ETH_Signal'] = 1  # Buy signal
    df.loc[df['ethereum_price'] < df['ETH_SMA_50'], 'ETH_Signal'] = -1  # Sell signal
    
    df['DOGE_Signal'] = 0
    df.loc[df['dogecoin_price'] > df['DOGE_SMA_50'], 'DOGE_Signal'] = 1  # Buy signal
    df.loc[df['dogecoin_price'] < df['DOGE_SMA_50'], 'DOGE_Signal'] = -1  # Sell signal
    
    return df
