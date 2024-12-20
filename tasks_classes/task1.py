# task1.py
import tkinter as tk
from tasks_classes.functions import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Task1:
    def __init__(self, parent):
        self.parent = parent

        self.signalA = None
        self.signalB = None

        # Create GUI Components but do not grid them yet
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
        self.button_width = 32  
        self.pad_y = 4

        self.file1_button = tk.Button(self.frame, text="Display SignalA", command=self.upload_file1, width=self.button_width, font=large_font)
        self.file1_button.grid(row=1, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.file2_button = tk.Button(self.frame, text="Display SignalB", command=self.upload_file2, width=self.button_width, font=large_font)
        self.file2_button.grid(row=1, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.add_button = tk.Button(self.frame, text="Add Signals and Display", command=self.add_signals, width=self.button_width, font=large_font)
        self.add_button.grid(row=2, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.sub_button = tk.Button(self.frame, text="Subtract Signals and Display", command=self.sub_signals, width=self.button_width, font=large_font)
        self.sub_button.grid(row=2, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.mul_button = tk.Button(self.frame, text="Multiply SignalA by Constant", command=self.multiply_signals, width=self.button_width, font=large_font)
        self.mul_button.grid(row=3, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.shift_button = tk.Button(self.frame, text="Shift SignalA and Display", command=self.shift_signal, width=self.button_width, font=large_font)
        self.shift_button.grid(row=3, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        self.fold_button = tk.Button(self.frame, text="Fold SignalA and Display", command=self.fold_signals, width=self.button_width, font=large_font)
        self.fold_button.grid(row=4, column=0, padx=(5, 10), pady=self.pad_y, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="Constant:", font=large_font)
        self.label.pack(side='left', padx=0)
        
        self.ConstantInput = tk.Entry(self.label_entry_frame, width=40)
        self.ConstantInput.pack(side='left', padx=0)

        self.label_entry_frame.grid(row=4, column=1, padx=(5, 10), pady=self.pad_y, sticky='ew')

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        self.path1 = r'task1_files\Signal1.txt'
        self.path2 = r'task1_files\Signal2.txt'



    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def upload_file1(self):
        self.signalA = ReadSignals(self.path1)
        PlotSignal(self.signalA[2], self.ax, self.canvas) 

    def upload_file2(self):
        self.signalB = ReadSignals(self.path2)
        PlotSignal(self.signalB[2], self.ax, self.canvas) 


    def add_signals(self):
        indices, values, samples = add_signals(self.signalA, self.signalB)
        PlotSignal(samples, self.ax, self.canvas) 

        AddSignalSamplesAreEqual(self.path1, self.path2,  indices, values,)

    
    def sub_signals(self):
        indices, values, samples = sub_signals(self.signalA, self.signalB)

        PlotSignal(samples, self.ax, self.canvas) 
        SubSignalSamplesAreEqual(self.path1, self.path2, indices, values)


    def multiply_signals(self):
        constant = int(self.ConstantInput.get())
        indices, values, samples = multiply_signals(self.signalA, constant)

        PlotSignal(samples, self.ax, self.canvas) 
        MultiplySignalByConst(constant, indices, values)



    def shift_signal(self):
        constant = int(self.ConstantInput.get()) 
        indices, values, samples = shift_signal(self.signalA, constant)

        PlotSignal(samples, self.ax, self.canvas) 
        ShiftSignalByConst(constant, indices, values)


    def fold_signals(self):
        indices, values, samples = fold_signals(self.signalA)  

        PlotSignal(samples, self.ax, self.canvas) 
        Folding(indices, values)



    


