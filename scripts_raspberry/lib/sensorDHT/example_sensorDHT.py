import time
import sensorDHT

DHTSensor = sensorDHT.GroveDHTSensor(26)
humidity = 0
temperature = 0

while True:
	DHTSensor.getRawSensorValue()
	humidity = int(DHTSensor.humidity())
	temperature = int(DHTSensor.temperature())
	print(str(humidity) + " " + str(temperature))
	time.sleep(2.0)
