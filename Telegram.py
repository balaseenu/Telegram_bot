''' Import all the Liabraries '''

import os
from telegram.ext import Application, MessageHandler, filters
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
import nest_asyncio

#set environment variable
def set_environ():
    os.environ['TOKEN'] = '8380163368:AAHq78IVBsKUAenRc_mrDtd-tcGpun_D9kM'
    os.environ['CHAT_ID'] = '8451555149'
    
def get_forex(text):
    check = text.split(' ')
    print(check)
    tv = TvDatafeed()
    df = tv.get_hist(symbol='USDJPY',exchange='OANDA',interval=Interval.in_5_minute,n_bars=200) 
    df = df.reset_index().rename(columns={'time':'datetime'})
    df['datetime'] = pd.to_datetime(df['datetime'])
    print(df['close'].iloc[-1])
    if check[0] == 'between':
        if df['close'].iloc[-1] <= float(check[1]) or df['close'].iloc[-1] >= float(check[3]):
            out = f"price crossed {df['close'].iloc[-1]}"
            return out
    elif check[0] == 'check':
        if df['close'].iloc[-1] >= float(check[1]):
            out = f"price crossed {df['close'].iloc[-1]}"
            return out

#RECIEVE MESSAGE FROM TELEGRAM AND SEND BACK THE RESPONSE     
async def echo(update, context):
    text = update.message.text
    result = get_forex(text)
    await update.message.reply_text(f"Alert : {result}")



#main function starts here
if __name__ == '__main__':
    set_environ()
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    nest_asyncio.apply()
    
    #asyncio.run(main())
    app = Application.builder().token(TOKEN).build()

    # Handle normal text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot is running... (Press CTRL+C to stop)")
    app.run_polling()
    