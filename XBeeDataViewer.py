import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import os
from RealXBeeData import RealXBeeData

class XBeeDataViewer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("XBee Data Viewer")
        self.geometry("900x700")

        # Utilizar RealXBeeData para comunicação real
        self.real_xbee = RealXBeeData(self, port="COM4", baudrate=9600)

        # Configurar a chamada de download_data ao fechar a aplicação
        self.protocol("WM_DELETE_WINDOW", self.exit_application)

        # Criar e configurar widgets
        self.create_widgets()

    def create_widgets(self):
        self.paned_window = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.paned_window.pack(expand=True, fill='both')

        self.serial_monitor_label = tk.Label(self.paned_window, text="Monitor Serial:")
        self.serial_monitor_label.pack()

        self.serial_monitor = tk.Text(self.paned_window, height=10, width=70)
        self.serial_monitor.pack(expand=True, fill='both')

        self.paned_window.add(self.serial_monitor_label)
        self.paned_window.add(self.serial_monitor)

        self.data_analysis_label = tk.Label(self, text="Análise de Dados:")
        self.data_analysis_label.pack()

        self.data_tree = ttk.Treeview(self, columns=('Source', 'Data', 'Timestamp'), show='headings', height=10)
        self.data_tree.heading('Source', text='Source')
        self.data_tree.heading('Data', text='Data')
        self.data_tree.heading('Timestamp', text='Timestamp')
        self.data_tree.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        self.start_button = tk.Button(self.button_frame, text="Iniciar Leitura", command=self.start_real_communication)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(self.button_frame, text="Parar Leitura", command=self.stop_real_communication)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.download_button = tk.Button(self.button_frame, text="Baixar Dados", command=self.download_data)
        self.download_button.grid(row=0, column=2, padx=10, pady=10)

        self.clear_monitor_button = tk.Button(self.button_frame, text="Limpar Monitor", command=self.clear_monitor)
        self.clear_monitor_button.grid(row=0, column=3, padx=10, pady=10)

        self.clear_data_button = tk.Button(self.button_frame, text="Limpar Dados", command=self.clear_data)
        self.clear_data_button.grid(row=0, column=4, padx=10, pady=10)

        self.exit_button = tk.Button(self.button_frame, text="Sair", command=self.exit_application)
        self.exit_button.grid(row=0, column=5, padx=10, pady=10)

    def start_real_communication(self):
        self.real_xbee.start_real_communication()

    def stop_real_communication(self):
        self.real_xbee.stop_real_communication()

    def download_data(self):
        self.real_xbee.download_data()

    def update_serial_monitor(self, text):
        self.serial_monitor.insert(tk.END, text)
        self.serial_monitor.see(tk.END)

    def update_data_tree(self, data):
        values = (data['source'], data['data'], data['timestamp'])
        self.data_tree.insert('', 0, values=values)

    def clear_monitor(self):
        self.serial_monitor.delete(1.0, tk.END)

    def clear_data(self):
        self.data_tree.delete(*self.data_tree.get_children())

    def exit_application(self):
        self.real_xbee.download_data()  # Chama a função download_data ao fechar a aplicação
        self.stop_real_communication()
        self.destroy()