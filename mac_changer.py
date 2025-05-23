#!usr/bin/env_python

import subprocess
import optparse
import re
import random
from datetime import datetime
import os
from colorama import init, Fore, Style
init(autoreset=True)

# checking whether the script is running as root
if os.geteuid() != 0:
    exit(Fore.RED + "[-] Please run as root")

def generate_random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0x00, 0xFF) for _ in range(5))

def is_valid_mac(mac):
    return re.match(r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$", mac) is not None

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m","--mac", dest="new_mac", help="New MAC address")
    parser.add_option("-r", "--random", action="store_true", dest="random_mac", help="Generate a random MAC address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error(Fore.RED + "[-] Please specify an interface, use --help for more info")
    elif not options.new_mac and options.random_mac:
        options.new_mac = generate_random_mac() 
    elif not options.new_mac and not options.random_mac:       
        parser.error(Fore.RED + "[-] Please specify a new mac, use --help for more info")
    elif not is_valid_mac(options.new_mac):
        parser.error(Fore.RED + "[-] Incorrect MAC format")
    
    return options
   

def change_mac(interface, new_mac):
    print(Fore.GREEN + "[+] Changing MAC address for " + interface + " to " + new_mac)

    subprocess.call(["ip", "link", "set", interface, "down"])
    subprocess.call(["ip", "link", "set", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", interface, "up"])



def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode('utf-8')
    mac_address_search_result = re.search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print(Fore.RED + "[-] Could not read MAC address")

def log_mac_change(interface, old_mac, new_mac):
    with open("mac_changer.log", "a") as log:
        log.write(f"[{datetime.now()}] Changed {interface} MAC from {old_mac} to {new_mac}\n")


options = get_arguments()
original_mac = get_current_mac(options.interface)
current_mac = get_current_mac(options.interface)
print("Current MAC address is "+ str(current_mac))

old_mac = current_mac
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if(current_mac == options.new_mac):
    print(Fore.GREEN + "[+] MAC address was successfully changed to " + current_mac)
    log_mac_change(options.interface, old_mac, current_mac) # logging on successful change
else:
    print(Fore.RED + "[-] MAC address did not get changed")
    with open("mac_changer.log", "a") as log: # logging when unsuccessful
        log.write(f"[{datetime.now()}] FAILED to change {options.interface} MAC from {old_mac} to {options.new_mac}\n")

