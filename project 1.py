import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ==============================
# Utility Functions
# ==============================

def get_system_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "Unable to get IP"

# ==============================
# Port Scanning Logic
# ==============================

class PortScanner:
    
    def __init__(self, target, start_port, end_port, output_widget):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.output_widget = output_widget
        self.running = True

    def log(self, message):
        self.output_widget.insert(tk.END, message + "\n")
        self.output_widget.see(tk.END)

    def scan(self):
        try:
            target_ip = socket.gethostbyname(self.target)
        except:
            self.log("Invalid Target ❌")
            return
        
        self.log("="*60)
        self.log(f"Target: {self.target} ({target_ip})")
        self.log(f"System IP: {get_system_ip()}")
        self.log(f"Scanning Ports: {self.start_port} - {self.end_port}")
        self.log(f"Started at: {datetime.now()}")
        self.log("="*60)

        open_ports = []

        for port in range(self.start_port, self.end_port + 1):
            if not self.running:
                break
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)
                
                result = sock.connect_ex((target_ip, port))
                
                if result == 0:
                    open_ports.append(port)
                    self.log(f"[OPEN] Port {port}")
                
                sock.close()

            except:
                pass

        self.log("="*60)
        self.log("Scan Completed ✔")
        self.log(f"Total Open Ports: {len(open_ports)}")
        self.log("="*60)

# ==============================
# GUI Application
# ==============================

class ScannerApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Network Port Scanner")
        self.root.geometry("750x600")
        self.root.configure(bg="#1e1e1e")

        self.create_widgets()

    def create_widgets(self):
        
        title = tk.Label(self.root, text="CYBER SECURITY PORT SCANNER",
                         font=("Arial", 18, "bold"), fg="white", bg="#1e1e1e")
        title.pack(pady=10)

        ip_label = tk.Label(self.root,
                            text=f"Your System IP: {get_system_ip()}",
                            fg="cyan", bg="#1e1e1e")
        ip_label.pack()

        frame = tk.Frame(self.root, bg="#1e1e1e")
        frame.pack(pady=10)

        tk.Label(frame, text="Target:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)
        self.target_entry = tk.Entry(frame, width=25)
        self.target_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Start Port:", fg="white", bg="#1e1e1e").grid(row=1, column=0, padx=5)
        self.start_port_entry = tk.Entry(frame, width=10)
        self.start_port_entry.grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="End Port:", fg="white", bg="#1e1e1e").grid(row=2, column=0, padx=5)
        self.end_port_entry = tk.Entry(frame, width=10)
        self.end_port_entry.grid(row=2, column=1, sticky="w")

        self.scan_btn = tk.Button(self.root, text="Start Scan",
                                 command=self.start_scan,
                                 bg="green", fg="white", width=15)
        self.scan_btn.pack(pady=5)

        self.stop_btn = tk.Button(self.root, text="Stop Scan",
                                 command=self.stop_scan,
                                 bg="red", fg="white", width=15)
        self.stop_btn.pack(pady=5)

        self.output = tk.Text(self.root, height=25, width=85,
                              bg="black", fg="lime")
        self.output.pack(pady=10)

        scrollbar = ttk.Scrollbar(self.root, command=self.output.yview)
        self.output.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def start_scan(self):
        target = self.target_entry.get()
        
        if target == "":
            messagebox.showerror("Error", "Enter target")
            return
        
        try:
            start_port = int(self.start_port_entry.get())
            end_port = int(self.end_port_entry.get())
        except:
            messagebox.showerror("Error", "Invalid port range")
            return

        self.output.delete(1.0, tk.END)

        self.scanner = PortScanner(target, start_port, end_port, self.output)
        
        self.thread = threading.Thread(target=self.scanner.scan)
        self.thread.start()

    def stop_scan(self):
        try:
            self.scanner.running = False
            self.output.insert(tk.END, "\nScan Stopped by User ❌\n")
        except:
            pass

# ==============================
# Run Application
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()
