# task1.py
import tkinter as tk
from tkinter import filedialog, messagebox, Text
from functions import *

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

        # Result Text Area
        self.result_text = Text(self.frame, width=80, height=15)
        self.result_text.grid(row=5, column=0, columnspan=2, pady=10)

    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def upload_file1(self):
        file_path = filedialog.askopenfilename(title="Select Signal 1 File")
        self.signalA = functions.read_signals(file_path)

    def upload_file2(self):
        file_path = filedialog.askopenfilename(title="Select Signal 2 File")
        self.signalB = functions.read_signals(file_path)

    def add_signals(self):
        if self.signalA is None or self.signalB is None:
            messagebox.showwarning("Missing Files", "Please upload both Signal files!")
            return

        operation = "Addition Result:\n"
        signal = functions.add_signals(self.signalA, self.signalB)
        self.display_result(signal, operation)
        AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", signal[0], signal[1])

      
        
    
    def sub_signals():
        if self.signalA is None or task1.signalB is None:
            messagebox.showwarning("Missing Files", "Please upload both Signal files!")
            return

        operation = "Subtraction Result:\n"
        signal = functions.sub_signals(self.signalA, self.signalB)
        self.display_result(signal, operation)
        SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", signal[0], signal[1])


    def multiply_signals():
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        constant = int(self.ConstantInput.get())
        operation = f"Multiplication Result (by {constant}):\n"

        signal = functions.multiply_signals(self.signalA, constant)
        self.display_result(signal, operation)
        MultiplySignalByConst(constant, signal[0], signal[1])



    def shift_signal():
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        constant = int(self.ConstantInput.get()) 
        operation = f"Shift Result (by {constant}):\n"

        signal = functions.shift_signal(self.signalA, constant)
        self.display_result(signal, operation)
        ShiftSignalByConst(constant, signal[0], signal[1])


    def fold_signals():
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        operation = "Fold Result:\n"
        signal = functions.fold_signals(self.signalA)
        self.display_result(signal, operation)
        Folding(signal[0], signal[1])


    def plot_signals(samples):
        indices = list(samples.keys())
        values = list(samples.values())
        plt.figure(figsize=(10, 5))
        plt.stem(indices, values)
        plt.title("Signal Visualization")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.grid()
        plt.show()


    def display_result(signal, result):
        result += "\n".join([f"{idx}: {val}" for idx, val in zip(signal[0], signal[1])])
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, result)
        self.plot_signals(signal[2])
