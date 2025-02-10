import time
from gateway import Gateway

print("Initialisation de l'application")
passerelleObject = Gateway()
print("Lancement de l'application")

while True:
	print("---------------")
	passerelleObject.inputUpdate()
	passerelleObject.inputProcessing()
	passerelleObject.graph()
	passerelleObject.outputProcessing()
	passerelleObject.outputUpdate()
