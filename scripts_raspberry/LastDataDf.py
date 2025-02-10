# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 09:35:24 2024

@author: e1735u
"""
import random

import pandas as pd
import datetime as dt
import time


class LastDataDf():
    def __init__(self, delta_sec : int):
        self.df = pd.DataFrame(
            {"time": [], "temperature": [], "humidity": [], "noise": [], "isPeopleDetected": [], "TVoC": [],
             "CO2eq": []})
        self.delta_sec = delta_sec


    def append_new_row(self, dico_new_row):
        ## Suppression des anciennes lignes (plus à jour) en fonction du self.delta_sec
        index_old_rows_list = self.df.index[self.df['time'] < dico_new_row["time"][0] - dt.timedelta(seconds=self.delta_sec)].tolist()
        self.delete_old_rows(index_old_rows_list)

        ## Ajout de la nouvelle ligne
        new_row = pd.DataFrame(dico_new_row)
        # ignore_index est ici important pour pouvoir ensuite agir sur les index du df (suppression de ligne par exemple)
        self.df = pd.concat([self.df, new_row], ignore_index=True)


    def get_df(self):
        return self.df


    def get_aggregate(self):
        aggregats = dict(self.df.aggregate("mean"))
        # la présence vaut soit 0, soit 1, si une personne a été detectée sur l'intervalle de temps des valeurs du df, la valeur de ce champs est set à 1
        if aggregats["isPeopleDetected"] > 0:
            aggregats["isPeopleDetected"] = 1
        return aggregats

    def delete_old_rows(self, index_list):
        self.df = self.df.drop(index=index_list)


"""
last = LastDataDf(delta_sec=20)
import random
for i in range(20):
    x = random.randint(0,1000)
    last.append_new_row(
        {"time": [dt.datetime.now()], "temperature": [x], "humidity": [x], "noise": [x], "isPeopleDetected": [x],
         "TVoC": [x], "CO2eq": [x]})
    print(len(last.get_df().iloc[:,1]))
    d = last.get_aggregate()
    print(d)
    del d["time"]
    print(d)
    time.sleep(2)

print(last.get_df())
"""
