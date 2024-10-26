import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
from task3_files import QuanTest1
import math


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
        self.num_of_bits = tk.IntVar(value=0)  # Initialize to 0 instead of None
        self.num_of_levels = tk.IntVar(value=0)  # Initialize to 0

        ttk.Label(self.frame, text="Number of bits:").grid(row=2, column=0, pady=5)
        self.bits_entry = ttk.Entry(self.frame, textvariable=self.num_of_bits)
        self.bits_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Number of levels:").grid(row=3, column=0, pady=5)
        self.levels_entry = ttk.Entry(self.frame, textvariable=self.num_of_levels)
        self.levels_entry.grid(row=3, column=1, pady=5)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command=self.quantize_and_encode)
        generate_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.intervals = dict()
        self.signal = None
        self.binary_numbers = None

    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()


    def quantize_and_encode(self):
        self.signal = functions.read_signals("task3_files\\Quan1_input.txt")

        self.claculate_intervals()
        quantized_values = self.quantize_values()
        self.get_binary_numbers(self.num_of_bits.get())
        encoded_values = self.encode_values()
        self.plot_signal()
        self.print_resutls(encoded_values, quantized_values)

        QuanTest1.QuantizationTest1('task3_files\\Quan1_Out.txt', encoded_values, quantized_values)


    def claculate_intervals(self):
        self.intervals.clear()
        
        if self.num_of_levels.get() == 0:  
            self.num_of_levels.set(math.pow(2, int(self.num_of_bits.get())))

        if self.num_of_bits.get() == 0:  
            self.num_of_bits.set(math.log2(int(self.num_of_levels.get())))

        start = min(self.signal[1])  
        end = max(self.signal[1])
        delta = end - start
        delta = round(delta / float(self.num_of_levels.get()), 2) 

        end = round(start + delta, 2)
        for i in range(int(self.num_of_levels.get())):  
            x = (start + end) / 2
            self.intervals[(start, end)] = round(x, 2)
            start = end
            end = round(start + delta, 2)


    def quantize_values(self):
        values = []
        for element in self.signal[1]:
            for start, end in self.intervals.keys():
                if start <= element <= end:
                    values.append(self.intervals[(start, end)])
                    break

        self.signal[1].clear()
        self.signal[1].extend(values)
        return self.signal[1]
        

    def get_binary_numbers(self, num_of_bits):
        self.binary_numbers = []
        total_numbers = 2 ** num_of_bits
    
        for i in range(total_numbers):
            binary_number = format(i, f'0{num_of_bits}b')
            self.binary_numbers.append(binary_number)    
    

    def encode_values(self):
        encoded = {}
        i = 0
        for value in sorted(set(self.signal[1])):
            encoded[value] = self.binary_numbers[i]
            i += 1
        
        new_list = []
        for value in self.signal[1]:
            new_list.append(encoded[value]) 

        return new_list


    def plot_signal(self):
        self.ax.clear()
        self.ax.plot(self.signal[0], self.signal[1])
        self.canvas.draw()


    def print_resutls(self, encoded_values, quantized_values):
        for i in range(len(encoded_values)):
            print(encoded_values[i], '\t', quantized_values[i])
