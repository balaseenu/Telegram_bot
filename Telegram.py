# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 08:45:03 2025

@author: Balachandar 
"""
#Import the requierd libraries 
from tvDatafeed import TvDatafeed, Interval
import requests
import os
    
#get Forex data 
def get_forex_data():
    # TradingView login (guest mode works too)
    tv = TvDatafeed()
    # Fetch 15 mins of XAUUSD data
    df = tv.get_hist(symbol='XAUUSD', exchange='OANDA', interval=Interval.in_15_minute, n_bars=10).reset_index()
    df = df.reset_index(drop=True)
    # Define sessions in Mexico time
    return df

def mins5_strategy(data):
    last_open = data['open'].iloc[-1]
    last_close = data['close'].iloc[-1]
    diff = last_close - last_open

    if diff >= 10:
        return f"Bullish candle: +{diff:.2f} points"
    elif diff <= -10:
        return f"Bearish candle: {diff:.2f} points"
    else:
        pass
    
def last_3candles(data):
    candle_3 = data['open'].iloc[-3]
    candle_2 = data['open'].iloc[-2]
    candle_1 = data['open'].iloc[-1]
    print(candle_1,candle_2,candle_3)
    
    if candle_1 > candle_2 and candle_2 > candle_3:
        if (candle_1 - candle_3) > 10:
            return f"last 3 Bullish candle: +{candle_1 - candle_3:.2f} points"
    elif candle_1 < candle_2 and candle_2 < candle_3:
        if (candle_3 - candle_1) > 10:
            return f"last 3 Bearish candle: +{candle_3 - candle_1:.2f} points"
        
def wick_found(data):
    last = data.iloc[-1]
    upper_wick = last['high'] - max(last['open'], last['close'])
    lower_wick = min(last['open'], last['close']) - last['low']
    print(upper_wick)
    print(lower_wick)
    if upper_wick >= 5 or lower_wick >= 5:
        return "candle wick is greater than 5 points"
    
    
def send_message(message,bot_token,chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
        }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.text)

def normalized(check):
    if check is not None:
        bot_token = os.getenv("TOKEN")
        chat_id = os.getenv("CHAT_ID")
        send_message(result,bot_token,chat_id)
    else:
        pass
    
if __name__ == '__main__':
    data = get_forex_data()  
    result = mins5_strategy(data)
    normalized(result)
    output = last_3candles(data)
    normalized(output)
    msg = wick_found(data)
    normalized(msg)
