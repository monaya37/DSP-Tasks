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
        self.num_of_levels = tk.DoubleVar(value=4.0)

        ttk.Label(self.frame, text="Number of bits:").grid(row=2, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.num_of_bits).grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Number of levels:").grid(row=3, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.num_of_levels).grid(row=3, column=1, pady=5)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command= self.quantize_and_encode)
        generate_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.intervals = dict()
        self.signal = None



    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def quantize_and_encode(self):
        self.signal = functions.read_signals("task3_files\\Quan1_input.txt")
        self.claculate_intervals()
        self.update_values()
        self.plot_signal()

    def claculate_intervals(self):
        self.intervals.clear()
        num_of_levels = self.num_of_levels.get()
        num_of_bits = self.num_of_bits.get()
        
        start = min(self.signal[1])
        end = max(self.signal[1])
        delta = end - start     
        delta = round(delta / float(num_of_levels), 2)


        end = round(start + delta, 2)
        for i in range(int(num_of_levels)):
            x = (start + (end)) / 2
            self.intervals[(start,end)] =  round(x, 2)
            start = end
            end = round(start + delta,2)
        print('intervals: ', self.intervals.keys())

    def update_values(self):
        values = list()
        found = False
        for element in self.signal[1]:
            for start, end in self.intervals.keys():
                if start <= element <= end:
                    values.append(self.intervals[(start, end)])
                    found = True
                    break
            if(found == False):
                print('element: ', element)
            found = False

        print('values: ', self.signal[1])
        self.signal[1].clear()
        self.signal[1].extend(values)
        print('updated values: ', self.signal[1])
        

    def plot_signal(self):
        self.ax.clear()
        self.ax.plot(self.signal[0], self.signal[1])
        self.canvas.draw()

           

                    

