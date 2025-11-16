import socket
import threading
import csv

# Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

print(CYAN + "=== Harsh Fast Port Scanner (Multithreaded + Banner Grabbing) ===" + RESET)
target = input("Enter target IP or domain: ")

# Resolve domain to IP
try:
    target_ip = socket.gethostbyname(target)
    print(CYAN + "Scanning Target: " + target_ip + RESET)
except:
    print("Invalid domain name")
    exit()

open_ports = []
port_data = []
lock = threading.Lock()

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    try:
        s.connect((target_ip, port))

        try:
            service = socket.getservbyport(port)
        except:
            service = "Unknown"

        try:
            banner = s.recv(1024).decode(errors="ignore").strip()
            if banner == "":
                banner = "No banner"
        except:
            banner = "No banner"

        with lock:
            print(GREEN + "[OPEN] Port " + str(port) + " → " + service + " | Banner: " + banner + RESET)
            open_ports.append(port)
            port_data.append((port, service, banner))

    except:
        pass

    s.close()

# Input port range
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

print(CYAN + "Scanning ports " + str(start_port) + " to " + str(end_port) + " ..." + RESET)

threads = []

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(CYAN + "\nScan Complete ✔" + RESET)
print(CYAN + "Total Open Ports Found: " + str(len(open_ports)) + RESET)

# Save TXT
with open("scan_results.txt", "w") as f:
    f.write("Scan Results for " + target_ip + "\n")
    f.write("Port Range: " + str(start_port) + "-" + str(end_port) + "\n\n")
    for p, s, b in port_data:
        f.write("Port " + str(p) + " → " + s + " | Banner: " + b + "\n")

print(GREEN + "Saved to scan_results.txt" + RESET)

# Save CSV
with open("open_ports.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Port", "Service", "Banner"])
    for p, s, b in port_data:
        writer.writerow([p, s, b])

print(GREEN + "Saved to open_ports.csv" + RESET)

