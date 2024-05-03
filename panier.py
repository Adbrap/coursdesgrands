import os
import time
import subprocess
from ftplib import FTP
import shutil


def ecrire(fichier1, nombre):
    try:
        # Essayer d'ouvrir le fichier en mode lecture
        with open(fichier1, 'r') as fichier:
            # Lire la première ligne du fichier et convertir en entier
            nombre_actuel = int(fichier.readline().strip())
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
        # Essayer d'ouvrir le fichier en mode lecture
        with open(fichier1, 'r') as fichier:
            # Lire la première ligne du fichier et convertir en entier
            nombre_actuel = int(fichier.readline().strip())
    except FileNotFoundError:
        # Si le fichier n'existe pas, afficher un message d'erreur et quitter
        print("Erreur : Le fichier n'existe pas.")
        return

    # Incrémenter le nombre
    nombre_actuel = nombre

    # Écrire le nouveau nombre dans le fichier
    with open(fichier1, 'w') as fichier:
        fichier.write(str(nombre_actuel))

    # Afficher le nombre actuel
    print(nombre_actuel)


def miseajoursite(fichier,fichier2):
    # Informations de connexion FTP
    serveur_ftp = "server133.web-hosting.com"
    utilisateur = "abtrqawg"
    mot_de_passe = "Km8V2Q67pUbL"


    # Chemin local du fichier à téléverser
    chemin_local = fichier

    # Chemin sur le serveur où le fichier doit être téléversé
    chemin_serveur = f"/public_html/{fichier2}"

    # Se connecter au serveur FTP
    ftp = FTP(serveur_ftp)
    ftp.login(utilisateur, mot_de_passe)

    # Ouvrir le fichier en mode lecture binaire
    with open(chemin_local, 'rb') as fichier:
        # Téléverser le fichier sur le serveur en remplaçant le fichier existant s'il y en a un
        ftp.storbinary('STOR ' + chemin_serveur, fichier)

    # Fermer la connexion FTP
    ftp.quit()

    print("Fichier téléversé avec succès.")


# Chemin du dossier à surveiller
dossier_a_surveiller = "/home/atoll/trouvailles"
dossier_a_surveiller2 = "/home/atoll/trouvailles2"


# Fonction pour récupérer tous les fichiers PNG dans un dossier
def obtenir_fichiers_png(dossier):
    fichiers_png = []
    try:
        # Parcourir tous les fichiers dans le dossier spécifié
        for fichier in os.listdir(dossier):
            # Vérifier si le fichier a l'extension .png
            if fichier.lower().endswith('.png'):
                # Ajouter le chemin complet du fichier à la liste
                fichiers_png.append(os.path.join(dossier, fichier))
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return fichiers_png

while True:


    try:
        fichiers_png = obtenir_fichiers_png(dossier_a_surveiller)
        if fichiers_png:
            for fichier1 in fichiers_png:
                fichier1 = os.path.basename(fichier1)
                premier_mot = fichier1.split()[0]
                fichiers_toilette = filter(lambda x: f"{premier_mot}" in x, os.listdir('/home/atoll/trouvailles2'))
                fichiers_toilette2 = filter(lambda x: f"{premier_mot}" in x, os.listdir('/home/atoll/trouvailles2/fini'))
                if not any(fichiers_toilette) and not any(fichiers_toilette2):
                    shutil.copy(f'/home/atoll/trouvailles/{fichier1}', f'/home/atoll/trouvailles2/{fichier1}')



        fichiers_png2 = obtenir_fichiers_png(dossier_a_surveiller2)
        if fichiers_png2:
            # Il y a de nouveaux fichiers
            for fichier in fichiers_png2:
                nom_fichier_sans_chemin = os.path.basename(fichier)
                # Exécuter le script avec le nom du fichier comme argument
                arg0 = nom_fichier_sans_chemin.split()[0]
                arg1 = nom_fichier_sans_chemin.split()[1]
                arg2 = nom_fichier_sans_chemin.split()[2]
                arg3 = nom_fichier_sans_chemin.split()[3]
                arg4 = nom_fichier_sans_chemin.split()[4]
                arg5 = nom_fichier_sans_chemin.split()[5]
                arg6 = nom_fichier_sans_chemin
                print(f'{arg0}')
                subprocess.run(["python3", "dino.py", arg0, arg1, arg2, arg3, arg4, arg5, arg6])
        else:
            print('Pas de nouveau trade')

        time.sleep(5)
        ecrire2('nb_pris.txt', len(fichiers_png2))
        miseajoursite('nb_pris.txt', 'nombre_trade_pris.txt')
        miseajoursite('gagnant.txt','nombre_trade_gagne.txt')
        miseajoursite('perdant.txt','nombre_trade_perdu.txt')
        miseajoursite('pourcent.txt','pourcent.txt')
        miseajoursite('plusgrosgain.txt', 'plus_gros_gain2.txt')
        miseajoursite('plusgrosseperte.txt', 'plus_grosse_perte2.txt')
        miseajoursite('dernierdf.txt', 'dernierdf.txt')
        miseajoursite('df.txt', 'df.txt')
    except :
        print('beug connection time out')