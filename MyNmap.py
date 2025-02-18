import os
import re
import sys
import time
import signal
import platform
import subprocess
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()

# Constants
OUTPUT_DIR = "scan_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color shortcuts
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
CYAN = Fore.CYAN
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

# Global process variable for cleanup
process = None

# ------------------------------
# Helper Functions
# ------------------------------
def print_header():
    print(f"""{CYAN} Created By: CyberPantheon
   


                            ███╗   ███╗██╗   ██╗███╗   ██╗███╗   ███╗ █████╗ ██████╗ 
                            ████╗ ████║╚██╗ ██╔╝████╗  ██║████╗ ████║██╔══██╗██╔══██╗
                            ██╔████╔██║ ╚████╔╝ ██╔██╗ ██║██╔████╔██║███████║██████╔╝
                            ██║╚██╔╝██║  ╚██╔╝  ██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝ 
                            ██║ ╚═╝ ██║   ██║   ██║ ╚████║██║ ╚═╝ ██║██║  ██║██║     
                            ╚═╝     ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
                                                                                     
   Simplifying your favorite Network mapper ...                                                                                                                           

{RESET}""")


def print_error(message):
    """Print error messages in red."""
    print(f"{RED}[!] ERROR: {message}{RESET}")

def print_success(message):
    """Print success messages in green."""
    print(f"{GREEN}[✓] {message}{RESET}")

def print_warning(message):
    """Print warning messages in yellow."""
    print(f"{YELLOW}[!] WARNING: {message}{RESET}")

def validate_ip(ip):
    """Validate an IP address or CIDR range."""
    pattern = r"^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$"
    if not re.match(pattern, ip):
        raise ValueError(f"Invalid IP/CIDR: {ip}")

def generate_filename(extension):
    """Generate a unique filename with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.abspath(os.path.join(OUTPUT_DIR, f"scan_{timestamp}.{extension}"))

def check_root():
    """Check if the script is running with root privileges."""
    if platform.system() != "Windows" and os.geteuid() != 0:
        print_error("This scan requires root privileges. Use 'sudo'.")
        exit()

def handle_interrupt(signal, frame):
    """Handle Ctrl+C interruptions gracefully."""
    global process
    if process:
        process.kill()
    print_error("Scan interrupted. Exiting...")
    exit()
    





# ------------------------------
# Nmap Execution
# ------------------------------

import subprocess
import sys

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def run_nmap(command):
    """Run the Nmap command and display real-time output with color formatting."""
    global process

    # Ensure verbose mode (-v) is always included
    if "-v" not in command:
        command.append("-v")

    print(f"\n{BOLD}{CYAN}>>> Running Nmap Scan: {' '.join(command)} <<<{RESET}\n")

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # Print output in real time with a neat format
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(format_output(output.strip()))

        # Check for errors
        stderr = process.stderr.read()
        if stderr:
            print_error(stderr.strip())

    except Exception as e:
        print_error(f"Failed to run Nmap: {e}")
    finally:
        process = None

def format_output(line):
    """Format Nmap output with colors and structure."""
    if "open" in line:
        return f"{GREEN}[+] {line}{RESET}"
    elif "closed" in line:
        return f"{RED}[-] {line}{RESET}"
    elif "filtered" in line:
        return f"{YELLOW}[!] {line}{RESET}"
    elif "Nmap scan report for" in line:
        return f"\n{BOLD}{CYAN}{line}{RESET}"
    elif "Starting Nmap" in line:
        return f"{BOLD}{CYAN}{line}{RESET}"
    elif "Host is up" in line:
        return f"{GREEN}{line}{RESET}"
    elif "Host seems down" in line:
        return f"{RED}{line}{RESET}"
    elif "MAC Address" in line:
        return f"{CYAN}{line}{RESET}"
    else:
        return line

def print_error(message):
    """Print error messages in red."""
    print(f"{RED}[ERROR] {message}{RESET}", file=sys.stderr)



# AGGRESIVENESS AND OUTPUT 


def ask_timing():
    """Ask the user for scan timing/aggressiveness."""
    print(f"{BOLD}\n=== Timing/Aggressiveness ==={RESET}")
    print("1. Paranoid (-T0)")
    print("2. Sneaky (-T1)")
    print("3. Polite (-T2)")
    print("4. Normal (-T3)")
    print("5. Aggressive (-T4)")
    print("6. Insane (-T5)")
    print("7. Skip (Use default timing)")

    choice = input(f"{CYAN}Choose an option (1-7): {RESET}")
    if choice == "7":
        return None
    elif choice in ["1", "2", "3", "4", "5", "6"]:
        return f"-T{int(choice) - 1}"
    else:
        print_error("Invalid choice. Using default timing.")
        return None

def ask_output():
    """Ask the user for output format."""
    print(f"{BOLD}\n=== Output Format ==={RESET}")
    print("1. Save output to file")
    print("2. Skip (No output file)")

    choice = input(f"{CYAN}Choose an option (1-2): {RESET}")
    if choice == "2":
        return None

    print(f"{BOLD}\n=== File Format ==={RESET}")
    print("1. Normal (-oN)")
    print("2. XML (-oX)")
    print("3. Grepable (-oG)")
    print("4. All formats (-oA)")

    format_choice = input(f"{CYAN}Choose an option (1-4): {RESET}")
    if format_choice == "1":
        return "-oN", generate_filename("txt")
    elif format_choice == "2":
        return "-oX", generate_filename("xml")
    elif format_choice == "3":
        return "-oG", generate_filename("grep")
    elif format_choice == "4":
        return "-oA", generate_filename("all")
    else:
        print_error("Invalid choice. Skipping output file.")
        return None
# ------------------------------
# Menu System
# ------------------------------

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print_header()
        print(f"{BOLD}1. Host Discovery{RESET}")
        print(f"{BOLD}2. Port Scanning{RESET}")
        print(f"{BOLD}3. Service/Version Detection{RESET}")
        print(f"{BOLD}4. OS Detection{RESET}")
        print(f"{BOLD}5. Script Scanning (NSE){RESET}")
        print(f"{BOLD}6. Firewall/IDS Evasion{RESET}")
        print(f"{BOLD}7. Traceroute{RESET}")
        print(f"{BOLD}8. Aggressive Scan{RESET}")
        print(f"{BOLD}9. Custom Scan{RESET}")
        print(f"{BOLD}10. Quick Scans{RESET}")  # New option
        print(f"{BOLD}11. Exit{RESET}")

        choice = input(f"{CYAN}Choose an option (1-11): {RESET}")
        if choice == "1":
            host_discovery()
        elif choice == "2":
            port_scanning()
        elif choice == "3":
            service_detection()
        elif choice == "4":
            os_detection()
        elif choice == "5":
            script_scanning()
        elif choice == "6":
            firewall_evasion()
        elif choice == "7":
            traceroute()
        elif choice == "8":
            aggressive_scan()
        elif choice == "9":
            custom_scan()
        elif choice == "10":
            quick_scans()  # New option
        elif choice == "11":
            print_success("Exiting...")
            exit()
        else:
            print_error("Invalid choice. Try again.")

# ------------------------------
# Submenus
# ------------------------------
def quick_scans():
    """Quick scan presets."""
    print(f"{BOLD}\n=== Quick Scans ==={RESET}")
    print("1. Network Survey (-sn -T4)")
    print("2. Full Audit (-A -T4)")
    print("3. Back")

    choice = input(f"{CYAN}Choose an option (1-3): {RESET}")
    if choice == "3":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1/24): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.extend(["-sn", "-T4"])
    elif choice == "2":
        command.extend(["-A", "-T4"])
    else:
        print_error("Invalid choice.")
        return

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])

    command.append(target)
    run_nmap(command)

#HOST DISCOVERY 

def host_discovery():
    """Host discovery submenu."""
    print(f"{BOLD}\n=== Host Discovery ==={RESET}")
    print("1. ARP Scan (-PR)")
    print("2. TCP SYN Ping (-PS)")
    print("3. TCP ACK Ping (-PA)")
    print("4. UDP Ping (-PU)")
    print("5. ICMP Echo Ping (-PE)")
    print("6. Back")

    choice = input(f"{CYAN}Choose an option (1-6): {RESET}")
    if choice == "6":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1/24): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("-PR")
    elif choice == "2":
        command.append("-PS")
    elif choice == "3":
        command.append("-PA")
    elif choice == "4":
        command.append("-PU")
    elif choice == "5":
        command.append("-PE")
    else:
        print_error("Invalid choice.")
        return
      # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])

  
    command.append(target)
    run_nmap(command)
    
    
    
    
    
    
    
 #PORT SCANNING   

def port_scanning():
    """Port scanning submenu."""
    print(f"{BOLD}\n=== Port Scanning ==={RESET}")
    print("1. TCP SYN Scan (-sS)")
    print("2. TCP Connect Scan (-sT)")
    print("3. UDP Scan (-sU)")
    print("4. NULL Scan (-sN)")
    print("5. FIN Scan (-sF)")
    print("6. Xmas Scan (-sX)")
    print("7. Back")

    choice = input(f"{CYAN}Choose an option (1-7): {RESET}")
    if choice == "7":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("-sS")
    elif choice == "2":
        command.append("-sT")
    elif choice == "3":
        command.append("-sU")
    elif choice == "4":
        command.append("-sN")
    elif choice == "5":
        command.append("-sF")
    elif choice == "6":
        command.append("-sX")
    else:
        print_error("Invalid choice.")
        return
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command.append(target)
    run_nmap(command)







#service detection
def service_detection():
    """Service/version detection submenu."""
    print(f"{BOLD}\n=== Service/Version Detection ==={RESET}")
    print("1. Basic Version Detection (-sV)")
    print("2. Version Intensity (--version-intensity <0-9>)")
    print("3. Light Mode (--version-light)")
    print("4. All-out Detection (--version-all)")
    print("5. Back")

    choice = input(f"{CYAN}Choose an option (1-5): {RESET}")
    if choice == "5":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("-sV")
    elif choice == "2":
        intensity = input(f"{CYAN}Enter intensity (0-9): {RESET}")
        command.extend(["-sV", f"--version-intensity={intensity}"])
    elif choice == "3":
        command.extend(["-sV", "--version-light"])
    elif choice == "4":
        command.extend(["-sV", "--version-all"])
    else:
        print_error("Invalid choice.")
        return
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command.append(target)
    run_nmap(command)







#OS DETECTION

def os_detection():
    """OS detection submenu."""
    print(f"{BOLD}\n=== OS Detection ==={RESET}")
    print("1. Enable OS Detection (-O)")
    print("2. Max OS Tries (--max-os-tries <number>)")
    print("3. Back")

    choice = input(f"{CYAN}Choose an option (1-3): {RESET}")
    if choice == "3":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("-O")
    elif choice == "2":
        max_tries = input(f"{CYAN}Enter max OS tries (1-9): {RESET}")
        command.extend(["-O", f"--max-os-tries={max_tries}"])
    else:
        print_error("Invalid choice.")
        return
    
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command.append(target)
    run_nmap(command)
    
    
    
    
    
    
    
 #SCRIPT SCANNING:
 
def script_scanning():
    """Script scanning submenu."""
    print(f"{BOLD}\n=== Script Scanning (NSE) ==={RESET}")
    print("1. Default Scripts (-sC)")
    print("2. Vulnerability Detection (--script vuln)")
    print("3. Exploit Detection (--script exploit)")
    print("4. Safe Scripts (--script safe)")
    print("5. Custom Script (--script <name/path>)")
    print("6. Back")

    choice = input(f"{CYAN}Choose an option (1-6): {RESET}")
    if choice == "6":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("-sC")
    elif choice == "2":
        command.extend(["--script", "vuln"])
    elif choice == "3":
        command.extend(["--script", "exploit"])
    elif choice == "4":
        command.extend(["--script", "safe"])
    elif choice == "5":
        script_name = input(f"{CYAN}Enter script name/path: {RESET}")
        command.extend(["--script", script_name])
    else:
        print_error("Invalid choice.")
        return
    
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command.append(target)
    run_nmap(command)
    
    
    
    
    
    
    
    
    
    
    #FIREWALL / IDS EVASION   
def firewall_evasion():
    """Firewall/IDS evasion submenu."""
    print(f"{BOLD}\n=== Firewall/IDS Evasion ==={RESET}")
    print("1. Fragment Packets (-f)")
    print("2. Specify MTU (--mtu <size>)")
    print("3. Decoy IPs (-D <decoy1,decoy2>)")
    print("4. Spoof Source IP (-S <ip>)")
    print("5. Spoof Source Port (--source-port <port>)")
    print("6. Append Random Data (--data-length <bytes>)")
    print("7. Back")

    choice = input(f"{CYAN}Choose an option (1-7): {RESET}")
    if choice == "7":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("-f")
    elif choice == "2":
        mtu = input(f"{CYAN}Enter MTU size (e.g., 24): {RESET}")
        command.extend(["--mtu", mtu])
    elif choice == "3":
        decoys = input(f"{CYAN}Enter decoy IPs (comma-separated): {RESET}")
        command.extend(["-D", decoys])
    elif choice == "4":
        spoof_ip = input(f"{CYAN}Enter source IP to spoof: {RESET}")
        command.extend(["-S", spoof_ip])
    elif choice == "5":
        spoof_port = input(f"{CYAN}Enter source port to spoof: {RESET}")
        command.extend(["--source-port", spoof_port])
    elif choice == "6":
        data_length = input(f"{CYAN}Enter data length (bytes): {RESET}")
        command.extend(["--data-length", data_length])
    else:
        print_error("Invalid choice.")
        return
    
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command.append(target)
    run_nmap(command)
    
    
    
    


#TRACEROUTE

def traceroute():
    """Traceroute submenu."""
    print(f"{BOLD}\n=== Traceroute ==={RESET}")
    print("1. Enable Traceroute (--traceroute)")
    print("2. Traceroute Port (--traceroute-port <port>)")
    print("3. Max Hops (--max-hops <number>)")
    print("4. Back")

    choice = input(f"{CYAN}Choose an option (1-4): {RESET}")
    if choice == "4":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return

    command = ["nmap"]
    if choice == "1":
        command.append("--traceroute")
    elif choice == "2":
        port = input(f"{CYAN}Enter traceroute port: {RESET}")
        command.extend(["--traceroute-port", port])
    elif choice == "3":
        max_hops = input(f"{CYAN}Enter max hops: {RESET}")
        command.extend(["--max-hops", max_hops])
    else:
        print_error("Invalid choice.")
        return
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command.append(target)
    run_nmap(command)



#AGGRESIVE SCAN 

def aggressive_scan():
    """Aggressive scan submenu."""
    print(f"{BOLD}\n=== Aggressive Scan ==={RESET}")
    print("1. Enable Aggressive Mode (-A)")
    print("2. Back")

    choice = input(f"{CYAN}Choose an option (1-2): {RESET}")
    if choice == "2":
        return

    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command = ["nmap", "-A", target]
    run_nmap(command)




#CUSTOM SCAN 

def custom_scan():
    """Custom scan submenu."""
    print(f"{BOLD}\n=== Custom Scan ==={RESET}")
    print("Enter custom Nmap flags (e.g., -sS -f -D decoy1,decoy2)")
    flags = input(f"{CYAN}Enter flags: {RESET}")
    target = input(f"{CYAN}Enter target (e.g., 192.168.1.1): {RESET}")
    try:
        validate_ip(target)
    except ValueError as e:
        print_error(str(e))
        return
    
     # Ask for timing/aggressiveness
    timing = ask_timing()
    if timing:
        command.append(timing)

    # Ask for output format
    output = ask_output()
    if output:
        command.extend([output[0], output[1]])
        
    command = ["nmap"] + flags.split() + [target]
    run_nmap(command)



    
    
    
    
    
    
    
    
    
    
    





# ------------------------------
# Main Execution
# ------------------------------

if __name__ == "__main__":
    # Register interrupt handler
    signal.signal(signal.SIGINT, handle_interrupt)

    # Check if Nmap is installed
    #if not shutil.which("nmap"):
       # print_error("Nmap is not installed. Please install it first.")
        #exit()

    # Start the main menu
    main_menu()
