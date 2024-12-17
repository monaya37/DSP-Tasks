import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from files.functions import *
from task3_files import QuanTest1, QuanTest2 
import math


class Task7:
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


        self.num_of_bits = tk.IntVar(value=0)  # Initialize to 0 instead of None
        self.num_of_levels = tk.IntVar(value=0)  # Initialize to 0

        ttk.Label(self.frame, text="practical:", font=large_font).grid(row=2, column=0, pady=5)
        self.bits_entry = ttk.Entry(self.frame, textvariable=self.num_of_bits)
        self.bits_entry.grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Number of levels:", font=large_font).grid(row=3, column=0, pady=5)
        self.levels_entry = ttk.Entry(self.frame, textvariable=self.num_of_levels)
        self.levels_entry.grid(row=3, column=1, pady=5)

        # Radio buttons to select sine or cosine
        self.test = tk.StringVar(value="Test1")
        tk.Radiobutton(self.frame, text="Test 1", variable=self.test, value="Test1", font=large_font).grid(row=4, column=0, pady=5)
        tk.Radiobutton(self.frame, text="Test 2", variable=self.test, value="Test2", font=large_font).grid(row=4, column=1, pady=5)

        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=large_font)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command=self.choose_test, style='Large.TButton')
        generate_button.grid(row=6, column=0, columnspan=2, rowspan= 1, pady=10)

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        self.signal = None
        self.midpoints = []



    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()
