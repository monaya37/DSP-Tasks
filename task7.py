import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *
from CompareSignal import *
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

        self.pady = 3

        # Center all rows and columns in the frame
        for i in range(8):  # Adjust number of rows based on content
            self.frame.grid_rowconfigure(i, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        large_font = ('Helvetica', 14)


        self.filter_type = tk.StringVar(value='bandstop')  
        self.fs = tk.IntVar(value=1000)  
        self.stop_atten = tk.IntVar(value=60)  
        self.fc = tk.StringVar(value='150, 250')  
        self.transition_band = tk.StringVar(value=50)  


        ttk.Label(self.frame, text="Filter Type (low, high, bandpass, bandstop):", font=large_font).grid(row=2, column=0, pady=self.pady, sticky="w")
        ttk.Entry(self.frame, textvariable=self.filter_type, font=large_font).grid(row=2, column=1, pady=self.pady)

        ttk.Label(self.frame, text="Sampling Frequency (Hz):", font=large_font).grid(row=3, column=0, pady=self.pady, sticky="w")
        ttk.Entry(self.frame, textvariable=self.fs, font=large_font).grid(row=3, column=1, pady=self.pady)

        ttk.Label(self.frame, text="Stop Band Attenuation (dB):", font=large_font).grid(row=4, column=0, pady=self.pady, sticky="w")
        ttk.Entry(self.frame, textvariable=self.stop_atten, font=large_font).grid(row=4, column=1, pady=self.pady)

        ttk.Label(self.frame, text="Cut-off Frequency (Hz) or Range [f1, f2] (comma-separated):", font=large_font).grid(row=5, column=0, pady=self.pady, sticky="w")
        ttk.Entry(self.frame, textvariable=self.fc, font=large_font).grid(row=5, column=1, pady=self.pady)

        ttk.Label(self.frame, text="Transition Band (Hz):", font=large_font).grid(row=6, column=0, pady=self.pady, sticky="w")
        ttk.Entry(self.frame, textvariable=self.transition_band, font=large_font).grid(row=6, column=1, pady=self.pady)

        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=large_font)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command=self.design_filter, style='Large.TButton')
        generate_button.grid(row=7, column=0, columnspan=2, rowspan= 1, pady=10)

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=2, pady=10)

        self.path1= 'task7_files\FIR test cases\Testcase 1\LPFCoefficients.txt'
        self.path3 = 'task7_files\FIR test cases\Testcase 3\HPFCoefficients.txt'
        self.path5 = 'task7_files\FIR test cases\Testcase 5\BPFCoefficients.txt'
        self.path7 = 'task7_files\FIR test cases\Testcase 7\BSFCoefficients.txt'

        self.path8 = 'task7_files\FIR test cases\Testcase 8\ecg400.txt'

    def print_filter_parameters(self):
        filter_type = self.filter_type.get().lower() 
        print(f"Filter Type: {filter_type}")
        
        fs = float(self.fs.get())  
        print(f"Sampling Frequency (fs): {fs}")
        
        stop_atten = float(self.stop_atten.get())  
        print(f"Stop Band Attenuation: {stop_atten} dB")
        
        transition_band = float(self.transition_band.get())  
        print(f"Transition Band: {transition_band} Hz")
        
        fc_input = self.fc.get()
        if ',' in fc_input:
            fc = [float(f) for f in fc_input.split(',')]
            print(f"Cut-off Frequencies: {fc}")
        else:
            fc = float(fc_input)
            print(f"Cut-off Frequency: {fc} Hz")



    def design_filter(self):

        filter_type = self.filter_type.get().lower() # low , high, pass, reject
        fs = float(self.fs.get()) #sampling frequency
        stop_atten = float(self.stop_atten.get()) #stop band attention
        transition_band = float(self.transition_band.get())

        fc_input = self.fc.get()
        if ',' in fc_input:
            fc = [float(f) for f in fc_input.split(',')]
        else:
            fc = float(fc_input)
              
        self.print_filter_parameters()


        window_type, window_constant = choose_window(stop_atten)
        N = calculate_N(transition_band, window_constant, fs)
        indices, coefficients = design_fir_filter(filter_type, fs, fc, window_type, N, transition_band) #filter

        #x, vals = ReadSignalFile('task7_files\FIR test cases\Testcase 8\ecg400.txt')

        #indices, coefficients = ecg(len(vals), filter_type, fc[0], fc[1], fs, transition_band, stop_atten, vals)

        #والقائمة تطول
        # Save coefficients to file
        np.savetxt("FIR_Coefficients.txt", np.column_stack((indices, coefficients)), fmt="%d %.10f")
        Compare_Signals(self.path7, indices, coefficients)


        self.plot_filter(coefficients)



    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()

        
    def plot_filter(self, coefficients):
        self.ax.clear()

        coefficients = np.array(coefficients)
        # Generate the x-axis index
        indices = np.arange(-len(coefficients)//2 +1, len(coefficients)//2 +1)

        # Plot the coefficients
        self.ax.plot(indices, coefficients, marker='o', linestyle='-', color='b')

        # Add titles and labels
        self.ax.set_title("Filter Coefficients")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Coefficient Value")

        # Display the plot
        self.ax.grid(True)
        self.canvas.draw()

def calculate_N(transition_band, window_constant, fs):
    delta_f = transition_band / fs  # Normalized transition band
    N = int(np.ceil(window_constant / delta_f))
    if N % 2 == 0:
        N += 1  # Ensure N is odd
    return N

def design_fir_filter(filter_type, fs, fc,window_type, N, transition_band):
    
    if filter_type in ['low', 'high']:
        fc_adjusted = fc
    else:
        fc_adjusted = [fc[0], fc[1]]

    hd, middleindex = ideal_impulse_response(filter_type, fc_adjusted, N, fs, transition_band)
    w = compute_window(N, window_type)
    h = np.array(hd) * np.array(w)
    print("h[M]: ", h[middleindex])
    print("w[M]: ", w[middleindex])
    indices = np.arange(-len(h)//2 +1, len(h)//2 +1)

    return indices, h


# Function to compute the ideal impulse response
def ideal_impulse_response(filter_type, fc, N, fs, transition_band):
    h = np.zeros(N)
    M = (N-1) // 2 # Ensure symmetry

    if filter_type in ['low', 'high']:
        fc_low = fc + transition_band/2
        fc_high = fc - transition_band/2
    elif filter_type == 'bandpass':
        fc_low = fc[0] - transition_band/2
        fc_high = fc[1] + transition_band/2
    else:
        fc_low = fc[0] + transition_band/2
        fc_high = fc[1] - transition_band/2


    for n in range(N):
        if n == M:
            if filter_type == 'low':
                h[n] = 2 * fc_low / fs
            elif filter_type == 'high':
                h[n] = 1 - 2 * fc_high / fs
            elif filter_type == 'bandpass':
                h[n] = (2 * fc_low/fs) - (2 * fc_high/fs)
            elif filter_type == 'bandstop':
                old = (2 * (fc[1] + transition_band/2)/fs) - (2 * (fc[0] - transition_band/2)/fs)
                h[n] = 2 - (2 * (fc[1] - transition_band/2)/fs) - (2 * (fc[0] + transition_band/2)/fs) -old
                #h[n] = 2 - 4*(fc[1] -fc[0])/fs

        else:
            if filter_type == 'low':
                h[n] = np.sin(2 * np.pi * fc_low * (n - M) / fs) / (np.pi * (n - M))
            elif filter_type == 'high':
                h[n] = -np.sin(2 * np.pi * fc_high * (n - M) / fs) / (np.pi * (n - M))
            elif filter_type == 'bandpass':               
                h_high = 2 * fc_high/fs * np.sin(2 * np.pi * fc_high * (n - M) / fs) / (2 * np.pi * (n - M) * fc_high / fs)
                h_low = 2 * fc_low/fs * np.sin(2* np.pi * fc_low * (n - M) / fs) / (2* np.pi * (n - M) * fc_low / fs)
                h[n] = h_high - h_low
            elif filter_type == 'bandstop':
                h_high = 2 * fc_high/fs * np.sin(2 * np.pi * fc_high * (n - M) / fs) / (2 * np.pi * (n - M) * fc_high / fs)
                h_low = 2 * fc_low/fs * np.sin(2* np.pi * fc_low * (n - M) / fs) / (2* np.pi * (n - M) * fc_low / fs)
                h[n] =  h_low- h_high
    return h ,M

def choose_window(stop_atten):
    if stop_atten <= 21:
        return 'rectangular', 0.9
    elif stop_atten <= 44:
        return 'hanning', 3.1
    elif stop_atten <= 53:
        return 'hamming', 3.3
    else:
        return 'blackman', 5.5

def compute_window(N, window_type):
 
    window = np.zeros(N)
    print('window type is: ', window_type)

    # Handle the window type
    if window_type == 'hamming':
        index = 0
        for n in range(-N//2, N//2):  # Loop from -N/2 to N/2
            window[index] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
            index+=1
            
    elif window_type == 'hanning':
        index = 0
        for n in range(-N//2, N//2):  # Loop from -N/2 to N/2
            index = 0
            window[index] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
            index+=1

    elif window_type == 'blackman':
        index = 0
        N = N - 1
        for n in range(-N//2, N//2):  # Loop from -N/2 to N/2
            window[index] = round(0.42 + (0.5 * np.cos(2 * np.pi * n/N)) + (0.08* np.cos(4 * np.pi * n /N)),2)
            index+=1
            
    else:
        window = np.ones(N)  # Rectangular window

    return window
    

def ecg(N, filter_type, fc_low, fc_high, fs, transition_band, stop_atten, ecg_signal):
    M = N-1 // 2

    if(filter_type == 'bandstop'):
        # Ideal low-pass and high-pass filters
        hd_low = np.sinc(2 * fc_low * (N) / fs)
        hd_high = np.sinc(2 * fc_high * (N) / fs)
        hd = hd_low - hd_high

    window_type, window_constant = choose_window(stop_atten)
    w = compute_window(N, window_type)
    #N = calculate_N(transition_band, window_constant, fs)

    h = hd * w
    y = np.convolve(ecg_signal, h, mode='same')  # Convolution with 'same' mode to maintain signal length
    indices = np.arange(-len(y)//2 +1, len(y)//2 +1)

    return indices , y