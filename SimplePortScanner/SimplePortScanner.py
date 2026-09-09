import socket
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Dictionary mapping common port numbers to their standard network service names.
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"
}

def grab_banner(target_ip: str, port: int) -> str | None:
    """
    Attempts to perform banner grabbing on an open port to identify 
    the service or software version running on the remote host.
    
    :param target_ip: IP address of the target machine.
    :param port: The open TCP port number.
    :return: Received banner string if available, otherwise None.
    """
    try:
        # Initialize an IPv4 TCP Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((target_ip, port))
        
        # Send basic payloads to trigger a response depending on the port type
        if port in [80, 8080, 443]:
            s.send(b"HEAD / HTTP/1.1\r\nHost: target\r\n\r\n")
        else:
            s.send(b"Hello\r\n")
            
        # Receive up to 1024 bytes of response data
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        return banner if banner else None
    except Exception:
        return None

def scan_port(target_ip: str, port: int, timeout: float) -> None:
    """
    Scans a single TCP port on the target IP address. If the port is open,
    it identifies the common service and attempts to grab the service banner.
    
    :param target_ip: Resolved IPv4 address.
    :param port: Port number to scan.
    :param timeout: Connection timeout in seconds.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        
        # connect_ex returns 0 if the connection attempt succeeded (port open)
        result = s.connect_ex((target_ip, port))
        s.close()

        if result == 0:
            service = COMMON_SERVICES.get(port, "Unknown Service")
            banner = grab_banner(target_ip, port)
            
            banner_info = f" | Banner: {banner}" if banner else ""
            print(f"[+] Port {port:5d}/TCP : OPEN ({service}){banner_info}")
            
    except Exception:
        pass

def main() -> None:
    # Command-Line Argument Parser Configuration
    parser = argparse.ArgumentParser(
        description="Fast Multi-Threaded TCP Port Scanner with Banner Grabbing"
    )
    parser.add_argument("-t", "--target", required=True, help="Target IP or hostname (e.g. scanme.nmap.org)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (e.g., 1-100 or 80,443). Default: 1-1024")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Number of concurrent worker threads. Default: 50")
    parser.add_argument("--timeout", type=float, default=0.5, help="Socket timeout in seconds. Default: 0.5")
    
    args = parser.parse_args()

    # Parse port input formats (supports ranges like '1-100' or explicit lists like '80,443')
    ports_to_scan = []
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports_to_scan = range(start, end + 1)
    elif "," in args.ports:
        ports_to_scan = [int(p) for p in args.ports.split(",")]
    else:
        ports_to_scan = [int(args.ports)]

    # Resolve target hostname to IPv4 address
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[-] Error: Could not resolve hostname '{args.target}'.")
        return

    print("=" * 60)
    print(f" Target: {args.target} ({target_ip})")
    print(f" Ports: {args.ports} | Threads: {args.workers} | Timeout: {args.timeout}s")
    print(f" Scan Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Execute concurrent port scanning using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        for port in ports_to_scan:
            executor.submit(scan_port, target_ip, port, args.timeout)

    print("=" * 60)
    print(f" Scan Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
