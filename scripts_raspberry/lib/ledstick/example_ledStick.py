import time
import ledStick

LEDStick = ledStick.GroveLedStick(12,10)

while True:
	for i in range(10):
		LEDStick.LedRGB_ON(i, 0, 0, 255)
		time.sleep(0.3)
	
	LEDStick.LedRGB_AllOFF()
	time.sleep(1.0)

	LEDStick.LedRGB_AllON(0,255,0)
	time.sleep(1.0)
