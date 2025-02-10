import time
import buttonLED

bLed1 = buttonLED.GroveButtonLed(6,5)
bLed2 = buttonLED.GroveButtonLed(17,16)

bLed1.setStatusLed(0)
bLed2.setStatusLed(0)
time.sleep(1.0)
bLed1.setStatusLed(1)
bLed2.setStatusLed(1)

while True:
	status_b1 = bLed1.getStatusButton()
	bLed1.setStatusLed(not(status_b1))
	status_b2 = bLed2.getStatusButton()
	bLed2.setStatusLed(not(status_b2))
	print("Status Button : ", str(status_b1) + " " + str(status_b2))
	time.sleep(0.2)
