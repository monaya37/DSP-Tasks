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
        large_font = ('Helvetica', 14)

        # Create GUI Components
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)  

        # Radio buttons to conv type
        self.conv_type = tk.StringVar(value="convolution")
        tk.Radiobutton(self.frame, text="Convolution", variable=self.conv_type, value="convolution", font=large_font).grid(row=1, column=0, pady=5)
        tk.Radiobutton(self.frame, text="Derivative", variable=self.conv_type, value="derivative", font=large_font).grid(row=1, column=1, pady=5)
        tk.Radiobutton(self.frame, text="Average", variable=self.conv_type, value="average", font=large_font).grid(row=1, column=2, pady=5)

        # Radio buttons to select input signal
        # self.avarage_signal = tk.StringVar(value="Signal1")
        # tk.Radiobutton(self.frame, text="Signal 1", variable=self.avarage_signal, value="Signal1", font=large_font).grid(row=4, column=0, pady=5)
        # tk.Radiobutton(self.frame, text="Signal 2", variable=self.avarage_signal, value="Signal2", font=large_font).grid(row=4, column=1, pady=5)

        # Figure and canvas for plotting
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        self.fig2, self.ax3= plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig2, master=self.frame)
        self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=2, pady=10)

        self.constant = tk.IntVar(value=0)  # Initialize to 0
        ttk.Label(self.frame, text="Enter: ", font=large_font).grid(row=3, column=0, pady=5)
        self.constant_entry = ttk.Entry(self.frame, textvariable=self.constant)
        self.constant_entry.grid(row=3, column=1, pady=5)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="start", command=self.run_algorithm)
        generate_button.grid(row=6, column=0, columnspan=2, rowspan= 1, pady=10)

        self.signal = None
        self.signal2 = None


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def run_algorithm(self):

        self.window_size = self.constant.get()
        self.conv_type = self.conv_type.get()
        if(self.conv_type == "convolution"):

            path = 'testcases\Convolution testcases\Signal 1.txt'
            path2 = 'testcases\Convolution testcases\Signal 2.txt'

            self.signal = functions.read_signals(path)
            self.signal2 = functions.read_signals(path2)

            self.convolution()

        elif(self.conv_type == "derivative"):

            path = 'testcases\Derivative testcases\Derivative_input.txt'
            self.signal = functions.read_signals(path)

            self.derivative()

        elif(self.conv_type == "average"):

            path = 'testcases\Moving Average testcases\MovingAvg_input.txt'
            self.signal = functions.read_signals(path)
            self.window_size = self.constant.get()

            self.average()


    def convolution(self):
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
        self.plot_signals(y)

        output_path = 'testcases/Convolution testcases/Conv_output.txt'
        #functions.CompareOutput(indices, values, output_path)
        return
    
    def derivative(self):
        #computer using given equations 
        #call compare function
        return
    
    def average(self):

        # Compute moving average
        x = self.signal[2]
        M = self.constant_entry.get()
        indices = list(x.keys())
        values = list(x.values())
        moving_avg = []
        valid_indices = []  # Keep track of indices for valid moving averages
        for i in range(len(values)):
            if i < M - 1:
                continue  # Skip indices where averaging cannot be done
            avg = round(sum(values[i - M + 1:i + 1]) / M, 3)
            moving_avg.append(avg)
            valid_indices.append(indices[i])  # Record valid index
        print("RGer", M)

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

