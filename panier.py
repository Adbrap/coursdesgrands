import os
import time
import subprocess

# Chemin du dossier à surveiller
dossier_a_surveiller = "trouvailles"

# Liste des fichiers actuels dans le dossier
fichiers_actuels = set(os.listdir(dossier_a_surveiller))

while True:
    # Liste des fichiers dans le dossier à surveiller
    fichiers_nouveaux = set(os.listdir(dossier_a_surveiller))

    # Vérifier s'il y a de nouveaux fichiers
    nouveaux_fichiers = fichiers_nouveaux - fichiers_actuels

    if nouveaux_fichiers:
        # Il y a de nouveaux fichiers
        for fichier in nouveaux_fichiers:
            # Exécuter le script avec le nom du fichier comme argument
            arg0 = fichier.split()[0]
            arg1 = fichier.split()[1]
            arg2 = fichier.split()[2]
            arg3 = fichier.split()[3]
            arg4 = fichier.split()[4]
            subprocess.run(["python3", "dino.py", arg0, arg1, arg2, arg3, arg4])

        # Mettre à jour la liste des fichiers actuels
        fichiers_actuels = fichiers_nouveaux

    # Attendre un certain temps avant de vérifier à nouveau
    time.sleep(300)
