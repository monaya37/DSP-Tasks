# task2.py
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Task2:
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
        self.button_width = 35  
        self.pad_y = 2

        # Radio buttons to select sine or cosine
        self.function_radio = tk.StringVar(value="Sine")
        tk.Radiobutton(self.frame, text="Sine", variable=self.function_radio, value="Sine", font=large_font).grid(row=0, column=1, padx=(5, 10), pady=self.pad_y, sticky="n")
        tk.Radiobutton(self.frame, text="Cosine", variable=self.function_radio, value="Cosine", font=large_font).grid(row=1, column=1, padx=(5, 10), pady=self.pad_y, sticky="n")

        # Radio buttons to select sine or cosine
        self.signal_radio = tk.StringVar(value="Continuous")
        tk.Radiobutton(self.frame, text="Continuous", variable=self.signal_radio, value="Continuous", font=large_font).grid(row=0, column=0, padx=(5, 10), pady=self.pad_y, sticky="n")
        tk.Radiobutton(self.frame, text="Discrete", variable=self.signal_radio, value="Discrete", font=large_font).grid(row=1, column=0, padx=(5, 10), pady=self.pad_y, sticky="n")

        # Input fields for amplitude, frequency, phase, sampling
        self.amplitude_entry = tk.DoubleVar(value=1.0)
        self.theta_entry = tk.DoubleVar(value=0.0)
        self.frequency_entry = tk.DoubleVar(value=1.0)
        self.sampling_rate_entry = tk.DoubleVar(value=50.0)

        frame = self.frame
        pad_y = self.pad_y

        # Label and Entry for Amplitude
        ttk.Label(frame, text="Amplitude:", font=large_font).grid(row=2, column=0, padx=(5, 10), pady=pad_y, sticky="n")
        ttk.Entry(frame, textvariable=tk.StringVar()).grid(row=2, column=1, padx=(20, 10), pady=pad_y, sticky="n")  # Increased padx to add space

        # Label and Entry for Phase Shift (theta)
        ttk.Label(frame, text="Phase Shift (theta):", font=large_font).grid(row=3, column=0, padx=(5, 10), pady=pad_y, sticky="n")
        ttk.Entry(frame, textvariable=tk.StringVar()).grid(row=3, column=1, padx=(20, 10), pady=pad_y, sticky="n")  # Increased padx

        # Label and Entry for Analog Frequency
        ttk.Label(frame, text="Analog Frequency:", font=large_font).grid(row=4, column=0, padx=(5, 10), pady=pad_y, sticky="n")
        ttk.Entry(frame, textvariable=tk.StringVar()).grid(row=4, column=1, padx=(20, 10), pady=pad_y, sticky="n")  # Increased padx

        # Label and Entry for Sampling Frequency
        ttk.Label(frame, text="Sampling Frequency:", font=large_font).grid(row=5, column=0, padx=(5, 10), pady=pad_y, sticky="n")
        ttk.Entry(frame, textvariable=tk.StringVar()).grid(row=5, column=1, padx=(20, 10), pady=pad_y, sticky="n") 

        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=('Helvetica', 14), padding=(3, 3))
        
        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal",  width=self.button_width, command=self.GenerateSignal, style='Large.TButton')
        generate_button.grid(row=6, column=0, columnspan=2, padx=(5, 10), pady=self.pad_y, sticky="n")

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)






    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()


    def GenerateSignal(self):

        self.signal_type = self.signal_radio.get()
        self.function_type = self.function_radio.get()
        self.theta = self.theta_entry.get()

        self.amplitude = self.amplitude_entry.get()
        self.frequency = self.frequency_entry.get()
        self.sampling_rate = self.sampling_rate_entry.get()

        if self.sampling_rate < 2 * self.frequency:
            messagebox.showerror("Error", "Sampling frequency must be at least twice the analog frequency.")
            return
        
        self.PlotSignal()


    def PlotSignal(self):

        self.ax.clear()

        t = np.linspace(0, 1, int(self.sampling_rate))
        if self.function_type == "Sine":
            signal = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.theta)
        else:
            signal = self.amplitude * np.cos(2 * np.pi * self.frequency * t + self.theta)

        if self.signal_type == "Discrete":
            self.ax.stem(t[::], signal)
        else:
            self.ax.plot(t, signal)

        # Plot the generated signal
        self.ax.set_title(f"{self.function_type} Wave (A={self.amplitude}, f={self.frequency}, θ={self.theta})")
        self.canvas.draw()

