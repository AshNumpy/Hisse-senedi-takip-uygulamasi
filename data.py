import pandas as pd 
import numpy as np
import yfinance as yf


semboller = pd.read_csv('https://raw.githubusercontent.com/f1rzen/halkbank-skorkart-scraper/main/hisseisimleri.csv')

def get_dataset(item, period='2y', interval='1d'):
    """
    Parameters:\n
    item: Verilerini çekmek istediğin hisse senedinin Yahoo finance kodunu item e eşitleyip gir.\n
    period: Ne kadar geriye dönük bir veri çekilecek (5y: 5 yıl, 1y: 1 yıl, 1m: 1 Ay, 1w, 1d, 1H, ...)\n
    interval: Veriler ne tipinde çekilecek (1d: Günlük, 1w: Haftalık, 1m: Aylık, 1y: Yıllık)\n
        
    Return: veri seti
    """

    tracker = yf.Ticker(item)

    df = tracker.history(period=period, interval=interval)
    
    df = df.reset_index()
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Date'] = df['Date'].dt.date

    df = df.set_index('Date')

    return df 


def get_dividends(item):
    """
    Parameters:\n
    item: temettülerini istediğin hisse senedinin yahoo finance kodunu item e eşitleyerek girdi yap\n

    Return: Verdiği temettüler (hisse senedi başına kaç tl olduğu)
    """

    tracker = yf.Ticker(item)

    dividends = pd.DataFrame(tracker.dividends)
    dividends = dividends.reset_index()

    dividends['Date'] = pd.to_datetime(dividends['Date']).dt.date
    dividends = dividends.iloc[1:,]
    dividends = dividends.set_index('Date')

    return dividends