import subprocess
import argparse
import re

def get_arguments() -> argparse.Namespace:
    """
    Parses and returns command-line arguments.
    
    :return: Namespace object containing interface and new_mac attributes.
    """
    parser = argparse.ArgumentParser(
        description="Automated MAC Address Changer Utility for Linux Systems"
    )
    parser.add_argument(
        "-i", "--interface", 
        dest="interface", 
        required=True, 
        help="Target network interface (e.g., eth0, wlan0)"
    )
    parser.add_argument(
        "-m", "--mac", 
        dest="new_mac", 
        required=True, 
        help="New MAC address to assign (format: XX:XX:XX:XX:XX:XX)"
    )
    return parser.parse_args()

def validate_mac(mac_address: str) -> bool:
    """
    Validates whether the provided string matches standard MAC address syntax.
    
    :param mac_address: MAC address string to validate.
    :return: True if valid, False otherwise.
    """
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(pattern, mac_address))

def change_mac(interface: str, new_mac: str) -> None:
    """
    Executes system commands to modify the MAC address of a network interface.
    
    :param interface: Name of the target network interface.
    :param new_mac: Desired MAC address.
    """
    print(f"[*] Disabling network interface: {interface}")
    subprocess.run(["ip", "link", "set", "dev", interface, "down"], check=True)

    print(f"[*] Setting MAC address of {interface} to {new_mac}")
    subprocess.run(["ip", "link", "set", "dev", interface, "address", new_mac], check=True)

    print(f"[*] Re-enabling network interface: {interface}")
    subprocess.run(["ip", "link", "set", "dev", interface, "up"], check=True)

def main() -> None:
    args = get_arguments()

    if not validate_mac(args.new_mac):
        print("[-] Error: Invalid MAC address format. Please use XX:XX:XX:XX:XX:XX.")
        return

    try:
        change_mac(args.interface, args.new_mac)
        print(f"[+] Successfully changed MAC address to {args.new_mac} on {args.interface}.")
    except subprocess.CalledProcessError as e:
        print(f"[-] Command Execution Error: {e}")
        print("[-] Ensure you are running this script with root privileges (sudo).")
    except Exception as e:
        print(f"[-] Unexpected error encountered: {e}")

if __name__ == "__main__":
    main()
