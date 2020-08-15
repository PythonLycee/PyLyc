"""
Copyright Franck CHEVRIER www.python-lycee.com
Fichier pour le démarrage des vidéos interactives
"""


import IPython
from IPython.display import display, HTML, YouTubeVideo
from time import sleep

class PL_video:
    
    def __init__(self,nom=None,ref=None):
        self.nom = nom #nom de la vidéo
        self.ref = ref #référence sur Youtube

#Définition de la bibliothèque des vidéos disponibles
Bibliotheque_videos=[
    PL_video(nom="Premiers pas en console et affectations de variables",ref="QD72fHg6rBI"),
    PL_video(nom="Écrire ses premières fonctions Python",ref="6PLkqM99NIE")]


def menu_choix_video(Bibliotheque_videos):
    """
    Fonction de choix dans la Bibliothèque des vidéos
    """
    insert_html=""
    
    #création de l'entête de l'affichage html
    insert_html +="""
    <head>
        <meta charset="UTF-8">
        <title> python-lycee choix vidéos </title>
    </head>
    """
    
    #création du corps de l'affichage html
    insert_html +="""
    <body>
        <h1 style=\"color: #EC8F11\">Vidéos disponibles</h1>
        <ol>
    """
    for vid in Bibliotheque_videos:
        insert_html +="<li style=\"color: #EDA647\">"+vid.nom+"</li>"
        
    insert_html +="""
        </ol>
    Saisir le numéro de la vidéo choisie :
    </body>
    """
    #Affichage html
    IPython.display.clear_output()
    display(HTML(insert_html) )
    
    #précaution d'attente pour que le input soit inséré après le html
    sleep(0.5)
    #choix de la video
    choix = -1
    while not 1<=choix<=len(Bibliotheque_videos): choix=int(input())
    
    #renvoi de la référence Youtube correspondante
    return Bibliotheque_videos[int(input())-1].ref
     
