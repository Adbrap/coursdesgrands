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
import shutil
import ftplib
import re


def increment_value(html_content, selector):
    start_tag = f'<td>{selector}</td>'
    end_tag = '</td>'

    start_index = html_content.find(start_tag)
    if start_index != -1:
        start_index = html_content.find('<td>', start_index + len(start_tag))
        end_index = html_content.find(end_tag, start_index)
        if start_index != -1 and end_index != -1:
            value = int(html_content[start_index + 4:end_index])
            new_value = value + 1
            html_content = html_content[:start_index + 4] + str(new_value) + html_content[end_index:]

    return html_content


def deplacer_fichier(source, destination):
    try:
        # Vérifie si le fichier source existe
        if os.path.exists(source):
            # Déplace le fichier source vers la destination
            shutil.move(source, destination)
            print(f"Le fichier {source} a été déplacé vers {destination}.")
        else:
            print(f"Le fichier {source} n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

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
jaune = sys.argv[6]

minute = int(minute)
tp = float(tp)
sl = float(sl)
def haie(ticker,time_name1,time1,start,tp,sl,jaune):
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
        plt.savefig(f'pierres_trier/{ticker}-{date}.png')
        plt.close()
        # Informations de connexion FTP
        ftp_server = 'server133.web-hosting.com'
        ftp_username = 'abtrqawg'
        ftp_password = 'Km8V2Q67pUbL'
        ftp_file_path = '/public_html/index.html'

        # Connexion au serveur FTP
        ftp = ftplib.FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        # Téléchargement du fichier HTML depuis le serveur FTP
        with open('fichier_local.html', 'wb') as file:
            ftp.retrbinary(f'RETR {ftp_file_path}', file.write)

        # Lire le contenu du fichier HTML local
        with open('fichier_local.html', 'r') as file:
            html_content = file.read()

        # Incrémenter les valeurs spécifiées
        html_content = increment_value(html_content, 'Nombre de trades fini')
        html_content = increment_value(html_content, 'Nombre de trades gagnés')

        # Écrire le contenu modifié dans le fichier HTML local
        with open('fichier_local.html', 'w') as file:
            file.write(html_content)

        # Téléverser le fichier HTML modifié sur le serveur FTP
        with open('fichier_local.html', 'rb') as file:
            ftp.storbinary(f'STOR {ftp_file_path}', file)

        # Fermer la connexion FTP
        ftp.quit()

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
        plt.savefig(f'pierres_trier/{ticker}-{date}.png')
        plt.close()
        # Informations de connexion FTP
        ftp_server = 'server133.web-hosting.com'
        ftp_username = 'abtrqawg'
        ftp_password = 'Km8V2Q67pUbL'
        ftp_file_path = '/public_html/index.html'

        # Connexion au serveur FTP
        ftp = ftplib.FTP(ftp_server)
        ftp.login(ftp_username, ftp_password)

        # Téléchargement du fichier HTML depuis le serveur FTP
        with open('fichier_local.html', 'wb') as file:
            ftp.retrbinary(f'RETR {ftp_file_path}', file.write)

        # Lire le contenu du fichier HTML local
        with open('fichier_local.html', 'r') as file:
            html_content = file.read()

        # Incrémenter les valeurs spécifiées
        html_content = increment_value(html_content, 'Nombre de trades fini')
        html_content = increment_value(html_content, 'Nombre de trades perdu')

        # Écrire le contenu modifié dans le fichier HTML local
        with open('fichier_local.html', 'w') as file:
            file.write(html_content)

        # Téléverser le fichier HTML modifié sur le serveur FTP
        with open('fichier_local.html', 'rb') as file:
            ftp.storbinary(f'STOR {ftp_file_path}', file)

        # Fermer la connexion FTP
        ftp.quit()

    if fini == True:
        chemin_source = f"trouvailles/{ticker} {minute} {time_name} {tp} {sl} .png"
        chemin_destination = f"trouvailles/fini/{ticker} {minute} {time_name} {tp} {sl} .png"


        deplacer_fichier(chemin_source, chemin_destination)


if time_name == 'minute':
    haie(ticker,"minute",minute,start_1h,tp,sl,jaune)
if time_name == 'hour':
    haie(ticker, "hour", minute, start_6h, tp, sl,jaune)
print(ticker)






