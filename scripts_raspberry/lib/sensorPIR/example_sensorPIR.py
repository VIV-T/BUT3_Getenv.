import time
import sensorPIR

PIRsensor = sensorPIR.GrovePirMotionSensor(18)
isPeopleDetected = 0

while True:
	isPeopleDetected = PIRsensor.getSensorValue()
	print (str(isPeopleDetected))
	time.sleep(0.1)
