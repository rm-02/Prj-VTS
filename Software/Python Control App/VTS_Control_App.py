import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading

class ESBSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vibration Control")
        self.root.geometry("550x500")
        self.root.resizable(True, True)


        self.sleep_status_var = tk.IntVar()
        self.serial_connection = None
        self.is_listening = False
        self.listener_thread = None
        
        self.create_widgets()
        
        self.update_ports()
    
    def create_widgets(self):
        # Serial port selection
        port_frame = ttk.LabelFrame(self.root, text="Serial Connection")
        port_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(port_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.port_combobox = ttk.Combobox(port_frame, width=25)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(port_frame, text="Baud Rate:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.baud_combobox = ttk.Combobox(port_frame, width=25, values=["9600", "19200", "38400", "57600", "115200"])
        self.baud_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.baud_combobox.current(4) 
        
        refresh_button = ttk.Button(port_frame, text="Refresh", command=self.update_ports)
        refresh_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.connect_button = ttk.Button(port_frame, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=1, column=2, padx=5, pady=5)
        
        # Waveform characteristics input frame
        input_frame = ttk.LabelFrame(self.root, text="Input Values")
        input_frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(input_frame, text="Voltage (10 - 95 AC) [V]:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.Voltage_entry = ttk.Entry(input_frame, width=30)
        self.Voltage_entry.grid(row=0, column=1, padx=5, pady=5)
        self.Voltage_entry.insert(0, "95")  # Default value 95V
        
        ttk.Label(input_frame, text="Frequency [Hz]:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.Frequency_entry = ttk.Entry(input_frame, width=30)
        self.Frequency_entry.grid(row=1, column=1, padx=5, pady=5)
        self.Frequency_entry.insert(0, "100")  # Default value 100Hz
        
        ttk.Label(input_frame, text="No. Cycles:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.Cycles_entry = ttk.Entry(input_frame, width=30)
        self.Cycles_entry.grid(row=2, column=1, padx=5, pady=5)
        self.Cycles_entry.insert(0, "4")  # Default value 4 (= 40ms at 100Hz)
        
        # Send button - tells connected NRF52 to send changes over ESB
        send_button = ttk.Button(input_frame, text="Send Values", command=self.send_wave_values)
        send_button.grid(row=3, column=2, padx=5, pady=5) 
        

        # Sleep options
        sleep_frame = ttk.LabelFrame(self.root, text="Sleep Options")
        sleep_frame.pack(padx=10, pady=10, fill="x")

        self.sleep_status = tk.Checkbutton(sleep_frame, text="Sleep Enable?", variable = self.sleep_status_var, 
                             onvalue=1, offvalue=0)
        self.sleep_status.grid(row=0, column=0, padx=5, pady=5)


        ttk.Label(sleep_frame, text="On-Time (Multiples of 5 Minutes):").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.sleep_on_time = ttk.Entry(sleep_frame, width=30)
        self.sleep_on_time.grid(row=1, column=2, padx=5, pady=5)
        self.sleep_on_time.insert(0, "5")  # Default value 5 minutes
        
        ttk.Label(sleep_frame, text="Off-Time (Multiples of 5 Minutes):").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.sleep_off_time = ttk.Entry(sleep_frame, width=30)
        self.sleep_off_time.grid(row=2, column=2, padx=5, pady=5)
        self.sleep_off_time.insert(0, "5")  # Default value 5 minutes

        # Send button - tells connected NRF52 to send changes over ESB
        send_sleep_button = ttk.Button(sleep_frame, text="Send Values", command=self.send_sleep_values)
        send_sleep_button.grid(row=3, column=2, padx=5, pady=5)

        # Status display
        status_frame = ttk.LabelFrame(self.root, text="Status")
        status_frame.pack(padx=10, pady=10, fill="x")
        
        self.status_label = ttk.Label(status_frame, text="Not connected")
        self.status_label.pack(padx=5, pady=5)
        
        # Communication log
        log_frame = ttk.LabelFrame(self.root, text="Communication Log")
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=10, width=50, yscrollcommand=scrollbar.set)
        self.log_text.pack(padx=5, pady=5, fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)
        

    
    def update_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox['values'] = ports
        if ports:
            self.port_combobox.current(0)
    
    def connect_serial(self):
        if self.serial_connection and self.serial_connection.is_open:
            # Disconnect
            self.is_listening = False
            if self.listener_thread:
                self.listener_thread.join(timeout=1.0)
            self.serial_connection.close()
            self.status_label.config(text="Disconnected")
            self.connect_button.config(text="Connect")
            self.add_to_log("Disconnected from device")
            return
        
        port = self.port_combobox.get()
        baud = int(self.baud_combobox.get())
        
        try:
            self.serial_connection = serial.Serial(port, baud, timeout=0.1)
            self.status_label.config(text=f"Connected to {port} at {baud} baud")
            self.connect_button.config(text="Disconnect")
            self.add_to_log(f"Connected to {port} at {baud} baud")
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.status_label.config(text="Connection failed")
            self.add_to_log(f"Connection error: {str(e)}")
    
    def send_wave_values(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            messagebox.showerror("Error", "Not connected to device")
            return

        try:
            # Get values from input fields
            Voltage = self.Voltage_entry.get().strip()
            Frequency = self.Frequency_entry.get().strip()
            Cycles = self.Cycles_entry.get().strip()

            # Convert values to numbers and validate range
            try:
                Voltage = int(Voltage)
                Frequency = int(Frequency)  
                Cycles = int(Cycles)    

                # Assert that the values are within acceptable ranges
                if not (10 <= Voltage <= 95):
                    raise ValueError("Voltage must be between 10 and 95")
                if not (10 <= Frequency <= 300):
                    raise ValueError("Frequency must be between 10 and 300")
                period = 1/Frequency
                if not ((0 < period*Cycles <= 0.09) and (Cycles > 0)):
                    raise ValueError("\n\nYou Must Have More Than 0 Cycles & Cycles/Frequency Cannot Exceed 90ms.\n\nIt is expected that "
                    "VTS may be applied every 90ms. Setting a wave longer than this means the VTS will never turn off.\n\nIf this is "
                    "incorrect, this rule is at line 167 to be edited")

            except ValueError as ve:
                messagebox.showerror("Input Error", f"Invalid input: {ve}")
                return
            
            # Convert values into the BOS1921 Expected format

            Voltage *= 2 # Multiply voltage by 2, it'll be halved again on the BOS1921 as it's played unipolar
            Voltage = "{:#05X}".format(round((Voltage*4095)/190)) 
            Frequency = "{:#03X}".format(round(Frequency/3.9))
            Cycles = "{:#03X}".format(Cycles)

            # Create a packet with the validated values, set mode to 0x01 (wave change request)
            packet = f"0x01,{Voltage},{Frequency},{Cycles}\n"

            # Send packet
            self.serial_connection.write(packet.encode('utf-8'))
            self.add_to_log(f"SENT: {packet.strip()}")

        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send data: {str(e)}")
            self.add_to_log(f"Send error: {str(e)}")

    def send_sleep_values(self):
        if not self.serial_connection or not self.serial_connection.is_open:
            messagebox.showerror("Error", "Not connected to device")
            return

        try:
            # Get values from input fields
            sleep_status = int(self.sleep_status_var.get())
            sleep_on_time = self.sleep_on_time.get().strip()
            sleep_off_time = self.sleep_off_time.get().strip()

            try:

                # Assert that the values are within acceptable ranges
                sleep_on_time = int(sleep_on_time)
                sleep_off_time = int(sleep_off_time)

                if not (5 <= sleep_on_time <= 1275):
                    raise ValueError("On-Time Must be Between 5 and 1275")
                
                if (sleep_on_time % 5 != 0):
                    raise ValueError("On-Time Must be A Multiple of 5 Minutes")

                if not (5 <= sleep_off_time <= 1275):
                    raise ValueError("Off-Time Must be Between 5 and 1275")
                
                if (sleep_off_time % 5 != 0):
                    raise ValueError("Off-Time Must be A Multiple of 5 Minutes")
                

            except ValueError as ve:
                messagebox.showerror("Input Error", f"Invalid input: {ve}")
                return
            
            # Convert to hex to send 
            sleep_status = "{:#03X}".format(sleep_status)
            
            # Times are in multiples of 5 so that they can be /5, this allows 0xFF to represent 1275 minutes
            sleep_on_time /= 5
            sleep_on_time = "{:#03X}".format(int(sleep_on_time))

            sleep_off_time /= 5
            sleep_off_time = "{:#03X}".format(int(sleep_off_time))
            
            # Create a packet with the validated values, set mode to 0x02 (sleep change request)
            packet = f"0x02,{sleep_status},{sleep_on_time},{sleep_off_time}\n"

            # Send packet
            self.serial_connection.write(packet.encode('utf-8'))
            self.add_to_log(f"SENT: {packet.strip()}")

        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send data: {str(e)}")
            self.add_to_log(f"Send error: {str(e)}")
    
    def add_to_log(self, message):
        """Add a message to the log display with timestamp"""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)  # Auto-scroll to the end
    
    def clear_log(self):
        """Clear the communication log"""
        self.log_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ESBSenderApp(root)
    root.mainloop()
