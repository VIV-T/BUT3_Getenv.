import time
import buzzer

BuzzerAlert = buzzer.GroveBuzzer(22)
BuzzerAlert.on()
time.sleep(1.0)
BuzzerAlert.off()
