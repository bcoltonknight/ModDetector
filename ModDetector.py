from pymodbus.client.sync import ModbusTcpClient
import ipaddress
from pymodbus.exceptions import *
import sys

Endpoints = []
IPs = []
Subnet = ''

if len(sys.argv) == 2:
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('''Usage: python3 ModDetector.py [-h] [Subnet]''')
        quit()
    Subnet = sys.argv[1]
else:
    print('Invalid Arguments. Format python3 ModDetector.py [Subnet]')

try:
    IPs = [str(ip) for ip in ipaddress.IPv4Network(Subnet)]
except ipaddress.AddressValueError:
    print('Invalid Subnet')

print('Beginning Scan...')

for ip in IPs:
    try:
        client = ModbusTcpClient(ip)
        print(f'{ip}: {client.read_holding_registers(11)}')
        Endpoints.append(ip)

    except ConnectionException:
        continue

    except KeyboardInterrupt:
        quit()

print(f'Scan Complete. {len(Endpoints)} Found')

for i in Endpoints:
    print(i)
