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
        self.function_type = tk.StringVar(value="convolution")
        tk.Radiobutton(self.frame, text="Convolution", variable=self.function_type, value="convolution", font=self.large_font).grid(row=1, column=0, pady=5, sticky='ew')
        tk.Radiobutton(self.frame, text="Derivative", variable=self.function_type, value="derivative", font=self.large_font).grid(row=1, column=1, pady=5, sticky='ew')
        tk.Radiobutton(self.frame, text="Average", variable=self.function_type, value="average", font=self.large_font).grid(row=1, column=2, pady=5, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="Constant:", font=self.large_font)
        self.label.pack(side='left', padx=0)
        self.ConstantInput = tk.Entry(self.label_entry_frame, width=40)
        self.ConstantInput.pack(side='left', padx=0)
        self.label_entry_frame.grid(row=2, column=1, padx=(5, 10), pady=4, sticky='ew')

        # Start button
        generate_button = ttk.Button(self.frame, text="Start", command=self.run_algorithm)
        generate_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Plotting area (centered)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=4, column=0, columnspan=3, pady=10, sticky='nsew')

        self.signal = None
        self.signal2 = None


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def run_algorithm(self):
        print("run algo function called")
        self.window_size = self.ConstantInput.get()
        self.function_type = self.function_type.get()
        print(self.function_type)
        if(self.function_type == "convolution"):

            input_path = 'testcases\\Convolution testcases\\Signal 1.txt'
            input_path2 = 'testcases\\Convolution testcases\\Signal 2.txt'
            print("in")

            self.signal = functions.read_signals(input_path)
            self.signal2 = functions.read_signals(input_path2)

            self.convolution()

        elif(self.function_type == "derivative"):

            path = 'testcases\\Derivative testcases\\Derivative_input.txt'
            self.signal = functions.read_signals(path)

            self.derivative()

        elif(self.function_type == "average"):

            input_path  = 'testcases\\Moving Average testcases\\MovingAvg_input.txt'

            self.signal = functions.read_signals(input_path)
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
        self.plot_signals(y)

        output_path = 'testcases/Convolution testcases/Conv_output.txt'
        functions.CompareOutput(indices, values, output_path)

        #call compare function
        return
    
    def derivative(self):
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
    


