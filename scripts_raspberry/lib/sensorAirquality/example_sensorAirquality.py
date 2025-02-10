import time
import sensorAirquality

AirQualitySensor = sensorAirquality.GroveAirQualitySensor()
TVoC = 0
CO2eq = 0

while True:
	AirQualitySensor.getRawSensorValue()
	TVoC = AirQualitySensor.TVoC()
	CO2eq = AirQualitySensor.CO2eq()
	print(str(TVoC) + " " + str(CO2eq))
	time.sleep(0.5)
