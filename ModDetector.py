from pymodbus.client.sync import ModbusTcpClient
import ipaddress
from pymodbus.exceptions import *
import sys


if __name__ == '__main__':
    Endpoints = []
    IPs = []
    Subnet = ''

    print('''-------------------------------------------------------------------------------
 #     #               ######                                                 
 ##   ##  ####  #####  #     # ###### ##### ######  ####  #####  ####  #####  
 # # # # #    # #    # #     # #        #   #      #    #   #   #    # #    # 
 #  #  # #    # #    # #     # #####    #   #####  #        #   #    # #    # 
 #     # #    # #    # #     # #        #   #      #        #   #    # #####  
 #     # #    # #    # #     # #        #   #      #    #   #   #    # #   #  
 #     #  ####  #####  ######  ######   #   ######  ####    #    ####  #    # 
-------------------------------------------------------------------------------''')

    # Check valid number of arguments
    if len(sys.argv) == 2:
        # Print help text
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print('''Usage: python3 ModDetector.py [-h] [Subnet]''')
            quit()

        # Load Subnet as a variable
        Subnet = sys.argv[1]
    else:
        print('Invalid Arguments. Format python3 ModDetector.py [Subnet]')

    # Try to generate ip list from subnet
    try:
        IPs = [str(ip) for ip in ipaddress.IPv4Network(Subnet)]
    except ipaddress.AddressValueError:
        print('Invalid Subnet')
        quit()

    except:
        print('Error resolving Subnet')
        quit()

    print('Beginning Scan...')

    # Iterate over IPs in the subnet, and print ones with valid responses
    for ip in IPs:
        print(f'Testing... {ip}', end="\r")
        try:
            client = ModbusTcpClient(ip)
            print(f'{ip}: {client.read_holding_registers(11)}')
            Endpoints.append(ip)

        except ConnectionException:
            continue

        except KeyboardInterrupt:
            break

    # Print Valid endpoints found
    print(f'\n\nScan Complete. {len(Endpoints)} Found')

    for i in Endpoints:
        print(i)