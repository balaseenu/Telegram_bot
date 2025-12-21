from tvDatafeed import TvDatafeed, Interval
import requests
import os


# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# ---------------- DATA FETCH ----------------
def get_forex_data():
    tv = TvDatafeed()  # guest login
    df = tv.get_hist(
        symbol="XAUUSD",
        exchange="OANDA",
        interval=Interval.in_15_minute,
        n_bars=10
    ).reset_index(drop=True)
    return df


# ---------------- STRATEGIES ----------------
def mins5_strategy(data):
    last_open = data["open"].iloc[-1]
    last_close = data["close"].iloc[-1]
    diff = last_close - last_open

    if diff >= 10:
        return f"Bullish candle: +{diff:.2f} points"
    elif diff <= -10:
        return f"Bearish candle: {diff:.2f} points"
    return None


def last_3candles(data):
    c1 = data["open"].iloc[-1]
    c2 = data["open"].iloc[-2]
    c3 = data["open"].iloc[-3]

    if c1 > c2 > c3 and (c1 - c3) > 10:
        return f"Last 3 bullish candles: +{c1 - c3:.2f} points"
    elif c1 < c2 < c3 and (c3 - c1) > 10:
        return f"Last 3 bearish candles: +{c3 - c1:.2f} points"
    return None


def wick_found(data):
    last = data.iloc[-1]
    upper_wick = last["high"] - max(last["open"], last["close"])
    lower_wick = min(last["open"], last["close"]) - last["low"]

    if upper_wick >= 5 or lower_wick >= 5:
        return (
            f"Wick detected | Upper: {upper_wick:.2f}, "
            f"Lower: {lower_wick:.2f}"
        )
    return None


# ---------------- TELEGRAM ----------------
def send_message(message):
    if not message:
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


# ---------------- MAIN ----------------
def main():
    try:
        data = get_forex_data()

        send_message(mins5_strategy(data))
        send_message(last_3candles(data))
        send_message(wick_found(data))

    except Exception as e:
        send_message(f"❌ Bot error: {str(e)}")


if __name__ == "__main__":
    main()
