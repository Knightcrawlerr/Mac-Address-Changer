#!/usr/bin/python3

import subprocess
import sys
from argparse import *
import re
from termcolor import cprint, colored

def get_arg():
    parser = ArgumentParser()
    parser.add_argument("-m", "--mac", dest="mac", help="Enter the MAC Address")
    parser.add_argument("-i", "--interface", dest="interface", help="Enter the Interface to be changed")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


def get_interface():
    interface_dict = {"1": "wlan0", "2": "eth0"}
    interface_value = input(colored("Welcome to MAC Address Changer", "magenta") + colored("\n[+] Choose the "
                                                                                           "interface below\n(1) "
                                                                                           "wlan0 \n(2) eth0\n(3) "
                                                                                           "Other\n=>", "blue"))

    if interface_value == "3":
        custom_interface = input("Enter the interface\n=>")
        return custom_interface

    elif interface_value not in ["1", "2"]:
        print("Enter Correct Value")

    else:
        return interface_dict.get(interface_value)


def mac_changer(interface, new_mac):
    subprocess.call(["ip", "link", "set", interface, "down"])
    subprocess.call(["ip", "link", "set", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", interface, "up"])


def get_mac(interface):
    ip_result = subprocess.check_output(["ip", "address", "show", interface]).decode()
    result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ip_result)
    return result.group(0)


def main():
    try:
        mac = get_arg()
        interface = mac.interface

        if not mac.interface:
            interface = get_interface()

        mac_changer(interface, mac.mac)
        res_mac = get_mac(interface)

        if res_mac == mac.mac:
            cprint("[+] MAC Address was successfully changed to " + mac.mac, "green")
        else:
            cprint("[-] MAC Address did not get changed", "red")
    except KeyboardInterrupt:
        cprint("\nProgram Terminated\nCause: keyboard interruption", "red")


main()
