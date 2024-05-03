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
from ftplib import FTP
import ftplib
import requests


def recuperer_contenu(url):
    try:
        # Envoyer une requête GET à l'URL pour obtenir le contenu du fichier
        reponse = requests.get(url, verify=False)

        # Vérifier si la requête a réussi (statut 200)
        if reponse.status_code == 200:
            # Renvoyer le contenu du fichier
            return reponse.text
        else:
            print("La requête a échoué avec le code de statut :", reponse.status_code)
            return None
    except requests.RequestException as e:
        print("Une erreur s'est produite lors de la requête :", e)
        return None

def ecrire(fichier1, nombre):
    try:
        # Essayer d'ouvrir le fichier en mode lecture
        with open(fichier1, 'r') as fichier:
            # Lire la première ligne du fichier et convertir en entier
            nombre_actuel = float(fichier.readline().strip())
    except FileNotFoundError:
        # Si le fichier n'existe pas, afficher un message d'erreur et quitter
        print("Erreur : Le fichier n'existe pas.")
        return

    # Incrémenter le nombre
    nombre_actuel += nombre

    # Écrire le nouveau nombre dans le fichier
    with open(fichier1, 'w') as fichier:
        fichier.write(str(nombre_actuel))

    # Afficher le nombre actuel
    print(nombre_actuel)
def ecrire2(fichier1, nombre):
    try:
        # Ouvrir le fichier en mode écriture (ceci effacera son contenu)
        with open(fichier1, 'w') as fichier:
            # Écrire le nouveau nombre dans le fichier
            fichier.write(str(nombre))
    except Exception as e:
        # Gérer les exceptions
        print("Une erreur s'est produite :", e)
        return

    # Afficher le nombre actuel
    print("Nombre actuel écrit dans le fichier :", nombre)

def ecrire3(fichier1, nombre):
    try:
        # Ouvrir le fichier en mode ajout (append) pour ajouter à la fin
        with open(fichier1, 'a') as fichier:
            # Écrire le nouveau nombre suivi d'un saut de ligne
            fichier.write(str(nombre) + '\n')
    except Exception as e:
        # Gérer les exceptions
        print("Une erreur s'est produite :", e)
        return

    # Afficher le nombre ajouté
    print("Nombre ajouté au fichier :", nombre)

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
start_15m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_30m = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_1h = str(pd.Timestamp.today() + pd.DateOffset(-15))[0:10]
start_6h = str(pd.Timestamp.today() + pd.DateOffset(-25))[0:10]
start_12h = str(pd.Timestamp.today() + pd.DateOffset(-35))[0:10]
start_18h = str(pd.Timestamp.today() + pd.DateOffset(-50))[0:10]
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
nomdufichier = sys.argv[7]

minute = int(minute)
tp = float(tp)
sl = float(sl)
jaune = float(jaune)


def haie(ticker, time_name1, time1, start, tp, sl, jaune):
    global fini

    # ----- initialisation de l'API key et ticker -----#
    api_key = '1KsqKOh1pTAJyWZx6Qm9pvnaNcpKVh_8'
    # api_key = 'q5li8Y5ldvlF7eP8YI7XdMWbyOA3scWJ'
    # ----- Appel des données Polygon.io OHLC et creation du DF -----#

    try:
        api_url_OHLC = f'http://api.polygon.io/v2/aggs/ticker/{ticker}/range/{time1}/{time_name1}/{start}/{end}?adjusted=true&limit=50000&apiKey={api_key}'
        data = requests.get(api_url_OHLC).json()
        df = pd.DataFrame(data['results'])
    except:
        Write.Print("<⛔> <⛔> <⛔> <⛔> ERREUR CRITIQUE <⛔> <⛔> <⛔> <⛔>", Colors.red, interval=0.000)
        print('')

        # ----- Appel des données Polygon.io OHLC et creation du DF -----#

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

    # fig1 = plt.figure(figsize=(10, 7))
    # plt.plot([], [], " ")
    # fig1.patch.set_facecolor('#17DE17')
    # fig1.patch.set_alpha(0.3)
    # timestamp_sec1 = df['t'].iloc[0] / 1000
    # timestamp_sec2 = df['t'].iloc[-1] / 1000
    # plt.title(
    #    f'''IETE : {ticker} {start} | {end} | réel : {datetime.datetime.fromtimestamp(timestamp_sec1)} /  {datetime.datetime.fromtimestamp(timestamp_sec2)}  G''',
    #    fontweight="bold", color='black')
    # df['c'].plot(color=['blue'], label='Clotures')
    # plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
    # plt.axhline(y=tp, linestyle='--', alpha=1, color='green',
    #            label='30% objectif')
    # plt.axhline(y=sl, linestyle='--', alpha=1, color='red',
    #            label='-5% objectif')
    # plt.scatter(x=lows.index, y=lows["c"], alpha=0.4)
    # plt.scatter(x=highs.index, y=highs["c"], alpha=0.4)
    # plt.scatter(x=df['c'].index[-1], y=df['c'].iloc[-1], alpha=0.4, color='blue')
    # plt.scatter(x=df['c'].index[-2], y=df['c'].iloc[-2], alpha=0.4, color='blue')
    # plt.text(df['c'].index[-1], df['c'].iloc[-1], f"G  {round(df['c'].iloc[-1], 5)}", ha='left', style='normal',
    #         size=10.5,
    #         color='red', wrap=True)
    # plt.show()

    if df["c"].iloc[-1] >= tp:
        print("Sa a dépassé le takeprofit")
        fini = True
        fig1 = plt.figure(figsize=(10, 7))
        plt.plot([], [], " ")
        fig1.patch.set_facecolor('#17DE17')
        fig1.patch.set_alpha(0.3)
        timestamp_sec1 = df['t'].iloc[0] / 1000
        timestamp_sec2 = df['t'].iloc[-1] / 1000
        plt.title(f'''IETE : {ticker} {start} | {end} | réel : {datetime.datetime.fromtimestamp(timestamp_sec1)} /  {datetime.datetime.fromtimestamp(timestamp_sec2)}  G''', fontweight="bold", color='black')
        df['c'].plot(color=['blue'], label='Clotures')
        plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
        plt.axhline(y=tp, linestyle='--', alpha=1, color='green', label='30% objectif')
        plt.axhline(y=sl, linestyle='--', alpha=1, color='red', label='-5% objectif')
        plt.scatter(x=lows.index, y=lows["c"], alpha=0.4)
        plt.scatter(x=highs.index, y=highs["c"], alpha=0.4)
        plt.scatter(x=df['c'].index[-1], y=df['c'].iloc[-1], alpha=0.4, color='blue')
        plt.scatter(x=df['c'].index[-2], y=df['c'].iloc[-2], alpha=0.4, color='blue')
        plt.text(df['c'].index[-1], df['c'].iloc[-1], f"G  {round(df['c'].iloc[-1], 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
        plt.savefig(f'/home/atoll/trouvailles2/fini/trier/{ticker}-{date} {time1} {time_name1}.png')
        plt.close()
        dfgagnant = (((df["c"].iloc[-1] - jaune) * 100) / df["c"].iloc[-1])
        ecrire('gagnant.txt', 1)
        ecrire('pourcent.txt', dfgagnant)
        ecrire2('dernierdf.txt', dfgagnant)
        ecrire3("df.txt", dfgagnant)
        shutil.move(f'/home/atoll/trouvailles2/{nomdufichier}', f'/home/atoll/trouvailles2/fini/{nomdufichier}')
        url_du_fichier_texte = "http://ab-trading.fr/plus_gros_gain2.txt"
        contenu_du_fichier = recuperer_contenu(url_du_fichier_texte)
        contenu_du_fichier = float(contenu_du_fichier)
        if dfgagnant > contenu_du_fichier:
            ecrire2('plusgrosgain.txt', dfgagnant)

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
            f'''IETE : {ticker} {start} | {end} | réel : {datetime.datetime.fromtimestamp(timestamp_sec1)} /  {datetime.datetime.fromtimestamp(timestamp_sec2)}  P''', fontweight="bold", color='black')
        df['c'].plot(color=['blue'], label='Clotures')
        plt.grid(which='major', color='#666666', linestyle='-', alpha=0.2)
        plt.axhline(y=tp, linestyle='--', alpha=1, color='green', label='30% objectif')
        plt.axhline(y=sl, linestyle='--', alpha=1, color='red', label='-5% objectif')
        plt.scatter(x=lows.index, y=lows["c"], alpha=0.4)
        plt.scatter(x=highs.index, y=highs["c"], alpha=0.4)
        plt.scatter(x=df['c'].index[-1], y=df['c'].iloc[-1], alpha=0.4, color='blue')
        plt.scatter(x=df['c'].index[-2], y=df['c'].iloc[-2], alpha=0.4, color='blue')
        plt.text(df['c'].index[-1], df['c'].iloc[-1], f"G  {round(df['c'].iloc[-1], 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
        plt.savefig(f'/home/atoll/trouvailles2/fini/trier/{ticker}-{date} {time1} {time_name1}.png')
        plt.close()
        dfperdant = (((df["c"].iloc[-1] - jaune) * 100) / jaune)
        ecrire('perdant.txt', 1)
        ecrire('pourcent.txt', dfperdant)
        ecrire2('dernierdf.txt', dfperdant)
        ecrire3("df.txt", dfperdant)
        shutil.move(f'/home/atoll/trouvailles2/{nomdufichier}', f'/home/atoll/trouvailles2/fini/{nomdufichier}')
        url_du_fichier_texte = "http://ab-trading.fr/plus_grosse_perte2.txt"
        contenu_du_fichier = recuperer_contenu(url_du_fichier_texte)
        contenu_du_fichier = float(contenu_du_fichier)
        if dfperdant < contenu_du_fichier:
            ecrire2('plusgrosseperte.txt', dfperdant)



if time_name == 'minute':
    if minute == 15:
        haie(ticker, "minute", minute, start_15m, tp, sl, jaune)
    if minute == 20:
        haie(ticker, "minute", minute, start_15m, tp, sl, jaune)
    if minute == 25:
        haie(ticker, "minute", minute, start_15m, tp, sl, jaune)
    if minute == 30:
        haie(ticker, "minute", minute, start_30m, tp, sl, jaune)
    if minute == 35:
        haie(ticker, "minute", minute, start_30m, tp, sl, jaune)
    if minute == 45:
        haie(ticker, "minute", minute, start_30m, tp, sl, jaune)
    if minute == 40:
        haie(ticker, "minute", minute, start_30m, tp, sl, jaune)
    if minute == 50:
        haie(ticker, "minute", minute, start_30m, tp, sl, jaune)
    if minute == 55:
        haie(ticker, "minute", minute, start_30m, tp, sl, jaune)
    if minute == 75:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 90:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 105:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 135:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 150:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 165:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 195:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 210:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 225:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)
    if minute == 255:
        haie(ticker, "minute", minute, start_1h, tp, sl, jaune)


if time_name == 'hour':
    if minute == 3:
        haie(ticker, "hour", minute, start_1h, tp, sl, jaune)
    if minute == 5:
        haie(ticker, "hour", minute, start_1h, tp, sl, jaune)
    if minute == 6:
        haie(ticker, "hour", minute, start_6h, tp, sl, jaune)
    if minute == 7:
        haie(ticker, "hour", minute, start_6h, tp, sl, jaune)
    if minute == 8:
        haie(ticker, "hour", minute, start_6h, tp, sl, jaune)
    if minute == 9:
        haie(ticker, "hour", minute, start_6h, tp, sl, jaune)
    if minute == 10:
        haie(ticker, "hour", minute, start_6h, tp, sl, jaune)
    if minute == 11:
        haie(ticker, "hour", minute, start_6h, tp, sl, jaune)
    if minute == 12:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 13:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 14:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 15:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 16:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 17:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 18:
        haie(ticker, "hour", minute, start_12h, tp, sl, jaune)
    if minute == 19:
        haie(ticker, "hour", minute, start_18h, tp, sl, jaune)
    if minute == 20:
        haie(ticker, "hour", minute, start_18h, tp, sl, jaune)
    if minute == 21:
        haie(ticker, "hour", minute, start_18h, tp, sl, jaune)
    if minute == 22:
        haie(ticker, "hour", minute, start_18h, tp, sl, jaune)
    if minute == 23:
        haie(ticker, "hour", minute, start_18h, tp, sl, jaune)
    if minute == 24:
        haie(ticker, "hour", minute, start_18h, tp, sl, jaune)
print(ticker)