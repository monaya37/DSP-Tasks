import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *

class Task3:
    def __init__(self, parent):
        self.parent = parent

        # Create GUI Components
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)  

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        # Input fields for amplitude, frequency, phase, sampling
        self.num_of_bits = tk.DoubleVar(value=1.0)
        self.num_of_levels = tk.DoubleVar(value=0.0)

        ttk.Label(self.frame, text="Number of bits:").grid(row=2, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.num_of_bits).grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Number of levels:").grid(row=3, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.num_of_levels).grid(row=3, column=1, pady=5)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command= self.quantize_and_encode)
        generate_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.ranges = list()


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def quantize_and_encode(self):
        signal = functions.read_signals("task3_files\Quan1_input.txt")
        delta = max(signal[1]) - min(signal[1])        
        delta = delta / self.num_of_levels

        for i in range(1, self.num_of_levels+1):
            #TO DO:
            # self.ranges.append(min((signal[1] + (delta * i))/2 ))