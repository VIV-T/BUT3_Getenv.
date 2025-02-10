# Pour un scan bluetooth traditionnel (=> pour les appareils pouvant être apairé)
import bluetooth
# Pour scanner les appareil 'bluetooth low energy'
from bluetooth.ble import DiscoveryService


print("Scanning for bluetooth devices...")

# Scan traditionnel
devices = bluetooth.discover_devices(lookup_names = True)

# Scan BLE 
service = DiscoveryService()
devices_ble = service.discover(2)

print(f"- Traditionnal scan : {len(devices)} devices found !")
print(f"- BLE scan : {len(devices_ble)} devices found !")

for addr, name in devices :
	print(f"{name} : {addr}")


for addr, name in devices_ble.items() :
	print(f"{name} : {addr}")