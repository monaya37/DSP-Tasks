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
        # Create GUI Components
        
        # Create GUI Components
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)

        # Configure columns for even space
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

        # Radio buttons to conv type
        self.function_type = tk.StringVar(value="convolution")
        tk.Radiobutton(self.frame, text="Convolution", variable=self.function_type, value="convolution", font=self.large_font).grid(row=1, column=0, pady=5, sticky='ew')
        tk.Radiobutton(self.frame, text="Derivative", variable=self.function_type, value="derivative", font=self.large_font).grid(row=1, column=1, pady=5, sticky='ew')
        tk.Radiobutton(self.frame, text="Average", variable=self.function_type, value="average", font=self.large_font).grid(row=1, column=2, pady=5, sticky='ew')

        # Label and entry for constant value
        self.constant = tk.IntVar(value=0)  # Initialize to 0
        ttk.Label(self.frame, text="Enter: ", font=self.large_font).grid(row=2, column=0, pady=5)
        self.constant_entry = ttk.Entry(self.frame, textvariable=self.constant)
        self.constant_entry.grid(row=2, column=1, pady=5)

        # Generate the signal button
        generate_button = ttk.Button(self.frame, text="start", command=self.run_algorithm)
        generate_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, pady=10, sticky='ew')

        self.signal = None
        self.signal2 = None


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def run_algorithm(self):
        print("run algo function called")
        self.function_type = self.function_type.get()
        self.window_size = self.constant.get()

        if(self.function_type == "convolution"):

            path = 'testcases\\Convolution testcases\\Signal 1.txt'
            path2 = 'testcases\\Convolution testcases\\Signal 2.txt'

            self.signal = functions.read_signals(path)
            self.signal2 = functions.read_signals(path2)

            self.convolution()

        elif(self.function_type == "derivative"):

            path = 'testcases\\Derivative testcases\\Derivative_input.txt'
            self.signal = functions.read_signals(path)

            self.derivative()

        elif(self.function_type == "average"):

            path = 'testcases\\Moving Average testcases\\MovingAvg_input.txt'
            self.signal = functions.read_signals(path)
            self.window_size = self.constant.get()

            self.average()


    def convolution(self):
        #compute
        print("conv called")

        y = {}
        if(self.signal[0][0] <= self.signal2[0][0]):
            h = self.signal[2]
            x = self.signal2[2]
            print("x",self.signal2[0])
            print("h", self.signal[0])
            #print("last h" , self.signal[0][0])
            start = self.signal[0][0]
            #print("last x", self.singal2[0][-1]) 
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
        output_path = 'testcases/Convolution testcases/Conv_output.txt'
        self.plot_signals(y)
        functions.CompareOutput(indices, values, output_path)

        print("conv output", y)
        #call compare function
        return
    
    def derivative(self):
        print("deriv called")

        #computer using given equations 
        #call compare function
        return
    
    def average(self):
        print("avg called")

        if(self.window_size == 3):
            #compute
            #call compare function
            return
        elif(self.window_size == 5):
            #compute
            #call compare function
            return
        else:
            #warning message box text
            return
            
    

    def plot_signals(self, samples):
        self.ax.clear()
        
        indices = list(samples.keys())
        values = list(samples.values())
        
        self.ax.stem(indices, values)
        self.ax.set_title("Signal Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.grid()
        self.canvas.draw()
 
        return

