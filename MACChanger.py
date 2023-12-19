#!/usr/bin/env python

import subprocess
import optparse
import os
import sys

def CheckSudo():
    if os.getuid() != 0:
        print("\nProgram must be run with root privileges!!")
        sys.exit(1)
        

def CreateParser():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    return parser.parse_args()
    
def InitializeValues(options):
    if options.interface is None or options.new_mac is None:
        result = subprocess.check_output(["ip", "addr"], text=True)
        result = result.split("\n")
        interfaces = []
        addresses = []
        for line in result:
            if (": <" in line):
                interfaces.append(line.split(" ")[1])
            elif ("link/" in line):
                addresses.append(line.split(" ")[5])

        for i in range(len(interfaces)):
            print(interfaces[i] + " " + addresses[i])
        if options.interface is None:
            interface = input("\nQue interfaz deseas cambiar? ")
        else:
            interface = options.interface
        if options.new_mac is None:
            value = input("\nIntroduce el nuevo valor: ")
        else:
            value = options.new_mac
        
    else:
        interface = options.interface
        value = options.new_mac
    return (interface,value)

def ChangeMAC(interface, value):
    print("[+] Changing MAC of "+ interface + " for the new value " + value)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", value])
    subprocess.call(["ifconfig", interface, "up"])

### ----------------------MAIN------------------------------------------

try:
    CheckSudo()
    (options, arguments) = CreateParser()
    (interface, mac) = InitializeValues(options)
    ChangeMAC(interface, mac)
except KeyboardInterrupt:
    print('\n[-] CTRL+C detected. Exiting...')
    sys.exit(0)