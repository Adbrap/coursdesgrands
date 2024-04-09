import os
import time
import subprocess

# Chemin du dossier à surveiller
dossier_a_surveiller = "trouvailles"


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


fichiers_png = obtenir_fichiers_png(dossier_a_surveiller)
if fichiers_png:
    # Il y a de nouveaux fichiers
    for fichier in fichiers_png:
        nom_fichier_sans_chemin = os.path.basename(fichier)
        # Exécuter le script avec le nom du fichier comme argument
        arg0 = nom_fichier_sans_chemin.split()[0]
        arg1 = nom_fichier_sans_chemin.split()[1]
        arg2 = nom_fichier_sans_chemin.split()[2]
        arg3 = nom_fichier_sans_chemin.split()[3]
        arg4 = nom_fichier_sans_chemin.split()[4]
        print(f'{arg0}')
        subprocess.run(["python3", "dino.py", arg0, arg1, arg2, arg3, arg4])

