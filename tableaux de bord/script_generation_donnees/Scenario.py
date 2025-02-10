# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:33:03 2024

@author: e1735u
"""

from Generation_quotidienne import Generation_quotidienne
import pandas as pd
import datetime as dt

"""
Cette classe permet de générer des données en fonction de scénario établis.
Rajouter la possibilité d'avoir des scénario pré-établis.

""" 
class Scenario():
    def __init__(self, granularite : int, periode : int):
        # obtention de la date du jour
        self.start_date = dt.datetime.now().date()
        #dt.datetime.now().date() permet d'obtenir l'heure courante
        
        # la granularité s'exprime en minutes (int)
        self.granularite = granularite
        
        # la periode s'exprime en jours (int)
        self.periode = periode
        self.data : None | pd.DataFrame = None
        
        self.liste_donnees_quotidienne = []
        
        self.date =self.start_date
        
        for i in range(self.periode) : 
            generation_quotidienne = Generation_quotidienne(self.granularite, self.date)
            self.liste_donnees_quotidienne.append(generation_quotidienne.get_data())
            # gestion du cas du week end (on le passe car nous sommes ici intérréssé par les donées d'une semaine de cours classiques)
            # samedi soir -> lundi matin (au cas ou)
            if self.date.isoweekday() == 6 :
                self.date += dt.timedelta(days=2)
            # reste du temps
            else : 
                self.date += dt.timedelta(days=1)
            
        
        self.data_uniformisation()
            
            
    def get_granularite(self) :
        return self.granularite
    
    def data_uniformisation(self):
        """
        uniformiser les tableau de données recupérés dans "self.liste_données_quotidienne"
        en 1 seul tableau de données.
            => concaténation de tous les df pandas en 1 seul -> utilisation de la fonction concat() de pandas
        """
        self.data = pd.concat(self.liste_donnees_quotidienne)
        
        
    # Recupération des données formatées dans un df pandas après la fonction self.data_uniformisation
    def get_data(self) :
        return self.data