import streamlit as st
import matplotlib.pyplot as plt
from crypto_bot import fetch_crypto_data, add_technical_indicators, generate_signals

# Set up the Streamlit app
st.title('Cryptocurrency Investment Tracker')
st.write("Tracking Bitcoin, Ethereum, and Dogecoin with technical indicators!")

# Fetch and process crypto data
cryptos = ['bitcoin', 'ethereum', 'dogecoin']
crypto_data = fetch_crypto_data(cryptos)
crypto_data = add_technical_indicators(crypto_data)
crypto_data = generate_signals(crypto_data)

# Display the data table
st.write(crypto_data.tail())

# Plot the data for Bitcoin
def plot_crypto_data(df, crypto):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df[f'{crypto}_price'], label=f'{crypto.capitalize()} Price', color='blue')
    ax.plot(df.index, df[f'{crypto}_SMA_50'], label='50-Day SMA', color='orange')
    ax.plot(df.index, df[f'{crypto}_SMA_200'], label='200-Day SMA', color='green')
    ax.set_title(f'{crypto.capitalize()} Price with Technical Indicators')
    ax.legend()
    st.pyplot(fig)

# Plot for each coin
plot_crypto_data(crypto_data, 'bitcoin')
plot_crypto_data(crypto_data, 'ethereum')
plot_crypto_data(crypto_data, 'dogecoin')
