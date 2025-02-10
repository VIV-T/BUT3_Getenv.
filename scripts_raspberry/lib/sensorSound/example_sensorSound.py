import time
import sensorSound

SoundSensor = sensorSound.GroveSoundSensor(0)
noise = 0

while True:
	noise = SoundSensor.getRawSensorValue()
	print(str(noise))
	time.sleep(0.05)
