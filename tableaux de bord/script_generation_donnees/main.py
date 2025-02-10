# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 12:45:20 2024

@author: e1735u
"""


"""
Note : 
Le but est de generer un script .py parametrable par l'utilisateur qui genere des données aléatoirement.

On se limite a une plage horaire entre 8h et 18h30 (horaire de fermeture de l'IUT).
l'utilisateur doit pouvoir paramétrer les points suivants :
    - la granularité des données (minute - 15 min - h ?)
    - la période sur laquelle il souhaite generer ces données (plusieur jours ? - mois ? - plus ?)
    - Optionnel : la saison ou il génère ces données (printemps - ete - automne - hivers )

Une fois ces parametres donnés au script : générer des données selon des "scénarios" aléatoires :
    - présence d'un cours dans une salle.
    - fenêtre ouverte ou non ?
    - autres idées...?
    
"""

# import des pâckages nécessaires.
from Scenario import Scenario
    
    

"""
Code principal a run :
    prend les input utilisateur pour renvoyer un tableau de données a envoyer a Power BI
"""
if __name__=="__main__" :
    # initialisation des variable d'input à 0
    granularite = 0
    periode = 0

    # demander les input à l'utilisateur
    valid_input_granularite = False
    while not valid_input_granularite:
        try:
            granularite = int(input("Quelle est la granularité des données souhaitée ? (nombre entier de minutes entre 5 et 60)\n"))
            if granularite >= 5 and granularite <= 60:
                valid_input_granularite = True
        except ValueError:
            print("Veuillez rentrer une granularité valide !\n")

    valid_input_period = False
    while not valid_input_period:
        try:
            periode = int(input("Sur quelle période souhaiter vous générer les données ? (nombre entier de jours)\n"))
            if periode > 0 :
                valid_input_period = True
        except ValueError:
            print("Veuillez rentrer un période valide ! (nombre de jours supérieur à 0)\n")


    scenario = Scenario(granularite, periode)


    # écriture dans un fichier csv
    df_data = scenario.get_data()

    df_data.to_csv('tableau_donnees.csv', index=False)
    
    
    