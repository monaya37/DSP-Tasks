import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
import math
from task5_files.signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift
np.set_printoptions(precision=10)  # Adjust the precision as needed



class Task5:
    def __init__(self, parent):

        self.parent = parent
        self.large_font = ('Helvetica', 14)
        
        # Create main frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(padx=10, pady=10)

        # Radio buttons for function type
        self.radios_frame = tk.Frame(self.frame)

        self.radio = tk.StringVar(value="DFT")
        tk.Radiobutton(self.radios_frame, text="DFT",       variable=self.radio, value="DFT",   font=self.large_font).grid(row=1, column=0, padx = 1, pady=3, sticky='ew')
        tk.Radiobutton(self.radios_frame, text="IDFT",      variable=self.radio, value="IDFT", font=self.large_font).grid(row=1, column=1, padx = 1, pady=3, sticky='ew')
        self.radios_frame.grid(row=1, pady=4, sticky='ew')

        # Constant input
        self.label_entry_frame = tk.Frame(self.frame)
        self.label = tk.Label(self.label_entry_frame, text="Sampling Frequency:", font=self.large_font)
        self.label.pack(side='left', padx=5)
        self.ConstantInput = tk.Entry(self.label_entry_frame, width=10, font=self.large_font)
        self.ConstantInput.pack(side='left', padx=2)
        self.label_entry_frame.grid(row=2, column=0, pady=4, sticky='ew')

        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=self.large_font)

        # Start button with large font
        generate_button = ttk.Button(self.frame, text="Start", command=self.run_algorithm, style='Large.TButton')
        generate_button.grid(row=3, column=0, columnspan=3, pady=10)


        # Plotting area (centered)
        self.fig, self.axs = plt.subplots(2, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=4, column=0, columnspan=3, pady=10, sticky='nsew')

        self.title = None #for visualization

        # Data storage
        self.indices = []
        self.values = []
        self.amplitude = []
        self.phase = []
        self.freq = []
        
        # Reference data (to be loaded from the txt comparison file)
        self.reference_amplitude = []
        self.reference_phase = []
        


    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

    def run_algorithm(self):
        transformation_type = self.radio.get()

        if(transformation_type == "DFT"):
            print("DFT")
            input_signal = self.read_signals('task5_files\DFT\input_Signal_DFT.txt')
            output_signal =  self.read_signals('task5_files\DFT\output_DFT.txt')           
            self.dft(input_signal, output_signal)
        else:
            print("IDFT")

            input_signal = self.read_signals('task5_files\IDFT\input_IDFT.txt')
            output_signal = ReadSignalFile('task5_files\IDFT\Output_Signal_IDFT.txt')
            self.idft(input_signal, output_signal)

    def read_signals(self,file_path):
        amplitudes = []
        phases = []
        with open(file_path, "r") as file:
            for line in file:
                number_of_samples = int(line.strip())
                if number_of_samples == 0:
                    continue

                for _ in range(number_of_samples):
                    line = file.readline()
                    # read every single line, converts the values from string to float
                    amplitude, phase = line.strip().split()
                    amplitude = float(amplitude.replace('f', ''))
                    phase = float(phase.replace('f', ''))
                    amplitudes.append(amplitude)
                    phases.append(phase)
        return amplitudes, phases

    def idft(self, input_signal, output_signal):

        amplitudes = np.array(input_signal[0])
        shifts = np.array(input_signal[1])

        self.reference_amplitude = output_signal[1]
        N = (len(shifts))

        samples = {}
        counter = 0

        #X = amplitudes * np.exp(1j * shifts)
        for n in range(N):
            counter = 0
            for k in range(N):
                xk = amplitudes[k] * np.exp(1j * shifts[k])
                counter = counter + (xk * np.exp(1j* 2 * np.pi * k * n/N))

            samples[n] = round(np.real((counter)/N))

        
        self.amplitude = list(samples.values())
        amplitude_match = SignalComapreAmplitude(self.amplitude, self.reference_amplitude)
                
        print("Amplitude Comparison:", "Match" if amplitude_match else "Mismatch")
        print("idft done")
        self.plot_signals(output_signal)
        return
    
    def dft(self, input_signal, output_signal):

        values = np.array(input_signal[1])
        self.reference_amplitude = output_signal[0]
        self.reference_amplitude = np.round(self.reference_amplitude, 12)

        self.reference_phase = output_signal[1]
        N = (len(values))

        samples = np.zeros(N, dtype=complex)
        counter = 0

        # Get the sampling frequency from the user input
        sampling_frequency = float(self.ConstantInput.get())
        if sampling_frequency <= 0:
            raise ValueError("Sampling frequency must be a positive number.")
        for n in range(N):
            counter = 0
            for k in range(N):
                xk = values[k]
                counter += xk * np.exp(-2j * np.pi * k * n / N) 
            samples[n] = counter 

        self.amplitude = np.round(np.abs(samples), 12)  # Round to 12 decimal places
        self.phase = np.angle(samples)  

        # Normalize phases to [-π, π]
        self.phase = (self.phase + np.pi) % (2 * np.pi) - np.pi

        # Compute frequency bins
        self.freq = np.fft.fftfreq(N, d=1/sampling_frequency)


        amplitude_match = SignalComapreAmplitude(self.amplitude, self.reference_amplitude)
        phase_match = SignalComaprePhaseShift(self.phase, self.reference_phase)
                
        print("Amplitude Comparison:", "Match" if amplitude_match else "Mismatch")
        print("Phase Comparison:", "Match" if phase_match else "Mismatch")
                
        self.plot_results()


            
    def plot_results(self):

        self.axs[0].clear()
        self.axs[1].clear()

        # Amplitude Spectrum Plot
        self.axs[0].stem(self.freq, self.amplitude, basefmt=" ", label='Computed Amplitude')
        self.axs[0].stem(self.freq[:len(self.reference_amplitude)], self.reference_amplitude, basefmt=" ", linefmt='r--', markerfmt='ro', label='Reference Amplitude')
        self.axs[0].set_title('Amplitude Spectrum')
        self.axs[0].set_xlabel('Frequency (Hz)')
        self.axs[0].set_ylabel('Amplitude')
        self.axs[0].legend()
        self.axs[0].grid(True)

        # Phase Spectrum Plot
        self.axs[1].stem(self.freq, self.phase, basefmt=" ", label='Computed Phase')
        self.axs[1].stem(self.freq[:len(self.reference_phase)], self.reference_phase, basefmt=" ", linefmt='r--', markerfmt='ro', label='Reference Phase')
        self.axs[1].set_title('Phase Spectrum')
        self.axs[1].set_xlabel('Frequency (Hz)')
        self.axs[1].set_ylabel('Phase (radians)')
        self.axs[1].legend()
        self.axs[1].grid(True)

        #self.fig.tight_layout()
        self.canvas.draw()  # Render the plot on the canvas




    def plot_signals(self, outuput_signal):
        self.axs[0].clear()

        indices = list(outuput_signal[0])
        values = list(outuput_signal[1])

        
        self.axs[0].stem(indices, values)
        self.axs[0].set_title(f"Signal after IDFT Visualization")

        self.axs[0].set_xlabel("Index")
        self.axs[0].set_ylabel("Value")
        self.axs[0].legend()

        self.axs[0].grid(True)

        self.canvas.draw()
 
        return
    


