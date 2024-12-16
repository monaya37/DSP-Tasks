import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
from task3_files import QuanTest1, QuanTest2 
import math


class Task3:
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

        large_font = ('Helvetica', 14)


        self.num_of_bits = tk.IntVar(value=0)  # Initialize to 0 instead of None
        self.num_of_levels = tk.IntVar(value=0)  # Initialize to 0

        ttk.Label(self.frame, text="Number of bits:", font=large_font).grid(row=2, column=0, pady=5)
        self.bits_entry = ttk.Entry(self.frame, textvariable=self.num_of_bits)
        self.bits_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Number of levels:", font=large_font).grid(row=3, column=0, pady=5)
        self.levels_entry = ttk.Entry(self.frame, textvariable=self.num_of_levels)
        self.levels_entry.grid(row=3, column=1, pady=5)

        # Radio buttons to select sine or cosine
        self.test = tk.StringVar(value="Test1")
        tk.Radiobutton(self.frame, text="Test 1", variable=self.test, value="Test1", font=large_font).grid(row=4, column=0, pady=5)
        tk.Radiobutton(self.frame, text="Test 2", variable=self.test, value="Test2", font=large_font).grid(row=4, column=1, pady=5)

        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=large_font)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command=self.choose_test, style='Large.TButton')
        generate_button.grid(row=6, column=0, columnspan=2, rowspan= 1, pady=10)

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        self.signal = None
        self.midpoints = []



    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()


    def choose_test(self):

        test = self.test.get()
        levels = self.num_of_levels.get()
        bits = self.num_of_bits.get()

        if levels == 0:  
            self.num_of_levels.set(math.pow(2, int(bits))) #display it in text box
            levels = self.num_of_levels.get()

        if bits == 0:  
            self.num_of_bits.set(math.log2(int(levels)))
            bits = self.num_of_bits.get()


        if(test == "Test1"):
            intervals_indecies,encoded_values,quantized_values,errors = self.process_quantization("task3_files\\Quan1_input.txt", levels, bits)
            QuanTest1.QuantizationTest1('task3_files\\Quan1_Out.txt', encoded_values, quantized_values)

        else:
            intervals_indecies,encoded_values,quantized_values,errors = self.process_quantization("task3_files\\Quan2_input.txt", levels, bits)
            QuanTest2.QuantizationTest2('task3_files\\Quan2_Out.txt',intervals_indecies,encoded_values,quantized_values,errors)

        self.num_of_levels.set(0) #reset
        self.num_of_bits.set(0) #reset
        self.midpoints.clear()


    def process_quantization(self, path, levels, bits):
        self.signal = ReadSignals(path)
            
        intervals = self.get_intervals(levels)
        quantized_values, errors = self.quantize_values(intervals)
        binary_numbers = self.get_binary_numbers(bits)
        intervals_indecies, encoded_values = self.encode_values(binary_numbers, quantized_values)

        self.plot_signal()
        self.print_resutls(intervals_indecies, encoded_values, quantized_values, errors)
        
        return intervals_indecies, encoded_values, quantized_values, errors
    

    def get_intervals(self, levels): #ranges

        intervals = []

        start = min(self.signal[1])  
        end = max(self.signal[1])
        delta = end - start
        delta = round(delta / float(levels), 3) 

        end = round(start + delta, 3)
        for _ in range(int(levels)):  
            intervals.append((start, end))
            start = end
            end = round(start + delta, 3)

        return intervals


    def quantize_values(self, intervals):

        quantized_values = []
        errors = []

        for element in self.signal[1]: #y value
            for start, end in intervals: 

                midpoint = round((start + end) / 2, 3) 
                self.midpoints.append(midpoint)

                if start <= element <= end:
                    quantized_values.append(midpoint) 
                    errors.append(round(midpoint - element, 3)) #error
                    break

        self.signal[1].clear()
        self.signal[1].extend(quantized_values) #will then be used to plot

        return quantized_values, errors
        

    def get_binary_numbers(self, num_of_bits):
        binary_numbers = []
        total_numbers = 2 ** num_of_bits
    
        for i in range(total_numbers):
            binary_number = format(i, f'0{num_of_bits}b')
            binary_numbers.append(binary_number)

        return binary_numbers   
    

    def encode_values(self, binary_numbers, quantized_values): #to binary

        encoded = {}

        i = 0
        for value in sorted(set(self.midpoints)):
            encoded[value] = [i+1, binary_numbers[i]]  
            i += 1
        
        encoded_values = []
        intervals_indecies = []
        for value in quantized_values:
            intervals_indecies.append(encoded[value][0]) #interval index
            encoded_values.append(encoded[value][1]) #interval index in binary

        return intervals_indecies, encoded_values


    def plot_signal(self):
        self.ax.clear()
        self.ax.plot(self.signal[0], self.signal[1])
        self.canvas.draw()


    def print_resutls(self,intervals_indecies,encoded_values,quantized_values,errors):
        for i in range(len(encoded_values)):
            print('\t', intervals_indecies[i], '\t',  encoded_values[i], '\t', quantized_values[i], '\t', errors[i])
