import os
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
        
        # Configure the root window to center
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        # Create GUI Components
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=1, column=0, sticky="nsew")

        # Center all rows and columns in the frame
        for i in range(8):  # Adjust number of rows based on content
            self.frame.grid_rowconfigure(i, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.large_font = ('Helvetica', 14)

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


        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        self.signal = None
        self.signal2 = None
        self.title = None #for visualization




    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def run_algorithm(self):
        self.set_paths()
        point = self.radio.get()
        if(point == 'Point1'):
            signal1 = ReadSignalFile(self.corr1_path)
            signal2 = ReadSignalFile(self.corr2_path)
            samples, indices, values = correlation(signal1, signal2)
            Compare_Signals(self.output1_path, indices, values) 
            PlotSignal(samples, self.ax, self.canvas) 


        if(point == 'Point2'):
            signal1 = ReadSignalFile(self.path3)
            signal2 = ReadSignalFile(self.path4)
            sampling_frequency = float(self.ConstantInput.get())
            calculate_time_delay(signal1, signal2, sampling_frequency)
            

        if(point == 'Point3'):
            class1_signals = ReadSignalsFromDir(self.class1_dir)
            class2_signals = ReadSignalsFromDir(self.class2_dir)
            test_signal1 = ReadSignalValues(self.test1_path)
            test_signal2 = ReadSignalValues(self.test2_path)
            result = classify_signal(class1_signals, class2_signals, test_signal1)
            print("Signal 1 belongs to: ", result)
            result = classify_signal(class1_signals, class2_signals, test_signal2)
            print("Signal 2 belongs to: ", result)



        return

    def set_paths(self):
        self.corr1_path = r'task6_files\Point1 Correlation\Corr_input signal1.txt'
        self.corr2_path = r'task6_files\Point1 Correlation\Corr_input signal2.txt'
        self.output1_path = r'task6_files\Point1 Correlation\CorrOutput.txt'

        self.path3 = r'task6_files\Point2 Time analysis\TD_input signal1.txt'
        self.path4 = r'task6_files\Point2 Time analysis\TD_input signal2.txt'

        self.class1_dir = r'task6_files\point3 Files\Class 1'
        self.class2_dir = r'task6_files\point3 Files\Class 2'

        self.test1_path = r'task6_files\point3 Files\Test Signals\Test1.txt'
        self.test2_path = r'task6_files\point3 Files\Test Signals\Test2.txt'
        
        


    
        




    
#######################################################################
def correlation(signal1, signal2):

    _, values1 = signal1
    _, values2 = signal2
    N = len(values1)

    samples = {}
    for n in range(N):
        counter = 0
        for k in range(N):
            counter += values1[k]* values2[k]
        values2 = shift_left(values2)
        samples[n] = counter / N

    samples = calculate_normalization(values1, values2, samples)
    indices = list(samples.keys())
    values = list(samples.values())
    
    return samples, indices, values



def shift_left(list):
    return np.roll(list, -1)

def get_max(values):
    return np.argmax(np.abs(values))
    
def calculate_normalization(a, b, rj):
        N = len(rj)
        p = {}
        
        squares1 = sum([x**2 for x in a])
        squares2 = sum([x**2 for x in b])
        normalization_factor = (1/N) * (math.sqrt(abs(squares1 * squares2)))

        for k in range(N):
            p[k] = rj[k]/ normalization_factor
        return p

def calculate_time_delay(signal1, signal2, sampling_frequency, expected_lag=None):
    print("Starting correlation calculation...")

    # Calculate the periodic cross-correlation
    _, _, correlation_values = correlation(signal1, signal2)
    print(f"Correlation calculated: {correlation_values}")


    if expected_lag is not None:
        # Use the expected lag to calculate the time delay
        lag = expected_lag
        print(f"Using expected lag (j): {lag}")
    else:
        # Find the lag corresponding to the maximum absolute value of the correlation
        max_corr_index = get_max(correlation_values)
        print(f"Index of maximum correlation: {max_corr_index}")
        lag = max_corr_index 
        print(f"Calculated lag (j): {lag}")

    # Calculate time delay
    time_delay = abs(lag) / sampling_frequency
    print(f"Calculated time delay: {time_delay}")

    return time_delay


def classify_signal(class1_signals,  class2_signals, test_signal):
         
    up_correlations = []
    for signal in class1_signals:
        _, _, corr_values = correlation(signal, test_signal)
        max = get_max(corr_values)
        up_correlations.append(max)

    down_correlations = []
    for signal in class2_signals:
        _, _, corr_values = correlation(signal, test_signal)
        max = get_max(corr_values)
        down_correlations.append(max)
    
    up_avg = sum(up_correlations) / len(up_correlations)
    down_avg = sum(down_correlations) / len(down_correlations)

    if down_avg > up_avg:
        return "Class 1 (Down movement)"
    else:
        return "Class 2 (Up movement)"