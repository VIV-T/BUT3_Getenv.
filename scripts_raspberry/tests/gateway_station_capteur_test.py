
import time
import datetime as dt
from lib.ledstick.ledStick import GroveLedStick 
from lib.sensorSound.sensorSound import GroveSoundSensor
from lib.buttonLED.buttonLED import GroveButtonLed
from lib.sensorDHT.sensorDHT import GroveDHTSensor
from lib.sensorPIR.sensorPIR import GrovePirMotionSensor
from lib.sensorAirquality.sensorAirquality import GroveAirQualitySensor
from lib.buzzer.buzzer import GroveBuzzer

from LastDataDf import LastDataDf


class Gateway:
	def __init__(self):
		print("Initialisation de la passerelle")

		### Initialisation du dataframe de la classe LastDataDf contenant les valeurs des 20 dernière sec
		self.last_data_df_20_sec = LastDataDf(delta_sec=20)
		self.dico_new_row = {"time": [], "temperature": [], "humidity": [], "noise": [], "isPeopleDetected": [], "TVoC": [], "CO2eq": []}

		### Initialisation pour l'écriture du fichier CSV
		self.liste_entete =["time", "temperature", "humidity", "noise", "isPeopleDetected", "TVoC", "CO2eq", "alerte_aeration", "alerte_intrusion", "alerte_incendie"]
		self.alerte_aeration = False
		self.alerte_intrusion = False
		self.alerte_incendie = False
		self.last_time_writing = None
		# creation d'un autre df contenant cette fois les valeurs des 3 dernières minutes => utile pour l'écriture.
		self.delta_time_writing  = 5 # temps en secondes
		self.last_data_df_180_sec = LastDataDf(delta_sec=self.delta_time_writing)
		with open("all_data.csv", "w") as f:
			f.write(";".join(self.liste_entete)+"\n")

		#### Initialisation des capteurs ####
		# ledStick
		self.LEDStick = GroveLedStick(12,10)	
		self.numberLedStickLED=-1
		# sound sensor 
		self.soundSensor = GroveSoundSensor(0)
		self.noise = 0 
		# temperature & humidity
		self.DHTSensor = GroveDHTSensor(26)
		self.humidity = 0
		self.temperature = 0
		# buttonLED - on ne se sert que d'un seul LedButton.
		self.bLed1 = GroveButtonLed(6,5) 
		# PIR sensor & sa valeur
		self.PIRsensor = GrovePirMotionSensor(18)
		# AirQuality Sensor
		self.AirQualitySensor = GroveAirQualitySensor()
		# Buzzer
		self.BuzzerAlert = GroveBuzzer(22)

		self.etat = 0
		self.alerte_etat_1 = False
		self.alerte_etat_2 = False
		# on set le temps restant avant l'alerte (etat_2) à None
		self.time_alerte_etat_2 = None



	def inputUpdate(self):
		#print("Mise à jour des entrées")

		# Récupération du temps actuel
		self.current_datetime =dt.datetime.now()

		##### Recuperation INPUT des capteurs #####
		# Capteur volume sonore
		self.noise = self.soundSensor.getRawSensorValue()
		# Température & humidity
		self.DHTSensor.getRawSensorValue()
		self.humidity = round(self.DHTSensor.humidity(),2)
		self.temperature = round(self.DHTSensor.temperature(),2)
		# Détecteur de mvmt
		self.isPeopleDetected = self.PIRsensor.getSensorValue()
		# Airquality sensor
		self.AirQualitySensor.getRawSensorValue()
		self.TVoC = self.AirQualitySensor.TVoC()
		self.CO2eq = self.AirQualitySensor.CO2eq()
		# Button LED - statuts des 2 boutons
		self.b1_status = self.bLed1.getStatusButton()

		print(f"statut du bouton : {self.b1_status}")


		## Formatage pour écriture dans les df de la classe LastDataDf
		self.dico_new_row["time"].append(self.current_datetime)
		self.dico_new_row["temperature"].append(self.temperature)
		self.dico_new_row["humidity"].append(self.humidity)
		self.dico_new_row["noise"].append(self.noise)
		self.dico_new_row["isPeopleDetected"].append(self.isPeopleDetected)
		self.dico_new_row["TVoC"].append(self.TVoC)
		self.dico_new_row["CO2eq"].append(self.CO2eq)


		##### Integration des dernières données dans les df pandas de la classe LastDataDf #####
		self.last_data_df_20_sec.append_new_row(self.dico_new_row)
		self.last_data_df_180_sec.append_new_row(self.dico_new_row)
		# réinitialisation du dico_new_row pour la prochaine itération
		self.dico_new_row = {"time": [], "temperature": [], "humidity": [], "noise": [], "isPeopleDetected": [], "TVoC": [], "CO2eq": []}

		# Tests
		#print(self.last_data_df_20_sec.get_df())
		#print(self.last_data_df_180_sec.get_df())



	def inputProcessing(self):
		# adaptation des entrées (modification format)
		#print("Traitement des entrées")
		#print(self.isPeopleDetected)

		### Récuperation des moyennes depuis le df de la classe LastDataDf
		self.dico_aggregats_20 = self.last_data_df_20_sec.get_aggregate()
		# temperature (°C)
		self.moyenne_temperature = round(self.dico_aggregats_20["temperature"], 2)
		# humidity (%)
		self.moyenne_humidity = round(self.dico_aggregats_20["humidity"], 2)
		# taux de CO2 (ppm)
		self.moyenne_CO2eq = round(self.dico_aggregats_20["CO2eq"],2)
		# taux de TVoC (ppb)
		self.moyenne_TVoC = round(self.dico_aggregats_20["TVoC"], 2)
		# noise (unité ?)
		self.moyenne_noise = round(self.dico_aggregats_20["noise"], 2)
		# isPeopleDetected (0/1)
		self.moyenne_isPeopleDetected = round(self.dico_aggregats_20["isPeopleDetected"], 2)



	def graph(self):
		# scenario + traitement
		#print("Graph d'état")
		print(self.etat)
		

		# changement de l'etat du systeme des que l'IUT ferme : le soir et le dimanche
		if self.current_datetime.isoweekday() == 7 or self.current_datetime.time() > dt.datetime(2024,1,1,18,30,00).time() :
			self.etat = 2
		# cas du samedi
		elif self.current_datetime.isoweekday() == 6 and self.current_datetime.time() > dt.datetime(2024,1,1,12,30,00).time() :
			self.etat = 2

		# changement d'état dès que le bouton est appuyé et relaché
		if self.etat == 0 :
			# on éteint le buzzer sur le changement d'état = cas de désactivation mannuelle de l'alerte.
			self.BuzzerAlert.off()
			self.time_alerte_etat_2 = None
			# quand le bouton est enfoncé => changer d'état
			if self.b1_status == 0 :
				self.etat = 1
				# on return "self.etat" pour gagner en performance (on évite de parcourir les conditions restantes)
				return self.etat
		elif self.etat == 1 :
			# quand le bouton est enfoncé => changer d'état
			if self.b1_status == 1 :
				self.etat = 2
				return self.etat
		# cas ou l'iut est fermé ou que tout le monde est hors du bâtiment (le dernier à partir appuie sur le bouton = passage des capteurs en alarme)
		elif self.etat == 2 :
			# quand le bouton est enfoncé => changer d'état
			if self.b1_status == 0 and self.current_datetime.isoweekday() != 7 :
				if self.alerte_etat_2 :
					self.LEDStick.LedRGB_AllOFF()
				self.etat = 3
				return self.etat
			# cas de la nuit => rétabli a zero le matin (ouverture de l'IUT) sauf le dimanche
			#elif self.current_datetime.isoweekday() != 7 and self.current_datetime.time() > dt.datetime(2024,1,1,7,30,00).time() :
				#self.etat = 0
		elif self.etat == 3 :
			# quand le bouton est enfoncé => changer d'état
			if self.b1_status == 1 :
				self.etat = 0
				return self.etat




	def outputProcessing(self):
		# adaptation des variables pour les sorties
		#print("Traitement des sorties")

		#### Dépend de l'état du système ####
		if self.etat == 0 :
			### Modification valeur rgb ledStick
			## Temperature
			# échelle de couleur entre bleu (froid) et rouge (chaud)
			var_temperature = (19-self.moyenne_temperature)*35
			if var_temperature < 0 :
				self.red_temperature = int(255)
				self.blue_temperature = int(0)
				self.green_temperature = int(255+var_temperature)
				if self.green_temperature < 0 :
					self.green_temperature = 0
					self.alerte_etat_1 =True
					self.alerte_aeration = True
			else :
				self.blue_temperature = int(0+var_temperature)
				if self.blue_temperature > 255 :
					self.blue_temperature = int(255)
				self.red_temperature = int(255-var_temperature)
				if self.red_temperature < 0 :
					self.red_temperature = int(0)
				self.green_temperature = int(255)


			## Humidity
			var_humidity = (60-self.moyenne_humidity)*5
			# Cas où l'aération est nécessaire
			if self.moyenne_humidity >= 80 :
				self.red_humidity = int(255)
				self.green_humidity = int(0)
				self.blue_humidity = int(0)
				self.alerte_etat_1 =True
				self.alerte_aeration = True


			elif var_humidity < 0 :
				self.red_humidity = int(255)
				self.blue_humidity = int(0)
				self.green_humidity = int(255+var_humidity)
				if self.green_humidity < 0 :
					self.green_humidity = 0

			else :
				self.blue_humidity = int(0+var_humidity)
				if self.blue_humidity > 255 :
					self.blue_humidity = int(255)
				self.red_humidity = int(255-var_humidity)
				if self.red_humidity < 0 :
					self.red_humidity = int(0)
				self.green_humidity = int(255)



			## Taux de  TVoC
			# Si inferieur au seuil : vert
			# Si seuil intermédiaire : orange
			# sinon : rouge
			if self.moyenne_TVoC < 300 :
				self.red_TVoC = int(0)
				self.blue_TVoC = int(0)
				self.green_TVoC = int(160)
			elif self.moyenne_TVoC < 750 and self.moyenne_TVoC >= 300:
				self.red_TVoC = int(255)
				self.blue_TVoC = int(0)
				self.green_TVoC = int(75)
			else :
				self.red_TVoC = int(255)
				self.blue_TVoC = int(0)
				self.green_TVoC = int(0)
				self.alerte_etat_1 = True
				self.alerte_aeration = True


			## Taux de CO2eq
			# Si inferieur au seuil : vert
                        # Si seuil intermédiaire : orange
                        # sinon : rouge
			if self.moyenne_CO2eq < 800 :
				self.red_CO2 = int(0)
				self.blue_CO2 = int(0)
				self.green_CO2 = int(160)
			elif self.moyenne_CO2eq < 1500 and self.moyenne_CO2eq >= 800:
				self.red_CO2 = int(255)
				self.blue_CO2 = int(0)
				self.green_CO2 = int(75)
			else :
				self.red_CO2 = int(255)
				self.blue_CO2 = int(0)
				self.green_CO2 = int(0)
				self.alerte_etat_1 = True
				self.alerte_aeration = True


		# etat 2 = IUT fermé (nuit ou Dimanche)
		elif self.etat == 2 :
			### Note, il ne faut pas déclencher l'alerte tout de suite, s'il s'agit d'un personnel autorisé, il faut laisser un temps pour désactiver l'alarme.
			# D'où l'utilisation de la variable "self.time_alerte"

			# si presence == 1 | si bruit moyen au-dessus d'un seuil => alerte (intrusion)
			# valeur arbitraire ici pour le self.noise
			if self.moyenne_isPeopleDetected == 1 or self.moyenne_noise > 150 :
				self.alerte_etat_2 = True
				if self.time_alerte_etat_2 == None :
					# on laisse 1min30 à la personne détectée pour désactiver l'alarme avant qu'elle ne se déclenche (buzzer)
					self.time_alerte_etat_2 = self.current_datetime + dt.timedelta(seconds=90)
				elif self.time_alerte_etat_2 <= self.current_datetime :
					self.alerte_intrusion = True

			if self.moyenne_temperature > 65 :
				self.alerte_etat_2 = True
				self.alerte_incendie = True
				if self.time_alerte_etat_2 == None :
					self.time_alerte_etat_2 = self.current_datetime + dt.timedelta(seconds=10)


			### Revoir les seuils pour les particule, le CO2 et la temperature.
			# si temperature au-dessus d'un seuil => alerte (incendie)
			# si taux de particule superieur à un seuil => alerte (incendie ou fuite de gaz)


	def outputUpdate(self):
		#print("Traitement des sorties")

		##### Ecriture dans le fichier csv - historique des données  #####
		## Indépendemment de l'état du systeme ##
		# On réinitialise la liste d'input pour qu'elle ne contienne
		# que les valeurs de cette itération
		if self.last_time_writing == None or self.current_datetime >= self.last_time_writing + dt.timedelta(seconds= self.delta_time_writing) :
			self.last_time_writing = self.current_datetime

			self.liste_input_CSV = []
			# convertir la valeur de time() renvoyée par python
			self.liste_input_CSV.append(str(dt.datetime.now()))
			# recuperation des valeurs moyennes du df self.last_data_df_180_sec
			dico_writing_values = self.last_data_df_180_sec.get_aggregate()
			for value in dico_writing_values.values() :
				self.liste_input_CSV.append(str(round(value,2)))
			self.liste_input_CSV.append(str(self.alerte_aeration))
			self.liste_input_CSV.append(str(self.alerte_intrusion))
			self.liste_input_CSV.append(str(self.alerte_incendie))
			self.alerte_aeration = False
			self.alerte_intrusion = False
			self.alerte_incendie = False


			print(self.etat)
			print(self.liste_input_CSV)
			# écriture dans le CSV de la nouvelle ligne contenant les données moyennes selon la granularité voulue.
			with open("all_data.csv", "a") as f:
				f.write(";".join(self.liste_input_CSV)+"\n")


		## Maj du buzzer & du LedStick
		## Dépend de l'état du système ##

		if self.etat == 0 :
			self.LEDStick.LedRGB_ON(0, self.red_temperature, self.green_temperature, self.blue_temperature)
			self.LEDStick.LedRGB_ON(2, self.red_humidity, self.green_humidity, self.blue_humidity)
			self.LEDStick.LedRGB_ON(4, self.red_CO2, self.green_CO2, self.blue_CO2)
			self.LEDStick.LedRGB_ON(6, self.red_TVoC, self.green_TVoC, self.blue_TVoC)

			# Si l'une des valeurs relevées dépasse un certain seuil : déclencher une alerte
			if self.alerte_etat_1 :
				self.alerte(tuple_LED_alerte=(8,9))
				# remise du bool d'alerte à False
				self.alerte_etat_1 = False

		elif self.etat == 2 :
			if self.alerte_etat_2 :
				if self.current_datetime >= self.time_alerte_etat_2 :
					self.alerte(tuple_LED_alerte = (0,1,2,3,4,5,6,7,8,9), nuit=True)
					# on ne remet pas l'état d'alerte à False => pour laisser sonner un max
				else :
					self.LEDStick.LedRGB_AllON(255,0,0)




	def alerte(self, tuple_LED_alerte : tuple = (9), nuit = False ):
		self.BuzzerAlert.on()
		for num_LED in tuple_LED_alerte :
			self.LEDStick.LedRGB_ON(num_LED, 255,0,0)
		# Si on est la nuit et que l'alerte est donnée, le buzzer continuera de bipper jusqu'à désactivation mannuelle
		#if not nuit :
		time.sleep(0.2)
		self.BuzzerAlert.off()
		for num_LED in tuple_LED_alerte :
			self.LEDStick.LedRGB_OFF(num_LED)
