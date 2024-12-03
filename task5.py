import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
import math
from task5_files import signalcompare


class Task5:
    def __init__(self, parent):

        self.parent = parent
        self.large_font = ('Helvetica', 14)
        
        # Create main frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)

        # Radio buttons for function type
        self.radios_frame = tk.Frame(self.frame)

        self.radio = tk.StringVar(value="DFT")
        tk.Radiobutton(self.radios_frame, text="DFT",  variable=self.radio, value="DFT", font=self.large_font).grid(row=1, column=0, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="IDFT",      variable=self.radio, value="IDFT", font=self.large_font).grid(row=1, column=1, padx = 1, pady=3, sticky='ew')
        self.radios_frame.grid(row=1, pady=4, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="will see:", font=self.large_font)
        self.label.pack(side='left', padx=5)
        self.ConstantInput = tk.Entry(self.label_entry_frame, width=10, font=self.large_font)
        self.ConstantInput.pack(side='left', padx=2)
        self.label_entry_frame.grid(row=2, column=0, pady=4, sticky='ew')

        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=self.large_font)

        # Start button with large font
        generate_button = ttk.Button(self.frame, text="Start", command=self.run_algorithm, style='Large.TButton')
        generate_button.grid(row=3, column=0, columnspan=3, pady=10)


        # Plotting area (centered)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=4, column=0, columnspan=3, pady=10, sticky='nsew')

        self.signal = None
        self.signal2 = None
        self.title = None #for visualization


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def run_algorithm(self):
        if(self.radio == "DFT"):
            pass
        else:
            input_signal = self.read_signals('task5_files\IDFT\input_IDFT.txt')
            output_signal = ReadSignalFile('task5_files\IDFT\Output_Signal_IDFT.txt')
            self.idft(input_signal, output_signal)

    def read_signals(self,file_path):
        amplitudes = []
        phases = []
        with open(file_path, "r") as file:
            for line in file:
                number_of_samples = int(line.strip())
                if number_of_samples == 0:
                    continue

                for _ in range(number_of_samples):
                    line = file.readline()
                    # read every single line, converts the values from string to float
                    amplitude, phase = line.strip().split()
                    amplitude = float(amplitude.replace('f', ''))
                    phase = float(phase.replace('f', ''))
                    amplitudes.append(amplitude)
                    phases.append(phase)
            #amplitudes = np.array([float(a.replace('f', '')) for a in amplitudes])
            #phases = np.array([float(p.replace('f', '')) for p in phases])
        return amplitudes, phases

    def idft(self, input_signal, output_signal):
        amplitudes = input_signal[0]
        print(amplitudes)

        shifts = input_signal[1]
        print(shifts)

        N = (len(shifts))

        samples = {}
        counter = 0
        amplitudes = np.array(amplitudes)
        shifts = np.array(shifts)
        #X = amplitudes * np.exp(1j * shifts)
        for n in range(N):
            counter = 0
            for k in range(N):
                xk = amplitudes[k] * np.exp(1j * shifts[k])
                counter = counter + (xk * np.exp(1j* 2 * np.pi * k * n/N))

            samples[n] = round(np.real((counter)/N))

        
        values = list(samples.values())
        print(signalcompare.SignalComapreAmplitude(values, output_signal[1]))
        print("done")
        return

            
 

    def plot_signals(self, samples):
        self.ax.clear()

        indices = list(samples.keys())
        values = list(samples.values())
        
        self.ax.stem(indices, values)
        self.ax.set_title(f"{self.title} Visualization")

        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.grid()
        self.canvas.draw()
 
        return
    


