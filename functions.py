import tkinter as tk
from tkinter import filedialog, messagebox, Text
from DSP_Task2_TEST_functions import *
import matplotlib.pyplot as plt

# %%
def plot_signal(samples):
    indices = list(samples.keys())
    values = list(samples.values())
    plt.figure(figsize=(10, 5))
    plt.stem(indices, values)
    plt.title('Signal Visualization')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.grid()
    plt.show()

# Read Files
def read_signals(file_path):
    samples = {}
    with open(file_path, 'r') as file:
        for line in file:
            number_of_samples = int(line.strip())
            if number_of_samples == 0:
                continue

            for _ in range(number_of_samples):
                line = file.readline()
                #read every single line, converts the values from string to float
                index, value = map(float, line.strip().split()) 
                samples[int(index)] = value

        indices = list(samples.keys())
        values = list(samples.values())
        plot_signal(samples)
    return indices, values, samples


def add_signals(signal_a, signal_b):
    combined = {}

    # Add values from the first signal
    for index, value in signal_a[2].items():
        combined[index] = value

    # Add values from the second signal
    for index, value in signal_b[2].items():
        if index in combined:
            combined[index] += value  # Sum the values for overlapping keys
        else:
            combined[index] = value  # Add new key-value pairs

    combined = dict(sorted(combined.items()))
    indices = list(combined.keys())
    values = list(combined.values())
    return indices, values, combined


def sub_signals(signal_a, signal_b):
    combined = {}

    # Add values from the first signal
    for index, value in signal_a[2].items():
        combined[index] = value

    # Subtract values from the second signal
    for index, value in signal_b[2].items():
        if index in combined:
            combined[index] -= value  # Subtract the values for overlapping keys
        else:
            combined[index] = -value  # Add new key-value pairs

    combined = dict(sorted(combined.items()))
    indices = list(combined.keys())
    values = list(combined.values())
    return indices, values, combined


def multiply_signals(signal_a, constant):
    combined = {}
    for index, value in signal_a[2].items():
        combined[index] = value * constant

    combined = dict(sorted(combined.items()))
    indices = list(combined.keys())
    values = list(combined.values())
    return indices, values, combined


def shift_signal(signal_a, constant):
    combined = {}
    for index, value in signal_a[2].items():
        combined[index + -1* constant] = value

    combined = dict(sorted(combined.items()))
    indices = list(combined.keys())
    values = list(combined.values())
    return indices, values, combined


def fold_signals(signal_a):
    combined = {}

    # Fold the signal by reversing the index
    for index, value in signal_a[2].items():
        combined[-index] = value

    combined = dict(sorted(combined.items()))
    indices = list(combined.keys())
    values = list(combined.values())
    return indices, values, combined


# GUI Application Class
class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Signal Processing GUI")
        self.signalA = None
        self.signalB = None
        self.root.configure(padx=20, pady=20)

        # Create GUI Components
        # Buttons
        button_width = 45  
        pad_y = 5

        self.file1_button = tk.Button(root, text="Upload SignalA", command=self.upload_file1, width=button_width)
        self.file1_button.grid(row=1, column=0, padx=(5, 10), pady=pad_y, sticky='ew')

        self.file2_button = tk.Button(root, text="Upload SignalB", command=self.upload_file2, width=button_width)
        self.file2_button.grid(row=1, column=1, padx=(5, 10), pady=pad_y, sticky='ew')

        self.add_button = tk.Button(root, text="Add Signals and Display", command=self.add_signals, width=button_width)
        self.add_button.grid(row=2, column=0, padx=(5, 10), pady=pad_y, sticky='ew')

        self.sub_button = tk.Button(root, text="Subtract Signals and Display", command=self.sub_signals, width=button_width)
        self.sub_button.grid(row=2, column=1, padx=(5, 10), pady=pad_y, sticky='ew')

        self.mul_button = tk.Button(root, text="Multiply SignalA by Constant", command=self.multiply_signals, width=button_width)
        self.mul_button.grid(row=3, column=0, padx=(5, 10), pady=pad_y, sticky='ew')

        self.shift_button = tk.Button(root, text="Shift SignalA and Display", command=self.shift_signal, width=button_width)
        self.shift_button.grid(row=3, column=1, padx=(5, 10), pady=pad_y, sticky='ew')

        self.fold_button = tk.Button(root, text="Fold SignalA and Display", command=self.fold_signals, width=button_width)
        self.fold_button.grid(row=4, column=0, padx=(5, 10), pady=pad_y, sticky='ew')

        # Create a frame for the label and entry
        self.label_entry_frame = tk.Frame(root)
        
        self.label = tk.Label(self.label_entry_frame, text="Constant:")
        self.label.pack(side='left', padx=0)  # Pack the label to the left
        
        self.ConstantInput = tk.Entry(self.label_entry_frame, width = 40)  # Set a width for the entry
        self.ConstantInput.pack(side='left', padx=0)  # Pack the entry to the left

        self.label_entry_frame.grid(row=4, column=1, padx=(5, 10), pady=pad_y, sticky='ew')

        # Result Text Area
        self.result_text = Text(root, width=80, height=15)
        self.result_text.grid(row=5, column=0, columnspan=2, pady=10)

        # Configure column weights for centering
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)



    def upload_file1(self):
        file_path = filedialog.askopenfilename(title="Select Signal 1 File")
        self.signalA = read_signals(file_path)
        #messagebox.showinfo("File Upload", f"Signal 1 uploaded: {file_path}")

    def upload_file2(self):
        file_path = filedialog.askopenfilename(title="Select Signal 2 File")
        self.signalB = read_signals(file_path)
        #messagebox.showinfo("File Upload", f"Signal 2 uploaded: {file_path}")

    def add_signals(self):
        if self.signalA is None or self.signalB is None:
            messagebox.showwarning("Missing Files", "Please upload both Signal files!")
            return

        add_indices, add_values, samples = add_signals(self.signalA, self.signalB)
        result = "Addition Result:\n"
        result += "\n".join([f"{idx}: {val}" for idx, val in zip(add_indices, add_values)])
        self.display_result(result)
        self.plot_signals(samples)
        AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", add_indices, add_values)
        

    def sub_signals(self):
        if self.signalA is None or self.signalB is None:
            messagebox.showwarning("Missing Files", "Please upload both Signal files!")
            return

        sub_indices, sub_values, samples = sub_signals(self.signalA, self.signalB)
        result = "Subtraction Result:\n"
        result += "\n".join([f"{idx}: {val}" for idx, val in zip(sub_indices, sub_values)])
        self.display_result(result)
        self.plot_signals(samples)
        SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", sub_indices, sub_values)


    def multiply_signals(self):
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        constant = int(self.ConstantInput.get())
        mul_indices, mul_values, samples = multiply_signals(self.signalA, constant)
        result = f"Multiplication Result (by {constant}):\n"
        result += "\n".join([f"{idx}: {val}" for idx, val in zip(mul_indices, mul_values)])
        self.display_result(result)
        self.plot_signals(samples)
        MultiplySignalByConst(5, mul_indices, mul_values)



    def shift_signal(self):
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        constant = int(self.ConstantInput.get()) 
        shift_indices, shift_values, samples = shift_signal(self.signalA, constant)
        result = f"Shift Result (by {constant}):\n"
        result += "\n".join([f"{idx}: {val}" for idx, val in zip(shift_indices, shift_values)])
        self.display_result(result)
        self.plot_signals(samples)
        ShiftSignalByConst(constant, shift_indices, shift_values)


    def fold_signals(self):
        if self.signalA is None:
            messagebox.showwarning("Missing File", "Please upload Signal A file!")
            return

        fold_indices, fold_values, samples = fold_signals(self.signalA)
        result = "Fold Result:\n"
        result += "\n".join([f"{idx}: {val}" for idx, val in zip(fold_indices, fold_values)])
        self.display_result(result)
        self.plot_signals(samples)
        Folding(fold_indices, fold_values)


    def plot_signals(self, samples):
        plot_signal(samples)


    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, result)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = SignalApp(root)
    root.mainloop()




