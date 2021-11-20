#!/usr/bin/env python

from pymodbus.client.sync import ModbusTcpClient
import ipaddress
from pymodbus.exceptions import *
from pymodbus import mei_message
import sys
import threading

def checkgateway(ip):
    valid = False
    highestTested = 0
    # Check two lowest and most common unit numbers
    for unit in [0, 1]:
        if attemptconnection(ip, unit):
            valid = True
            highestTested = unit
            break

    if not valid:
        return False

    Endpoints.append(ip)

    for unit in range(highestTested + 1, 256):
        attemptconnection(ip, unit)


def attemptconnection(ip, unit):
    try:
        client = ModbusTcpClient(ip)
        response = client.read_holding_registers(0, 1, unit=unit)
        rq = mei_message.ReadDeviceInformationRequest(unit=unit, read_code=0x03)
        devInfo = client.execute(rq)
        if 'information' in vars(devInfo).keys():
            try:
                print(f'{ip} unit {unit} device information: {" ".join([x.decode() for x in devInfo.information.values()])}')
            except UnicodeDecodeError:
                print(f'{ip} unit {unit}: Device Information Retrieved But unable to be decoded. Printing in Sequence and removing'
                      f' invalid entries...')
                for i in devInfo.information.values():
                    try:
                        print(i.decode())
                    except UnicodeDecodeError:
                        pass
        else:
            if 'registers' in vars(response).keys():
                print(f'\r{ip} unit {unit} register 0: {response.registers}     ')
            else:
                return False
                #print(f'\r{ip}: Error. Unable to read holding registers')

        return True
    except ConnectionException:
        return False


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
        # Scuffed implementation of limiting running threads
        while threading.activeCount() >= 5:
            pass

        try:
            print(f'Testing... {ip}', end="\r")
            threading.Thread(target=checkgateway, args=(ip,)).start()

        except KeyboardInterrupt:
            break


    while threading.activeCount() > 1:
        pass
    # Print Valid endpoints found
    print(f'\n\nScan Complete. {len(Endpoints)} Found')

    for i in Endpoints:
        print(i)

