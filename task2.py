# task2.py
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Task2:
    def __init__(self, parent):
        self.parent = parent

        # Create GUI Components
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)  

        large_font = ('Helvetica', 14)
        self.button_width = 35  

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)


        # Radio buttons to select sine or cosine
        self.function_type = tk.StringVar(value="Sine")
        tk.Radiobutton(self.frame, text="Sine", variable=self.function_type, value="Sine", font=large_font).grid(row=0, column=1, pady=5)
        tk.Radiobutton(self.frame, text="Cosine", variable=self.function_type, value="Cosine", font=large_font).grid(row=1, column=1, pady=5)

        # Radio buttons to select sine or cosine
        self.signal_type = tk.StringVar(value="Continuous")
        tk.Radiobutton(self.frame, text="Continuous", variable=self.signal_type, value="Continuous", font=large_font).grid(row=0, column=0, pady=5)
        tk.Radiobutton(self.frame, text="Discrete", variable=self.signal_type, value="Discrete", font=large_font).grid(row=1, column=0, pady=5)

        # Input fields for amplitude, frequency, phase, sampling
        self.amplitude = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)
        self.frequency = tk.DoubleVar(value=1.0)
        self.sampling_rate = tk.DoubleVar(value=50.0)

        ttk.Label(self.frame, text="Amplitude:", font=large_font).grid(row=2, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.amplitude).grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Phase Shift (theta):", font=large_font).grid(row=3, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.phase).grid(row=3, column=1, pady=5)

        ttk.Label(self.frame, text="Analog Frequency:", font=large_font).grid(row=4, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.frequency).grid(row=4, column=1, pady=5)

        ttk.Label(self.frame, text="Sampling Frequency:", font=large_font).grid(row=5, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.sampling_rate).grid(row=5, column=1, pady=5)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", width=self.button_width, command=self.generate_signal)
        generate_button.grid(row=6, column=0, columnspan=2, pady=10)

    def clear_plot(self):
        self.ax.clear()

    def show_plot(self):
        self.canvas.draw()


    def generate_signal(self):
        self.clear_plot()  # Clear any existing plot

        signal_type = self.signal_type.get()
        function_type = self.function_type.get()
        A = self.amplitude.get()
        theta = self.phase.get()
        f = self.frequency.get()
        fs = self.sampling_rate.get()

        if fs < 2 * f:
            messagebox.showerror("Error", "Sampling frequency must be at least twice the analog frequency.")
            return

        t = np.linspace(0, 1, int(fs))
        if function_type == "Sine":
            signal = A * np.sin(2 * np.pi * f * t + theta)
        else:
            signal = A * np.cos(2 * np.pi * f * t + theta)

        if signal_type == "Discrete":
            self.ax.stem(t[::], signal)
        else:
            self.ax.plot(t, signal)
        # Plot the generated signal
        self.ax.set_title(f"{function_type} Wave (A={A}, f={f}, θ={theta})")

        self.canvas.draw()

    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()
