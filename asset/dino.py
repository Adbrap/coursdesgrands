# ----- initialisation des modules -----#
import time

import pandas as pd
import numpy
from tkinter import Tk
from tkinter import messagebox
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import requests
import datetime
from numpy import *
from matplotlib.pyplot import *
import colorama
from colorama import Fore
import os
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from multiprocessing import Process
import math
import webbrowser
import random


# ----- initialisation des couleurs du modules pystyle -----#
class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR
    PURPLE = '\033[35m'  # PURPLE

w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX
# ----- initialisation des couleurs du modules pystyle -----#

# ----- initialisation des temps de recherches -----#
date = datetime.datetime.now()
my_lock = threading.RLock()
end = str(pd.Timestamp.today() + pd.DateOffset(5))[0:10]
start_5m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15000))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-20))[0:10]
start_1d = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
start_1week = str(pd.Timestamp.today() + pd.DateOffset(-120))[0:10]
start_1month = str(pd.Timestamp.today() + pd.DateOffset(-240))[0:10]
# ----- initialisation des temps de recherches -----#
fini = False
ticker = sys.argv[1]
minute = sys.argv[2]
time_name = sys.argv[3]
tp = sys.argv[4]
sl = sys.argv[5]

minute = int(minute)
tp = float(tp)
sl = float(sl)
def haie(ticker,time_name1,time1,start,tp,sl):
    global fini



# ----- initialisation de l'API key et ticker -----#
    api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
    #api_key = 'q5li8Y5ldvlF7eP8YI7XdMWbyOA3scWJ'
    tiker_live = ticker
    # ----- Appel des données Polygon.io OHLC et creation du DF -----#

    try:
        api_url_livePrice = f'http://api.polygon.io/v2/last/trade/{tiker_live}?apiKey={api_key}'
        #api_url_livePrice = 'http://ab-trading.fr/data.json'
        data = requests.get(api_url_livePrice).json()
        df_livePrice = pd.DataFrame(data)
        # api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/15/minute/2022-07-01/2022-07-15?adjusted=true&sort=asc&limit=30000&apiKey={api_key}'
        api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
        #api_url_OHLC = 'http://ab-trading.fr/data2.json'
        data = requests.get(api_url_OHLC).json()
        df = pd.DataFrame(data['results'])
        la_place_de_p = 0
        for k in range(0, len(df_livePrice.index)):
            if df_livePrice.index[k] == 'p':
                la_place_de_p = k
        livePrice = df_livePrice['results'].iloc[la_place_de_p]
    except:
        Write.Print("<⛔> <⛔> <⛔> <⛔> ERREUR CRITIQUE <⛔> <⛔> <⛔> <⛔>", Colors.red, interval=0.000)
        print('')

        # ----- Appel des données Polygon.io OHLC et creation du DF -----#

    dernieres_lignes = df.iloc[-2:]
    nouveau_df = pd.DataFrame(dernieres_lignes)
    df = df.drop(df.index[-1])
    df = df.tail(30)

    # ----- creation des locals(min/max) -----#
    local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
    local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
    # ----- creation des locals(min/max) -----#

    # ----- suppression des points morts de la courbe -----#
    test_min = []
    test_max = []

    q = 0
    p = 0

    len1 = len(local_min)
    len2 = len(local_max)
    while p < len1 - 5 or p < len2 - 5:
        if local_min[p + 1] < local_max[p]:
            test_min.append(local_min[p])
            local_min = np.delete(local_min, p)

            p = p - 1
        if local_max[p + 1] < local_min[p + 1]:
            test_max.append(local_max[p])
            local_max = np.delete(local_max, p)

            p = p - 1
        p = p + 1

        len1 = len(local_min)
        len2 = len(local_max)

    highs = df.iloc[local_max, :]
    lows = df.iloc[local_min, :]

    #fig1 = plt.figure(figsize=(10, 7))
    #plt.plot([], [], " ")
    #fig1.patch.set_facecolor('#17DE17')
    #fig1.patch.set_alpha(0.3)
    #timestamp_sec1 = df['t'].iloc[0] / 1000
    #timestamp_sec2 = df['t'].iloc[-1] / 1000
    #plt.title(
    #    f'''IETE : {ticker} {start} | {end} | réel : {datetime.datetime.fromtimestamp(timestamp_sec1)} /  {datetime.datetime.fromtimestamp(timestamp_sec2)}  G''',
    #    fontweight="bold", color='black')
    #df['c'].plot(color=['blue'], label='Clotures')
    #plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
    #plt.axhline(y=tp, linestyle='--', alpha=1, color='green',
    #            label='30% objectif')
    #plt.axhline(y=sl, linestyle='--', alpha=1, color='red',
    #            label='-5% objectif')
    #plt.scatter(x=lows.index, y=lows["c"], alpha=0.4)
    #plt.scatter(x=highs.index, y=highs["c"], alpha=0.4)
    #plt.scatter(x=df['c'].index[-1], y=df['c'].iloc[-1], alpha=0.4, color='blue')
    #plt.scatter(x=df['c'].index[-2], y=df['c'].iloc[-2], alpha=0.4, color='blue')
    #plt.text(df['c'].index[-1], df['c'].iloc[-1], f"G  {round(df['c'].iloc[-1], 5)}", ha='left', style='normal',
    #         size=10.5,
    #         color='red', wrap=True)
    #plt.show()



    if df["c"].iloc[-1] >= tp:
        print("Sa a dépassé le takeprofit")
        fini = True
        fig1 = plt.figure(figsize=(10, 7))
        plt.plot([], [], " ")
        fig1.patch.set_facecolor('#17DE17')
        fig1.patch.set_alpha(0.3)
        timestamp_sec1 = df['t'].iloc[0] / 1000
        timestamp_sec2 = df['t'].iloc[-1] / 1000
        plt.title(
            f'''IETE : {ticker} {start} | {end} | réel : {datetime.datetime.fromtimestamp(timestamp_sec1)} /  {datetime.datetime.fromtimestamp(timestamp_sec2)}  G''',
            fontweight="bold", color='black')
        df['c'].plot(color=['blue'], label='Clotures')
        plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
        plt.axhline(y=tp, linestyle='--', alpha=1, color='green',
                    label='30% objectif')
        plt.scatter(x=lows.index, y=lows["c"], alpha=0.4)
        plt.scatter(x=highs.index, y=highs["c"], alpha=0.4)
        plt.scatter(x=df['c'].index[-1], y=df['c'].iloc[-1], alpha=0.4,color='blue')
        plt.scatter(x=df['c'].index[-2], y=df['c'].iloc[-2], alpha=0.4, color='blue')
        plt.text(df['c'].index[-1], df['c'].iloc[-1], f"G  {round(df['c'].iloc[-1], 5)}", ha='left', style='normal', size=10.5,
                 color='red', wrap=True)
        plt.savefig(f'images2/{ticker}-{date}.png')
        plt.close()

    if df["c"].iloc[-1] <= sl:
        print("Sa a dépassé le stoploss")
        fini = True
        fig1 = plt.figure(figsize=(10, 7))
        plt.plot([], [], " ")
        fig1.patch.set_facecolor('#ff0000')
        fig1.patch.set_alpha(0.3)
        timestamp_sec1 = df['t'].iloc[0] / 1000
        timestamp_sec2 = df['t'].iloc[-1] / 1000
        plt.title(
            f'''IETE : {ticker} {start} | {end} | réel : {datetime.datetime.fromtimestamp(timestamp_sec1)} /  {datetime.datetime.fromtimestamp(timestamp_sec2)}  P''',
            fontweight="bold", color='black')
        df['c'].plot(color=['blue'], label='Clotures')
        plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
        plt.axhline(y=sl, linestyle='--', alpha=1, color='red',
                    label='-5% objectif')
        plt.scatter(x=lows.index, y=lows["c"], alpha=0.4)
        plt.scatter(x=highs.index, y=highs["c"], alpha=0.4)
        plt.scatter(x=df['c'].index[-1], y=df['c'].iloc[-1], alpha=0.4,color='blue')
        plt.scatter(x=df['c'].index[-2], y=df['c'].iloc[-2], alpha=0.4, color='blue')
        plt.text(df['c'].index[-1], df['c'].iloc[-1], f"G  {round(df['c'].iloc[-1], 5)}", ha='left', style='normal', size=10.5,
                 color='red', wrap=True)
        plt.savefig(f'images2/{ticker}-{date}.png')
        plt.close()

while fini == False:
    if time_name == 'minute':
        haie(ticker,"minute",minute,start_1h,tp,sl)
    if time_name == 'hour':
        haie(ticker, "hour", minute, start_6h, tp, sl)
    time.sleep(5.5)






