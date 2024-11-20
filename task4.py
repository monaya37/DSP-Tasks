import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
from task3_files import QuanTest1, QuanTest2 
import math


class Task4:
    def __init__(self, parent):

        self.parent = parent
        self.large_font = ('Helvetica', 14)
        
        # Create main frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)

        # Radio buttons for function type
        self.radios_frame = tk.Frame(self.frame)

        self.radio = tk.StringVar(value="convolution")
        tk.Radiobutton(self.radios_frame, text="Convolution",  variable=self.radio, value="convolution",       font=self.large_font).grid(row=1, column=0, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="Average",      variable=self.radio, value="average",           font=self.large_font).grid(row=1, column=1, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="1st Derivative", variable=self.radio, value="firstderivative", font=self.large_font).grid(row=1, column=2, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="2nd Derivative", variable=self.radio, value="secondderivative", font=self.large_font).grid(row=1, column=3, padx = 1, pady=3, sticky='ew')
        self.radios_frame.grid(row=1, pady=4, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="Window Size:", font=self.large_font)
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

        self.function_type = self.radio.get()
        if(self.function_type == "convolution"):
            input_path = 'testcases\\Convolution testcases\\Signal 1.txt'
            input_path2 = 'testcases\\Convolution testcases\\Signal 2.txt'
            output_path = 'testcases/Convolution testcases/Conv_output.txt'
            self.signal = functions.read_signals(input_path)
            self.signal2 = functions.read_signals(input_path2)
            self.title = 'Convolution'
            self.convolution(output_path)

        elif(self.function_type == "firstderivative"):
            self.title = '1st Derivative'
            path = 'testcases\\Derivative testcases\\Derivative_input.txt'
            output_path = 'testcases\\Derivative testcases\\1st_derivative_out.txt'
            self.signal = functions.read_signals(path)
            self.first_derivative(output_path)

        elif(self.function_type == "secondderivative"):
            self.title = '2nd Derivative'           
            path = 'testcases\\Derivative testcases\\Derivative_input.txt'
            output_path = 'testcases\\Derivative testcases\\2nd_derivative_out.txt'
            self.signal = functions.read_signals(path)
            self.second_derivative(output_path)

        elif(self.function_type == "average"):
            self.title = 'Average'
            input_path  = 'testcases\\Moving Average testcases\\MovingAvg_input.txt'
            self.signal = functions.read_signals(input_path)

            self.window_size = int(self.ConstantInput.get())
            if(self.window_size == 3):
                output_path = 'testcases\\Moving Average testcases\\MovingAvg_out1.txt'
            elif(self.window_size == 5):
                output_path = 'testcases\\Moving Average testcases\\MovingAvg_out2.txt'
            
            self.average(output_path)


    def convolution(self, output_path):
        y = {}
        if(self.signal[0][0] <= self.signal2[0][0]):
            h = self.signal[2]
            x = self.signal2[2]
            start = self.signal[0][0]
            end = self.signal2[0][-1] + self.signal[0][-1]
        else:
            x = self.signal[2]
            h = self.signal2[2]
            start = self.signal2[0][0]
            end = self.signal2[0][-1] + self.signal[0][-1]
        

        for n in range(start, end+1):
            y[n] = 0
            for k in x.keys():
                if((n - k) in h.keys()):
                    y[n] += x[k] * h[n-k]

        indices = list(y.keys())
        values = list(y.values())

        functions.CompareOutput(indices, values, output_path)
        self.plot_signals(y)

        return
    
    def first_derivative(self, output_path):

        y = {}
        x = self.signal[2]

        for i in x.keys():
            if((i+1) in x.keys()):
                y[i] = x[i+1] - x[i]
 
        indices = list(y.keys())
        values = list(y.values())
        functions.CompareOutput(indices, values, output_path)
        self.plot_signals(y)

        return
    
    def second_derivative(self, output_path):
        y = {}
        x = self.signal[2]

        for i in x.keys():
            if((i+1) in x.keys() and (i-1) in x.keys()):
                y[i-1] = x[i+1] - 2*x[i] + x[i-1]

        indices = list(y.keys())
        values = list(y.values())
        functions.CompareOutput(indices, values, output_path)
        self.plot_signals(y)
        return
    
    def average(self, output_path):

        x = self.signal[2]
        indices = list(x.keys())
        values = list(x.values())
        samples = {}
        moving_avg = []
        valid_indices = []  # Keep track of indices for valid moving averages
        for i in range(len(values)):
            if i < self.window_size - 1:
                continue  # Skip indices where averaging cannot be done
            avg = round(sum(values[i - self.window_size + 1:i + 1]) / self.window_size, 3)
            moving_avg.append(avg)
            valid_indices.append(indices[i] - self.window_size+ 1)  # Record valid index
            samples[indices[i] - self.window_size+ 1] = avg
            
        values = [round(val, 3) if not val.is_integer() else int(val) for val in moving_avg]
        functions.CompareOutput(valid_indices, moving_avg, output_path)
        self.plot_signals(samples)

    

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
    


