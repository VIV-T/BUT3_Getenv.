# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:33:31 2024

@author: e1735u
"""


# import 

"""
uniform = pour la génération de données float
randint = pour générerer un volume humain aléatoire pour la fréquentation des salles en période de cours.
"""
from random import uniform 
import pandas as pd
import datetime as dt
from random import random, randint
from math import log

"""
Classe appelée pour générer les données d'une journée. 
    => appelée en boucle quand la période dépasse un jour.

"""
class Generation_quotidienne():
    def __init__(self, granularite, date):
        self.data = None
        
        self.granularite = granularite

        ## Conditions exterieures et periodes
        self.date = date
        self.saison = self.get_saison()
        # initialisation des conditions extérieures
        self.temperature_ext = None
        self.humidity_ext = None
        self.set_conditions_ext()

        ## gestion du temps
        self.start_time = dt.datetime.combine(self.date, dt.datetime(2012,12,31,7,30,00).time())
        self.end_time = dt.datetime.combine(self.date, dt.datetime(2012,12,31,18,30,00).time())
        self.current_time = self.start_time
        # Maj de la periode de la journee
        self.day_period = self.get_day_period()
        
        # enregistrement des présence enregistrée dans la salle utlisé sur la période de la journée
        # Les salles sont vide la nuit jusqu'au debut des cours le matin
        self.liste_presence_salle = ["V"]
        self.end_crenau = dt.datetime(2012,12,31,8,00,00).time()
        self.current_presence = None
        self.volume_humain = 0

        # initialisation des variables relative à la gestion d'évènements
        self.current_events : list[str] = []
        
        ## initialisation des valeurs initiales : condition initiale pour une pièce vide
        # temperature (°C)
        self.temperature_min_vide = 17.0
        self.temperature_max_vide = 18.5
        self.temperature_min = self.temperature_min_vide
        self.temperature_max = self.temperature_max_vide
        
        # humidity (%)
        self.humidity_min_vide = 34.2
        self.humidity_max_vide = 35.7
        self.humidity_min = self.humidity_min_vide
        self.humidity_max = self.humidity_max_vide
        
        # CO2 (ppm)
        self.CO2_min_vide = 0
        self.CO2_max_vide = 20
        self.CO2_min = self.CO2_min_vide
        self.CO2_max = self.CO2_max_vide
        
        # TVoC (ppb)
        self.TVoC_min_vide = 0
        self.TVoC_max_vide = 5
        self.TVoC_min = self.TVoC_min_vide
        self.TVoC_max = self.TVoC_max_vide
        
        # noise (dB)
        self.noise_min_vide = 0
        self.noise_max_vide = 30
        self.noise_min = self.noise_min_vide
        self.noise_max = self.noise_max_vide
        
        
        # list for pandas df transformation
        self.time = []
        self.temperature = []        
        self.humidity = []          
        self.noise = []        
        self.people_detected = []
        self.CO2 = []
        self.TVoC =[]
        
        ## Boucle principale
        while self.current_time <= self.end_time :

            # on sort de la boucle pour éviter d'enregistrer des données du week end (IUT fermé)
            if self.date.isoweekday() == 6 and self.current_time.time() > dt.datetime(2012,12,31,12,30,00).time():
                break
            
            """ 
            Maj de la periode de la journée :
                en fonction de la periode de la journee => adapter la liste de présence dans les salles
            """
            if self.day_period != self.get_day_period() :
                # réinitialisation de la liste de scénario (cours)
                self.day_period = self.get_day_period()
                
                # print(self.day_period)
                self.liste_presence_salle = []
                
                if self.day_period == "midi" : 
                    # personne dans les salles le midi (en theorie)
                    self.liste_presence_salle = ["V"]
                    self.end_crenau = dt.datetime(2012,12,31,13,30,00).time()
                    self.define_new_freq(vide = True)
                    
                elif self.day_period == "pas_cours" : 
                    # personne dans les salles le soir après les cours
                    self.liste_presence_salle = ["V"]
                    self.end_crenau = dt.datetime(2012,12,31,19,30,00).time()
                    self.define_new_freq(vide = True)
                    
                elif self.day_period == "apres-midi" : 
                    self.end_crenau = dt.datetime(2012,12,31,15,20,00).time()
            
            
            ## écriture des données des capteurs 
            ## L'écriture des données soit modifiée en fonction des scénario.

            # Condition pour modifier la liste de présence toute les heure en fnoction de l'arbre de décision => methode "self.find_scenario()"
            if self.current_time.time() >= self.end_crenau : 
                #print(self.liste_presence_salle)
                self.find_scenario()
                #print(self.liste_presence_salle)
                self.end_crenau = (dt.datetime.combine(self.date, self.end_crenau) + dt.timedelta(hours=1)).time()
                #print(self.end_crenau)
            
            ### Ajout aléatoire d'évènements
            self.current_presence = self.liste_presence_salle[len(self.liste_presence_salle)-1]
            #print(self.current_events)
            if len(self.current_events) == 0 :
                # Appel de la fonction de generation aléatoire d'évènement.
                self.add_event()
            elif self.current_time.time() > self.end_event.time() :
                self.current_events.clear()
            # cas où un event est en cours
            else :
                self.apply_event_effect()
            
            
            ### Initialisation des nouveau seuil en fonction du volume humain dans la pièce en fonction du scénario de la journéee.
            # temperature
            self.set_new_scale_temperature()
            # humidity
            self.set_new_scale_humidity()
            # CO2
            self.set_new_scale_CO2()
            # TVoC
            self.set_new_scale_TVoC()
            # noise 
            self.set_new_scale_noise()
            
            
            
            ### generation & ecriture des nouvelles données
            # time 
            self.time.append(self.current_time)
            
            # temperature
            new_temperature = uniform(self.temperature_min, self.temperature_max)
            self.temperature.append(new_temperature)
            
            # humidity
            new_humidity = uniform(self.humidity_min, self.humidity_max)
            self.humidity.append(new_humidity)
            
            # people_detected
            if self.volume_humain > 0:
                self.people_detected.append(1)
            else :
                self.people_detected.append(0)
            
            # CO2
            new_CO2 = uniform(self.CO2_min, self.CO2_max)
            self.CO2.append(new_CO2)
            
            # TVoC
            new_TVoC = uniform(self.TVoC_min, self.TVoC_max)
            self.TVoC.append(new_TVoC)

            # noise
            new_noise = uniform(self.noise_min, self.noise_max)
            self.noise.append(new_noise)



            ## Gestion du temps à chaque itération
            # ajout de la granularité à chaque itération
            self.current_time = self.current_time + dt.timedelta(minutes=self.granularite)


        # construction du df pandas
        self.data = self.construct_df()
        
        
        
    # methode a appeler quand la generation quotidienne est terminée.
    def construct_df(self):
        # code pour transformer ces données en df pandas.
        self.dico_daily_data = {
            "time" : self.time,
            "temperature": self.temperature,
            "humidity" : self.humidity, 
            "noise" : self.noise, 
            "CO2" : self.CO2,
            "TVoC" : self.TVoC
        }
        return pd.DataFrame.from_dict(self.dico_daily_data)
        
        
    
    # Methode de classe permettant de renvoyer les données générées
    def get_data(self):
        return self.data
    
    
    
    ### obtenir la periode de la journée, la saison, et les condition exterieures associées.
    def get_day_period(self):
        if self.current_time.hour < 12 and self.current_time.time() >= dt.datetime(2012,12,31,8,00,00).time() :
            return "matin"
        elif self.current_time.time() >= dt.datetime(2012,12,31,13,30,00).time() and self.current_time.time() <= dt.datetime(2012,12,31, 17,20,00).time() :
            return "après-midi"
        elif self.current_time.time() > dt.datetime(2012,12,31,17,20,00).time() or self.current_time.time() <= dt.datetime(2012,12,31,8,00,00).time():
            return "pas_cours"
        else :
            return "midi"

    # obtenir la saison
    def get_saison(self):
        mois = self.date.month
        jour = self.date.day

        if mois == 12 or (mois == 1 and jour <= 20) or (mois == 2 and jour <= 18):
            return "Hiver"
        elif (mois == 3 and jour >= 20) or mois == 4 or mois == 5 or (mois == 6 and jour <= 20):
            return "Printemps"
        elif (mois == 7 and jour >= 22) or mois == 8 or mois == 9 or (mois == 10 and jour <= 22):
            return "Ete"
        else:
            return "Automne"

    # changement des conditions extérieures en fonction de la saison - valeur estimée (arbitraires pour avoir des données significative si possible)
    def set_conditions_ext(self):
        match self.saison :
            case "Printemps" :
                self.temperature_ext = 14
                self.humidity_ext = 75
            case "Ete" :
                self.temperature_ext = 22
                self.humidity_ext = 60
            case "Automne":
                self.temperature_ext = 12
                self.humidity_ext = 80
            case "Hiver":
                self.temperature_ext = 2
                self.humidity_ext = 65



    # Nouveau volume humain dans la piece
    def define_new_freq(self, vide : bool = False) :
        if vide == False :
            self.volume_humain = randint(15,35)
        else :
            self.volume_humain = 0
    
    

    # Methode de classe permettant de definir un scenario aléatoire en fonction de la day_periode
    # presence ou non d'humain dans la piece
    # fonction construite a partir d'un arbre décisionnel
    def find_scenario(self) :
        match len(self.liste_presence_salle) :
            # début de la journée / de l'après midi => premier crénau
            case 0 :
                p = random()
                if p > 0.5 : 
                    # il y a cours => "C"
                    self.liste_presence_salle.append("C")
                    # on definit le nouveau volume de personnes dans la salle 
                    self.define_new_freq()
                else :
                    # la salle est vide => "V"
                    self.liste_presence_salle.append("V")
            
            # second crénau
            case 1 :
                match self.liste_presence_salle[0] : 
                    case "C" :
                        self.liste_presence_salle.append("C")
                    case "V" :
                        p = random()
                        if p>0.2 :
                            self.liste_presence_salle.append("C")
                            self.define_new_freq()
                        else :
                            self.liste_presence_salle.append("V")
            
            # troisieme crénau
            case 2 :
                match (self.liste_presence_salle[0], self.liste_presence_salle[1]) :
                    # la salle était pleine
                    case ("C", "C") :
                        p = random()
                        # continuité des cours 
                        if p>0.5 :
                            self.liste_presence_salle.append("C")
                            "changement de cours => les BUT 3 VCOD quittent la salle et les BUT 2 EMS prennent place"
                            if p>0.8 :
                                # changement du volume de personne dans la salle 
                                self.define_new_freq()
                        else :
                            self.liste_presence_salle.append("V")
                            self.define_new_freq(vide=True)
                    
                    # la salle était vide 
                    case ("V", "V") :
                        p = random()
                        if p > 0.5 : 
                            # il y a cours => "C"
                            self.liste_presence_salle.append("C")
                            self.define_new_freq()
                        else :
                            # la salle est vide => "V"
                            self.liste_presence_salle.append("V")
                            
                    # cours de 3h => le cours continue
                    case ("V", "C") :
                        self.liste_presence_salle.append("C")
            
            # dernier crénau
            case 3 :
                match (self.liste_presence_salle[0], self.liste_presence_salle[1], self.liste_presence_salle[2]) :
                    case ("C", "C", "C") : 
                        p =random()
                        # déterminer si cours de 3-4h
                        if p>0.2 :
                            self.liste_presence_salle.append("C")
                        else :
                            self.liste_presence_salle.append("V")
                            self.define_new_freq(vide=True)
                    
                    case ("C", "C", "V") :
                        # les cours sont fini dans cette salle pour cette periode de la journee
                        self.liste_presence_salle.append("V")
                    
                    case ("V", "V", "V") : 
                        # les cours sont fini dans cette salle pour cette periode de la journee
                        self.liste_presence_salle.append("V")
                    
                    case ("V", "V", "C") : 
                        # contuinité du cours de 2h commencé
                        self.liste_presence_salle.append("C")
                        self.define_new_freq()
                        
                    case ("V", "C", "C") : 
                        # contuinité du cours de 2h commencé
                        self.liste_presence_salle.append("C")
            
            
        return self.liste_presence_salle
    
    
    
    
    # Methodes de classe : changement de la temperature en fonction du volume d'humain dans la pièce (fréquence)
    def set_new_scale_temperature(self):
        """
        augmentation non linéaire de la température : 
        modélisation avec l'équation suivante (estimée avec des ressources trouvées en ligne) :
        4*log(volume humain)+1  avec le logarithme en base 10
        """
        if self.volume_humain != 0 :            
            # utilisation du log en base 10
            pas_augmentation_temperature = 4*log(self.volume_humain,10)+1
            
            self.temperature_min = self.temperature_min_vide + pas_augmentation_temperature
            self.temperature_max = self.temperature_max_vide + pas_augmentation_temperature
        else : 
            self.temperature_min = self.temperature_min_vide
            self.temperature_max = self.temperature_max_vide


    # Methodes de classe : changement de l'humidity en fonction du volume d'humain dans la pièce (fréquence)
    def set_new_scale_humidity(self):
        """
        D'après nos recherches, l'humidité d'une pièce augmente de 3 à 5 % par personne dans la pièce jusqu'à un maximum de +10% (5 personnes ou plus - dans un cadre domestique)
        Ici, nous sommes dans des salles plus grandes (x2) que les pièces domestique, nous pouvons donc supposer que l'augmentation de l'humidité est légèrement modifiée :
        +1.5% par personne, +10% max avec 7 personnes dans la pièce.
        """
        if self.volume_humain>0 and self.volume_humain < 7 :
            pas_augmentation_humidity = self.volume_humain*1.5
            
            self.humidity_min = self.humidity_min_vide + pas_augmentation_humidity
            self.humidity_max = self.humidity_max_vide + pas_augmentation_humidity
            
        elif self.volume_humain >= 7 :
            pas_augmentation_humidity = 10
            
            self.humidity_min = self.humidity_min_vide + pas_augmentation_humidity
            self.humidity_max = self.humidity_max_vide + pas_augmentation_humidity
            
        else : 
            self.humidity_min = self.humidity_min_vide
            self.humidity_max = self.humidity_max_vide


    # Methodes de classe : changement du taux de CO2 en fonction du volume d'humain dans la pièce (fréquence)
    def set_new_scale_CO2(self):
        """
        augmentation linéaire de la concentration de CO2 (ppm) dans la pièce. Equation trouvée :
        CO2 = volume humain * 0.4 + 400
        """
        if self.volume_humain != 0 :  
            pas_augmentation_CO2 = 0.4*self.volume_humain+400
            
            self.CO2_min = self.CO2_min_vide + pas_augmentation_CO2
            self.CO2_max = self.CO2_max_vide + pas_augmentation_CO2
        else : 
            self.CO2_min = self.CO2_min_vide
            self.CO2_max = self.CO2_max_vide


    # Methodes de classe : changement du taux de TVoC en fonction du volume d'humain dans la pièce (fréquence)
    def set_new_scale_TVoC(self):
        """
        augmentation linéaire de la concentration de TVoC (ppb) dans la pièce. Equation trouvée :
        TVoC = volume humain * 0.4 + 40
        """
        if self.volume_humain != 0 :  
            pas_augmentation_TVoC_min = 0.4*self.volume_humain+25
            pas_augmentation_TVoC_max = 0.4*self.volume_humain+40
            
            self.TVoC_min = self.TVoC_min_vide + pas_augmentation_TVoC_min
            self.TVoC_max = self.TVoC_max_vide + pas_augmentation_TVoC_max
        else : 
            self.TVoC_min = self.TVoC_min_vide
            self.TVoC_max = self.TVoC_max_vide


    # Methodes de classe : changement du volume sonore en fonction du volume d'humain dans la pièce (fréquence)
    def set_new_scale_noise(self):
        """
        augmentation linéaire du noise (dB) dans la pièce. Equation trouvée : (arbitrairement)
        noise = volume humain * 0.4 + 40
        """
        if self.volume_humain != 0 :  
            pas_augmentation_noise = 0.4*self.volume_humain+20
            
            self.noise_min = self.noise_min_vide + pas_augmentation_noise
            self.noise_max = self.noise_max_vide + pas_augmentation_noise
        else : 
            self.noise_min = self.noise_min_vide
            self.noise_max = self.noise_max_vide
    


    # fonction d'ajout d'évènement en fonction de probabilité et condition particulière (parfois definies arbitrairement)
    def add_event(self):
        # évènements météo
            # a rajouter si possible


        # évènement dans le cas ou la pièce est occupée
        if self.current_presence == "C" :
            p = random()
            # temps de pause
            if ((self.current_time.time() >= dt.datetime(2012,12,31,10,00,00).time() and
                self.current_time.time() <= dt.datetime(2012,12,31,10,20,00).time())
                    or (self.current_time.time() >= dt.datetime(2012,12,31,13,20,00).time() and
                        self.current_time.time() <= dt.datetime(2012,12,31,13,35,00).time())
                    or (self.current_time.time() >= dt.datetime(2012,12,31,15,20,00).time() and
                        self.current_time.time() <= dt.datetime(2012,12,31,15,35,00).time())) and p>0.2 :
                self.current_events.append("open_window")
                open_window_time = randint(5,20)
                self.end_event = self.current_time + dt.timedelta(minutes=open_window_time)
            # ouverture de la fenetre pendant les cours en ete, printemps, et automne avec des proba différentes (arbitraires)
            elif (p>0.3 and self.saison == "Ete") or (p>0.7 and (self.saison == "Automne" or self.saison == "Printemps")):
                self.current_events.append("open_window")
                open_window_time = randint(5, 20)
                self.end_event = self.current_time + dt.timedelta(minutes=open_window_time)

            # proba d'avoir un travail de groupe pendant les cours.
            elif p<0.3 :
                self.current_events.append("travaux_grp")
                travaux_grp_time = randint(5, 20)
                self.end_event = self.current_time + dt.timedelta(minutes=travaux_grp_time)

        # dernière condition : appliquer les effets des évènements ajoutés
        if len(self.current_events) > 0 :
            self.apply_event_effect()


    # appel des fonction de modification de valeur en fonction des evènements en cours.
    def apply_event_effect(self):
        for event in self.current_events :
            match event  :
                case "open_window" :
                    #print('la fenetre est ouverte')
                    self.set_open_window_values()

                case "travaux_grp" :
                    #print('un travail de grp est en cours')
                    self.set_travaux_grp_values()


    # methode de modification des valeurs relevées quand la fenetre est ouverte
    def set_open_window_values(self):
        #print('la fenetre est maintenant ouverte !')

        ## temperature
        # cas ou la temperature est plus faible dehors
        if self.temperature_min > self.temperature_ext:
            self.temperature_min -= (self.temperature_min - self.temperature_ext) / 2
            self.temperature_max -= (self.temperature_max - self.temperature_ext) / 2

        # cas ou la temperature est plus elevée dehors
        elif self.temperature_max < self.temperature_ext:
            self.temperature_min += (self.temperature_ext - self.temperature_min) / 2
            self.temperature_max += (self.temperature_ext - self.temperature_max) / 2

        ## humidity
        # sachant que l'humidité en Lorraine est comprise entre 60 et 90% d'humidité => l'humidity intérieur va augmenter.
        # cas ou l'humidity est plus faible dehors
        if self.humidity_min > self.humidity_ext:
            self.humidity_min -= (self.humidity_min - self.humidity_ext) / 2
            self.humidity_max -= (self.humidity_max - self.humidity_ext) / 2

        # cas ou la temperature est plus elevée dehors
        elif self.humidity_max < self.humidity_ext:
            self.humidity_min += (self.humidity_ext - self.humidity_min) / 2
            self.humidity_max += (self.humidity_ext - self.humidity_max) / 2

        # Rajouter la réinitialisation des taux de CO2 et de TVoC
        self.CO2_min = self.CO2_min_vide
        self.CO2_max = self.CO2_max_vide

        self.TVoC_min = self.TVoC_min_vide
        self.TVoC_max = self.TVoC_max_vide


    # methode pour modifier les valeurs en cas de trvaux de grp
    def set_travaux_grp_values(self):
        # augmentation de la T°, et du noise.
        self.temperature_min += 2.5
        self.temperature_max += 2.5

        pas_augmentation_noise = 0.4 * self.volume_humain + 20

        self.noise_min = self.noise_min_vide + pas_augmentation_noise
        self.noise_max = self.noise_max_vide + pas_augmentation_noise
