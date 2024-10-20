import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SignalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Signal Processing Framework")
        self.geometry("800x600")

        # Create Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        # Create tabs
        self.create_signal_display_tab()
        self.create_signal_generation_tab()

        # figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack_forget()  # Initially hidden

    def create_signal_display_tab(self):
        # Signal Display Tab
        signal_display_tab = ttk.Frame(self.notebook)
        self.notebook.add(signal_display_tab, text="Signal Display")

        # Dropdown to choose between continuous or discrete
        self.signal_type_var = tk.StringVar(value="Continuous")
        signal_type_menu = ttk.OptionMenu(signal_display_tab, self.signal_type_var, "Continuous", "Continuous", "Discrete")
        signal_type_menu.pack(pady=10)

        plot_button = ttk.Button(signal_display_tab, text="Plot Signal", command=self.plot_signal)
        plot_button.pack(pady=10)

    def create_signal_generation_tab(self):
        signal_gen_tab = ttk.Frame(self.notebook)
        self.notebook.add(signal_gen_tab, text="Signal Generation")

        # Radio buttons to select sine or cosine
        self.signal_type = tk.StringVar(value="Sine")
        tk.Radiobutton(signal_gen_tab, text="Sine", variable=self.signal_type, value="Sine").pack(pady=5)
        tk.Radiobutton(signal_gen_tab, text="Cosine", variable=self.signal_type, value="Cosine").pack(pady=5)

        # input fields for amplitude, frequency, phase, sampling
        self.amplitude = tk.DoubleVar(value=1.0)
        self.phase = tk.DoubleVar(value=0.0)
        self.frequency = tk.DoubleVar(value=1.0)
        self.sampling_rate = tk.DoubleVar(value=50.0)

        ttk.Label(signal_gen_tab, text="Amplitude:").pack(pady=5)
        ttk.Entry(signal_gen_tab, textvariable=self.amplitude).pack(pady=5)

        ttk.Label(signal_gen_tab, text="Phase Shift (theta):").pack(pady=5)
        ttk.Entry(signal_gen_tab, textvariable=self.phase).pack(pady=5)

        ttk.Label(signal_gen_tab, text="Analog Frequency:").pack(pady=5)
        ttk.Entry(signal_gen_tab, textvariable=self.frequency).pack(pady=5)

        ttk.Label(signal_gen_tab, text="Sampling Frequency:").pack(pady=5)
        ttk.Entry(signal_gen_tab, textvariable=self.sampling_rate).pack(pady=5)

        # generate the signal
        generate_button = ttk.Button(signal_gen_tab, text="Generate Signal", command=self.generate_signal)
        generate_button.pack(pady=10)

    def clear_plot(self):
        # Clear the current plot
        self.ax.clear()

    def show_plot(self):
        # Display the updated plot
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def plot_signal(self):
        self.clear_plot()  # Clear any existing plot

        signal_type = self.signal_type_var.get()
        t = np.linspace(0, 1, 100)
        signal = np.sin(2 * np.pi * 5 * t) if signal_type == "Continuous" else np.sin(2 * np.pi * 5 * t)[::5]

        if signal_type == "Discrete":
            self.ax.stem(t[::5], signal, use_line_collection=True)
        else:
            self.ax.plot(t, signal)

        self.ax.set_title(f"{signal_type} Signal")
        self.show_plot()

    def generate_signal(self):
        self.clear_plot()  # Clear any existing plot

        signal_type = self.signal_type.get()
        A = self.amplitude.get()
        theta = self.phase.get()
        f = self.frequency.get()
        fs = self.sampling_rate.get()

        if fs < 2 * f:
            messagebox.showerror("Error", "Sampling frequency must be at least twice the analog frequency.")
            return

        t = np.linspace(0, 1, int(fs))
        if signal_type == "Sine":
            signal = A * np.sin(2 * np.pi * f * t + theta)
        else:
            signal = A * np.cos(2 * np.pi * f * t + theta)

        # Plot the generated signal
        self.ax.plot(t, signal)
        self.ax.set_title(f"{signal_type} Wave (A={A}, f={f}, θ={theta})")

        self.show_plot()

# Run the app
if __name__ == "__main__":
    app = SignalApp()
    app.mainloop()
