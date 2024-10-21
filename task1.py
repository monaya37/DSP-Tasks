# task1.py
import tkinter as tk
from tkinter import filedialog, messagebox, Text
from functions import *
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class Task1:
    def __init__(self, parent):
        self.parent = parent
        self.signalA = None
        self.signalB = None

        # Create GUI Components but do not grid them yet
        self.frame = tk.Frame(self.parent)

        self.button_width = 45  
        self.pad_y = 5

        self.file1_button = tk.Button(self.frame, text="Upload SignalA", command=self.upload_file1, width=self.button_width)
        self.file1_button.grid(row=1, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.file2_button = tk.Button(self.frame, text="Upload SignalB", command=self.upload_file2, width=self.button_width)
        self.file2_button.grid(row=1, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.add_button = tk.Button(self.frame, text="Add Signals and Display", command=self.add_signals, width=self.button_width)
        self.add_button.grid(row=2, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.sub_button = tk.Button(self.frame, text="Subtract Signals and Display", command=self.sub_signals, width=self.button_width)
        self.sub_button.grid(row=2, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.mul_button = tk.Button(self.frame, text="Multiply SignalA by Constant", command=self.multiply_signals, width=self.button_width)
        self.mul_button.grid(row=3, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.shift_button = tk.Button(self.frame, text="Shift SignalA and Display", command=self.shift_signal, width=self.button_width)
        self.shift_button.grid(row=3, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.fold_button = tk.Button(self.frame, text="Fold SignalA and Display", command=self.fold_signals, width=self.button_width)
        self.fold_button.grid(row=4, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="Constant:")
        self.label.pack(side='left', padx=0)
        
        self.ConstantInput = tk.Entry(self.label_entry_frame, width=40)
        self.ConstantInput.pack(side='left', padx=0)

        self.label_entry_frame.grid(row=4, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def upload_file1(self):
        file_path = filedialog.askopenfilename(title="Select Signal 1 File")
        self.signalA = functions.read_signals(file_path)
        self.plot_signals(self.signalA[2]) 

    def upload_file2(self):
        file_path = filedialog.askopenfilename(title="Select Signal 2 File")
        self.signalB = functions.read_signals(file_path)
        self.plot_signals(self.signalB[2]) 


    def add_signals(self):
        if self.signalA is None or self.signalB is None:
            messagebox.showwarning("Missing Files", "Please upload both Signal files!")
            return

        signal = functions.add_signals(self.signalA, self.signalB)
        self.plot_signals(signal[2]) 
        AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", signal[0], signal[1])

      
        
    
    def sub_signals(self):
        if self.signalA is None or self.signalB is None:
            messagebox.showwarning("Missing Files", "Please upload both Signal files!")
            return

        signal = functions.sub_signals(self.signalA, self.signalB)
        self.plot_signals(signal[2])  

        SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", signal[0], signal[1])


    def multiply_signals(self):
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        constant = int(self.ConstantInput.get())

        signal = functions.multiply_signals(self.signalA, constant)
        self.plot_signals(signal[2])  
        
        MultiplySignalByConst(constant, signal[0], signal[1])



    def shift_signal(self):
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        constant = int(self.ConstantInput.get()) 

        signal = functions.shift_signal(self.signalA, constant)
        self.plot_signals(signal[2])  

        ShiftSignalByConst(constant, signal[0], signal[1])


    def fold_signals(self):
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        signal = functions.fold_signals(self.signalA)   
        self.plot_signals(signal[2])  
        Folding(signal[0], signal[1])



    def plot_signals(self, samples):
        indices = list(samples.keys())
        values = list(samples.values())
        
        # Create a figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.stem(indices, values)
        ax.set_title("Signal Visualization")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.grid()

        # Clear previous plot if it exists
        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()  # Remove the previous canvas

        # Create a canvas to display the plot
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)  # Use your main frame or window as the master
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, pady=10)  # Adjust row/column as needed
 

