import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
import math
from task6_files.CompareSignal import Compare_Signals
#np.set_printoptions(precision=10)  # Adjust the precision as needed



class Task6:
    def __init__(self, parent):

        self.parent = parent
        self.large_font = ('Helvetica', 14)
        
        # Create main frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)

        # Radio buttons for function type
        self.radios_frame = tk.Frame(self.frame)

        self.radio = tk.StringVar(value="Point1")
        tk.Radiobutton(self.radios_frame, text="Point 1",       variable=self.radio, value="Point1",   font=self.large_font).grid(row=1, column=0, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="Point 2",      variable=self.radio, value="Point2", font=self.large_font).grid(row=1, column=1, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="Point 3",      variable=self.radio, value="Point3", font=self.large_font).grid(row=1, column=2, padx = 1, pady=3, sticky='ew')
        self.radios_frame.grid(row=1, pady=4, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="Sampling Frequency:", font=self.large_font)
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
       
        point = self.radio.get()
        if(point == 'Point1'):
            signal1 = ReadSignalFile(r'task6_files\Point1 Correlation\Corr_input signal1.txt')
            signal2 = ReadSignalFile(r'task6_files\Point1 Correlation\Corr_input signal2.txt')
            output_file = r'task6_files\Point1 Correlation\CorrOutput.txt'
            indices, values = self.correlation(signal1, signal2)
            Compare_Signals(output_file, indices, values)  


        if(point == 'Point2'):
            signal1 = ReadSignalFile(r'task6_files\Point2 Time analysis\TD_input signal1.txt')
            signal2 = ReadSignalFile(r'task6_files\Point2 Time analysis\TD_input signal2.txt')
            sampling_frequency = float(self.ConstantInput.get())
            self.calculate_time_delay(signal1, signal2, sampling_frequency)
            

        if(point == 'Point3'):
            pass
        return


    def correlation(self, signal1, signal2):

        _, values1 = signal1
        _, values2 = signal2
        N = len(values1)

        samples = {}
        for n in range(N):
            counter = 0
            for k in range(N):
                counter += values1[k]* values2[k]
            values2 = self.shift_left(values2)
            samples[n] = counter / N

        samples = self.calculate_normalization(values1, values2, samples)
        indices = list(samples.keys())
        values = list(samples.values())
        self.plot_signals(indices, values)
        return indices, values




    def mulitply_signals(self, a, b):
        c = []
        for n in range(len(a)):
            c.append(np.real(a[n] * b[n]))
        return c

    

    def shift_left(self, list):
        return np.roll(list, -1)



    def calculate_normalization(self, a, b, rj):
        N = len(rj)
        p = {}
        
        squares1 = sum([x**2 for x in a])
        squares2 = sum([x**2 for x in b])
        normalization_factor = (1/N)*(math.sqrt( squares1 * squares2))

        for k in range(N):
            p[k] = rj[k]/ normalization_factor
        return p


    def calculate_time_delay(self, signal1, signal2, sampling_frequency, expected_lag=None):
        print("Starting correlation calculation...")

        # Calculate the periodic cross-correlation
        _, correlation_values = self.correlation(signal1, signal2)
        print(f"Correlation calculated: {correlation_values}")


        if expected_lag is not None:
            # Use the expected lag to calculate the time delay
            lag = expected_lag
            print(f"Using expected lag (j): {lag}")
        else:
            # Find the lag corresponding to the maximum absolute value of the correlation
            max_corr_index = np.argmax(np.abs(correlation_values))
            print(f"Index of maximum correlation: {max_corr_index}")
            lag = max_corr_index 
            print(f"Calculated lag (j): {lag}")

        # Calculate time delay
        time_delay = abs(lag) / sampling_frequency
        print(f"Calculated time delay: {time_delay}")

        return time_delay

    def plot_signals(self, indices, values):
        self.ax.clear()

        
        self.ax.stem(indices, values)
        self.ax.set_title(f"Correlation Result")

        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")

        self.ax.grid(True)

        self.canvas.draw()
 
        return
    
#######################################################################


    def dft(self, values):

        N = len(values)
        samples = np.zeros(N, dtype=complex)

        for n in range(N):
            counter = 0
            for k in range(N):
                xk = values[k]
                counter += xk * np.exp(-2j * np.pi * k * n / N) 

            samples[n] = counter
        return samples
    
    def correlation_fast(self, signal1, signal2, output_file):

        _, values1 = signal1
        _, values2 = signal2
        N = len(values1)

        signal1 = self.dft(values1)
        signal2 = self.dft(values2)
        FD = self.mulitply_signals(signal1, np.conj(signal2))

        
        samples = {}
        for n in range(N):
            counter = 0
            for k in range(N):
                xk = FD[k]
                counter += (xk * np.exp(1j* 2 * np.pi * k * n/N))
            samples[n] = np.real(counter)/N/N
        

        samples = self.calculate_normalization(values1, values2, samples)
        indices = list(samples.keys())
        values = list(samples.values())
        Compare_Signals(output_file,indices, values)   
        self.plot_signals(indices, values)
        return
