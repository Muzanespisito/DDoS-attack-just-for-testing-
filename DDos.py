import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import threading
import random
import time
from datetime import datetime

class NetworkLearningTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Protocol Learning Tool - By Muzan")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Beautiful purple color scheme
        self.colors = {
            "bg_dark": "#0f0820",  # Deep purple-black
            "bg_primary": "#1a1029",
            "bg_secondary": "#2d1b42",
            "bg_tertiary": "#3d2963",
            "text_primary": "#e6d5ff",
            "text_secondary": "#b39ddb",
            "accent_purple": "#9c4dff",
            "accent_lavender": "#c77dff",
            "button": "#7b1fa2",
            "button_hover": "#9c27b0",
            "success": "#4caf50",
            "error": "#ff5252",
            "warning": "#ffb74d",
            "info": "#29b6f6"
        }
        
        # Configure root window
        self.root.configure(bg=self.colors["bg_dark"])
        
        # Set window icon
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        # Variables
        self.is_running = False
        self.packet_count = 0
        self.request_history = []
        
        self.create_gui()
        self.setup_styles()
        
    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Purple.TFrame', background=self.colors["bg_primary"])
        style.configure('Secondary.TFrame', background=self.colors["bg_secondary"])
        
        style.configure('Title.TLabel',
                       background=self.colors["bg_primary"],
                       foreground=self.colors["accent_lavender"],
                       font=('Arial', 18, 'bold'))
        
        style.configure('Normal.TLabel',
                       background=self.colors["bg_primary"],
                       foreground=self.colors["text_primary"],
                       font=('Arial', 10))
        
        style.configure('Purple.TButton',
                       background=self.colors["button"],
                       foreground='white',
                       borderwidth=0,
                       font=('Arial', 10, 'bold'),
                       padding=10)
        style.map('Purple.TButton',
                 background=[('active', self.colors["button_hover"])])
        
        style.configure('Accent.TButton',
                       background=self.colors["accent_purple"],
                       foreground='white',
                       borderwidth=0,
                       font=('Arial', 10, 'bold'),
                       padding=10)
        style.map('Accent.TButton',
                 background=[('active', self.colors["accent_lavender"])])
        
    def create_gui(self):
        """Create the main GUI layout"""
        # Main container with gradient effect
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header frame with author info
        header_frame = tk.Frame(main_container, bg=self.colors["bg_primary"], height=100)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Title and author label
        title_label = tk.Label(header_frame,
                              text="🌐 Network Protocol Learning Tool",
                              font=('Arial', 24, 'bold'),
                              bg=self.colors["bg_primary"],
                              fg=self.colors["accent_lavender"])
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        author_label = tk.Label(header_frame,
                               text="Created by Muzan - For Educational Purposes Only",
                               font=('Arial', 10, 'italic'),
                               bg=self.colors["bg_primary"],
                               fg=self.colors["text_secondary"])
        author_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Request Tab
        request_tab = ttk.Frame(notebook, style='Purple.TFrame')
        notebook.add(request_tab, text="📡 Request Simulator")
        self.create_request_tab(request_tab)
        
        # History Tab
        history_tab = ttk.Frame(notebook, style='Purple.TFrame')
        notebook.add(history_tab, text="📊 Request History")
        self.create_history_tab(history_tab)
        
        # Learning Tab
        learn_tab = ttk.Frame(notebook, style='Purple.TFrame')
        notebook.add(learn_tab, text="📚 Protocol Guide")
        self.create_learning_tab(learn_tab)
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_request_tab(self, parent):
        """Create the request simulation tab"""
        # Input Frame
        input_frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        input_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Target IP
        tk.Label(input_frame, text="Target IP:", 
                bg=self.colors["bg_primary"],
                fg=self.colors["text_primary"],
                font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        
        self.ip_entry = tk.Entry(input_frame, width=25, font=('Arial', 11),
                                bg=self.colors["bg_secondary"],
                                fg=self.colors["text_primary"],
                                insertbackground=self.colors["text_primary"])
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)
        self.ip_entry.insert(0, "127.0.0.1")
        
        tk.Label(input_frame, text="Port:", 
                bg=self.colors["bg_primary"],
                fg=self.colors["text_primary"],
                font=('Arial', 11, 'bold')).grid(row=0, column=2, sticky='w', pady=10, padx=(20,0))
        
        self.port_entry = tk.Entry(input_frame, width=10, font=('Arial', 11),
                                  bg=self.colors["bg_secondary"],
                                  fg=self.colors["text_primary"],
                                  insertbackground=self.colors["text_primary"])
        self.port_entry.grid(row=0, column=3, padx=10, pady=10)
        self.port_entry.insert(0, "8080")
        
        # Protocol Selection
        tk.Label(input_frame, text="Protocol:", 
                bg=self.colors["bg_primary"],
                fg=self.colors["text_primary"],
                font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=10)
        
        self.protocol_var = tk.StringVar(value="TCP")
        protocol_frame = tk.Frame(input_frame, bg=self.colors["bg_primary"])
        protocol_frame.grid(row=1, column=1, columnspan=3, sticky='w', pady=10)
        
        tcp_btn = tk.Radiobutton(protocol_frame, text="TCP (Connection-based)",
                                variable=self.protocol_var, value="TCP",
                                bg=self.colors["bg_primary"],
                                fg=self.colors["text_primary"],
                                selectcolor=self.colors["bg_secondary"],
                                activebackground=self.colors["bg_primary"],
                                font=('Arial', 10))
        tcp_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        udp_btn = tk.Radiobutton(protocol_frame, text="UDP (Connectionless)",
                                variable=self.protocol_var, value="UDP",
                                bg=self.colors["bg_primary"],
                                fg=self.colors["text_primary"],
                                selectcolor=self.colors["bg_secondary"],
                                activebackground=self.colors["bg_primary"],
                                font=('Arial', 10))
        udp_btn.pack(side=tk.LEFT)
        
        # Request Type
        tk.Label(input_frame, text="Request Type:", 
                bg=self.colors["bg_primary"],
                fg=self.colors["text_primary"],
                font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=10)
        
        self.request_type = ttk.Combobox(input_frame, width=20, font=('Arial', 10),
                                        values=["SYN Request", "ACK Request", "FIN Request", 
                                                "Data Packet", "Broadcast", "Multicast"],
                                        state="readonly")
        self.request_type.set("SYN Request")
        self.request_type.grid(row=2, column=1, padx=10, pady=10)
        
        # Packet Count
        tk.Label(input_frame, text="Packets:", 
                bg=self.colors["bg_primary"],
                fg=self.colors["text_primary"],
                font=('Arial', 11, 'bold')).grid(row=2, column=2, sticky='w', pady=10, padx=(20,0))
        
        self.packet_count_spin = tk.Spinbox(input_frame, from_=1, to=100, width=10,
                                           font=('Arial', 10),
                                           bg=self.colors["bg_secondary"],
                                           fg=self.colors["text_primary"])
        self.packet_count_spin.grid(row=2, column=3, padx=10, pady=10)
        self.packet_count_spin.delete(0, tk.END)
        self.packet_count_spin.insert(0, "5")
        
        # Button Frame
        button_frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Control Buttons
        self.start_btn = tk.Button(button_frame, text="▶ Start Simulation",
                                  command=self.start_simulation,
                                  bg=self.colors["accent_purple"],
                                  fg="white",
                                  font=('Arial', 12, 'bold'),
                                  padx=20,
                                  pady=10,
                                  cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(button_frame, text="⏹ Stop Simulation",
                                 command=self.stop_simulation,
                                 bg=self.colors["error"],
                                 fg="white",
                                 font=('Arial', 12, 'bold'),
                                 padx=20,
                                 pady=10,
                                 cursor="hand2",
                                 state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(button_frame, text="🗑 Clear Log",
                             command=self.clear_log,
                             bg=self.colors["warning"],
                             fg="white",
                             font=('Arial', 12, 'bold'),
                             padx=20,
                             pady=10,
                             cursor="hand2")
        clear_btn.pack(side=tk.LEFT, padx=10)
        
        # Log Output
        log_frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))
        
        tk.Label(log_frame, text="Simulation Log:",
                bg=self.colors["bg_primary"],
                fg=self.colors["accent_lavender"],
                font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0,10))
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 height=15,
                                                 bg=self.colors["bg_secondary"],
                                                 fg=self.colors["text_primary"],
                                                 font=('Consolas', 10),
                                                 insertbackground=self.colors["text_primary"])
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial log message
        self.log("🟢 Network Learning Tool initialized")
        self.log("🔧 Ready to simulate network requests")
        self.log("⚠️  WARNING: Only use on your own systems!")
    
    def create_history_tab(self, parent):
        """Create the history tab"""
        # History frame
        history_frame = tk.Frame(parent, bg=self.colors["bg_primary"])
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create treeview for history
        columns = ('Time', 'Protocol', 'IP', 'Port', 'Type', 'Packets', 'Status')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        # Style treeview
        style = ttk.Style()
        style.configure("Treeview",
                       background=self.colors["bg_secondary"],
                       foreground=self.colors["text_primary"],
                       fieldbackground=self.colors["bg_secondary"])
        style.configure("Treeview.Heading",
                       background=self.colors["bg_tertiary"],
                       foreground=self.colors["text_primary"],
                       font=('Arial', 10, 'bold'))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear history button
        clear_history_btn = tk.Button(parent, text="Clear History",
                                     command=self.clear_history,
                                     bg=self.colors["warning"],
                                     fg="white",
                                     font=('Arial', 10, 'bold'),
                                     padx=15,
                                     pady=5,
                                     cursor="hand2")
        clear_history_btn.pack(pady=(0, 20))
    
    def create_learning_tab(self, parent):
        """Create the learning/guide tab"""
        # Create scrollable frame
        canvas = tk.Canvas(parent, bg=self.colors["bg_primary"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["bg_primary"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Protocol information
        info_text = """
🌐 Network Protocol Learning Guide

📌 TCP (Transmission Control Protocol):
• Connection-oriented protocol
• Reliable data transfer
• Error checking and recovery
• Ordered data delivery
• Flow control
• Used by: HTTP, HTTPS, FTP, SSH

📌 UDP (User Datagram Protocol):
• Connectionless protocol
• Faster but less reliable
• No error recovery
• No ordered delivery
• Used by: DNS, VoIP, Streaming, Games

🔒 Safety Guidelines:
1. Only test on your own systems
2. Never scan networks without permission
3. Use for educational purposes only
4. Understand local laws and regulations
5. Respect others' privacy and security

🎯 This tool simulates:
• SYN packets (TCP connection initiation)
• ACK packets (Acknowledgement)
• Data transmission simulation
• Network protocol behavior

📚 Learning Resources:
• Wireshark for packet analysis
• RFC documents for protocol specs
• Network programming tutorials
• Cybersecurity courses
        """
        
        # Display info
        info_label = tk.Label(scrollable_frame,
                             text=info_text,
                             bg=self.colors["bg_primary"],
                             fg=self.colors["text_primary"],
                             font=('Arial', 11),
                             justify=tk.LEFT,
                             padx=20,
                             pady=20)
        info_label.pack(fill=tk.BOTH, expand=True)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, bg=self.colors["bg_tertiary"], height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame,
                                    text="🟢 Ready | Packets Sent: 0",
                                    bg=self.colors["bg_tertiary"],
                                    fg=self.colors["text_primary"],
                                    font=('Arial', 10))
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # Time label
        self.time_label = tk.Label(status_frame,
                                  text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  bg=self.colors["bg_tertiary"],
                                  fg=self.colors["text_secondary"],
                                  font=('Arial', 9))
        self.time_label.pack(side=tk.RIGHT, padx=20)
        
        # Update time every second
        self.update_time()
    
    def update_time(self):
        """Update time in status bar"""
        self.time_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def log(self, message):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def simulate_tcp_request(self, ip, port, request_type, packet_count):
        """Simulate TCP request (educational simulation)"""
        try:
            for i in range(packet_count):
                if not self.is_running:
                    break
                
                # Simulate different TCP packet types
                if request_type == "SYN Request":
                    status = f"TCP SYN packet {i+1} simulated to {ip}:{port}"
                    color = "🟡"
                elif request_type == "ACK Request":
                    status = f"TCP ACK packet {i+1} simulated to {ip}:{port}"
                    color = "🟢"
                elif request_type == "FIN Request":
                    status = f"TCP FIN packet {i+1} simulated to {ip}:{port}"
                    color = "🔵"
                else:
                    status = f"TCP Data packet {i+1} simulated to {ip}:{port}"
                    color = "🟣"
                
                self.log(f"{color} {status}")
                self.packet_count += 1
                self.update_status()
                
                # Add to history
                self.add_to_history(ip, port, "TCP", request_type, packet_count, "Simulated")
                
                time.sleep(0.5)  # Simulate network delay
                
            if self.is_running:
                self.log("✅ TCP simulation completed successfully")
        except Exception as e:
            self.log(f"❌ TCP simulation error: {str(e)}")
    
    def simulate_udp_request(self, ip, port, request_type, packet_count):
        """Simulate UDP request (educational simulation)"""
        try:
            for i in range(packet_count):
                if not self.is_running:
                    break
                
                # Simulate UDP packets
                if request_type == "Broadcast":
                    status = f"UDP Broadcast packet {i+1} simulated"
                    color = "🎯"
                elif request_type == "Multicast":
                    status = f"UDP Multicast packet {i+1} simulated"
                    color = "📡"
                else:
                    status = f"UDP packet {i+1} simulated to {ip}:{port}"
                    color = "🔷"
                
                self.log(f"{color} {status}")
                self.packet_count += 1
                self.update_status()
                
                # Add to history
                self.add_to_history(ip, port, "UDP", request_type, packet_count, "Simulated")
                
                time.sleep(0.3)  # UDP is faster
                
            if self.is_running:
                self.log("✅ UDP simulation completed successfully")
        except Exception as e:
            self.log(f"❌ UDP simulation error: {str(e)}")
    
    def start_simulation(self):
        """Start the network simulation"""
        if self.is_running:
            return
        
        # Get input values
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        protocol = self.protocol_var.get()
        request_type = self.request_type.get()
        
        try:
            packet_count = int(self.packet_count_spin.get())
            if packet_count <= 0 or packet_count > 1000:
                messagebox.showwarning("Warning", "Packet count must be between 1 and 1000")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid packet count")
            return
        
        # Validate IP address (basic validation)
        if not ip.replace('.', '').isdigit() or len(ip.split('.')) != 4:
            messagebox.showwarning("Warning", "Please enter a valid IP address")
            return
        
        # Validate port
        try:
            port_int = int(port)
            if port_int < 1 or port_int > 65535:
                messagebox.showwarning("Warning", "Port must be between 1 and 65535")
                return
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid port number")
            return
        
        # Start simulation
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.log(f"🚀 Starting {protocol} simulation to {ip}:{port}")
        self.log(f"📦 Packets to send: {packet_count}")
        self.log(f"🎯 Request type: {request_type}")
        
        # Start simulation in separate thread
        if protocol == "TCP":
            thread = threading.Thread(target=self.simulate_tcp_request,
                                     args=(ip, port, request_type, packet_count))
        else:
            thread = threading.Thread(target=self.simulate_udp_request,
                                     args=(ip, port, request_type, packet_count))
        thread.daemon = True
        thread.start()
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("🛑 Simulation stopped by user")
    
    def add_to_history(self, ip, port, protocol, req_type, packets, status):
        """Add request to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_tree.insert('', 'end', values=(
            timestamp, protocol, ip, port, req_type, packets, status
        ))
    
    def clear_history(self):
        """Clear request history"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
        self.log("🗑 Log cleared")
    
    def update_status(self):
        """Update status bar"""
        self.status_label.config(text=f"🟢 Running | Packets Sent: {self.packet_count}")

def main():
    root = tk.Tk()
    app = NetworkLearningTool(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()
