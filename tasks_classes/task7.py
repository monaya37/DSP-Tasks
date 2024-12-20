import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tasks_classes.functions import *
from tasks_classes.CompareSignal import *
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

        self.pady = 1

        # Center all rows and columns in the frame
        for i in range(8):  # Adjust number of rows based on content
            self.frame.grid_rowconfigure(i, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        large_font = ('Helvetica', 14)

        self.filter_type = tk.StringVar()  
        self.fs = tk.IntVar()  
        self.stop_atten = tk.IntVar()  
        self.fc = tk.StringVar()  
        self.transition_band = tk.StringVar()  
        self.test_number = tk.StringVar()  # Variable for test number input
        self.selected_option = tk.StringVar(value="Direct")

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
        generate_button = ttk.Button(self.frame, text="Generate Signal", command=self.choose_test, style='Large.TButton')
        generate_button.grid(row=8, column=0, columnspan=2, rowspan=1, pady=10)


        # Create a row for radio buttons and test number box
        option_frame = tk.Frame(self.frame)
        option_frame.grid(row=7, column=0, sticky="w")
        self.padx = 2
        # Radio buttons for "Direct" and "Fast"
        ttk.Label(option_frame, text="Select Option:", font=large_font).grid(row=0, column=0, pady=self.pady, sticky="w")
        # Bullet points
        direct_radio = tk.Radiobutton(option_frame, text="Direct", variable=self.selected_option, value="Direct", font=large_font)
        direct_radio.grid(row=0, column=1, padx = self.padx ,sticky="w")

        fast_radio = tk.Radiobutton(option_frame, text="Fast", variable=self.selected_option, value="Fast", font=large_font)
        fast_radio.grid(row=0, column=2, padx = self.padx, sticky="w")

        # Test number box
        test_frame = tk.Frame(self.frame)
        test_frame.grid(row=7, column=1, sticky="w")
        ttk.Label(test_frame, text="Test Number:", font=large_font).grid(row=7, column=0, pady=self.pady, sticky="w")
        test_number_entry = ttk.Entry(test_frame, textvariable=self.test_number, font=large_font, width=9)
        test_number_entry.grid(row=7, column=1, padx = self.padx, pady=self.pady, sticky="w")

        # Figure and canvas for plotting
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, pady=10)


            # Paths stored dynamically
        self.filter_output_paths = {
            1: 'task7_files\FIR test cases\Testcase 1\LPFCoefficients.txt',
            2: 'task7_files\FIR test cases\Testcase 3\HPFCoefficients.txt',
            3: 'task7_files\FIR test cases\Testcase 5\BPFCoefficients.txt',
            4: 'task7_files\FIR test cases\Testcase 7\BSFCoefficients.txt'
        }
            # Paths stored dynamically
        self.ecg_output_paths = {
            1: 'task7_files\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt',
            2: 'task7_files\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt',
            3: 'task7_files\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt',
            4: 'task7_files\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt'
        }
        self.ecg_input_paths = {
            1: 'task7_files\FIR test cases\Testcase 2\ecg400.txt',
            2: 'task7_files\FIR test cases\Testcase 4\ecg400.txt',
            3: 'task7_files\FIR test cases\Testcase 6\ecg400.txt',
            4: 'task7_files\FIR test cases\Testcase 8\ecg400.txt'
        }
        self.filter_specifications_paths = {
            1: 'task7_files\FIR test cases\Testcase 1\Filter Specifications.txt',
            2: 'task7_files\FIR test cases\Testcase 3\Filter Specifications.txt',
            3: 'task7_files\FIR test cases\Testcase 5\Filter Specifications.txt',
            4: 'task7_files\FIR test cases\Testcase 7\Filter Specifications.txt'
        }

    def display(self):
        self.frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def hide(self):
        self.frame.grid_forget()
        

    def read_filter_specifications(self, filepath):
        filter_params = {}

        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return filter_params
        
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Update the GUI variables based on the key
                    if key == "FilterType":
                        self.filter_type.set(value.lower())  # Set filter type (e.g., 'high')
                        filter_params["FilterType"] = value.lower()
                    elif key == "FS":
                        self.fs.set(int(value))  # Set sampling frequency
                        filter_params["FS"] = int(value)
                    elif key == "StopBandAttenuation":
                        self.stop_atten.set(int(value))  # Set stop band attenuation
                        filter_params["StopBandAttenuation"] = int(value)
                    elif key == "FC":
                        self.fc.set(value)  # Set cut-off frequency (string for flexibility)
                        filter_params["FC"] = int(value)
                    elif key == "F1":
                        filter_params["FC"] = []
                        filter_params["FC"].append(int(value))
                    elif key == "F2":
                        if "FC" in filter_params and isinstance(filter_params["FC"], list):
                            filter_params["FC"].append(int(value))                    
                    elif key == "TransitionBand":
                        self.transition_band.set(value)  # Set transition band
                        filter_params["TransitionBand"] = int(value)
                except ValueError:
                    print(f"Skipping invalid line: {line}")
        return filter_params 



    def choose_test(self):
        option = self.selected_option.get()
        test = int(self.test_number.get())
        filter_params = self.read_filter_specifications(self.filter_specifications_paths[test])


        ecg_indices, ecg_coefficients = ReadSignalFile(self.ecg_input_paths[test])

        filter_indices, filter_coefficients = design_fir_filter(filter_params['FilterType'], filter_params['FS'], filter_params['FC'], filter_params['StopBandAttenuation'], filter_params['TransitionBand'])

        indices, coefficients = apply_convolution(ecg_indices, ecg_coefficients, filter_indices, filter_coefficients, option)

        Compare_Signals(self.filter_output_paths[test], filter_indices, filter_coefficients)
        Compare_Signals(self.ecg_output_paths[test], indices, coefficients)

        np.savetxt("FIR_Coefficients.txt", np.column_stack((indices, coefficients)), fmt="%d %.10f")
        self.plot_filter(coefficients)

        
    def plot_filter(self, coefficients):
        self.ax.clear()

        coefficients = np.array(coefficients)
        indices = np.arange(-len(coefficients)//2 +1, len(coefficients)//2 +1)

        self.ax.plot(indices, coefficients, marker='o', linestyle='-', color='b')
        self.ax.set_title("Filter Coefficients")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Coefficient Value")
        self.ax.grid(True)
        self.canvas.draw()
        

def calculate_N(transition_band, window_constant, fs):
    delta_f = transition_band / fs  # Normalized transition band
    N = int(np.ceil(window_constant / delta_f))
    if N % 2 == 0:
        N += 1  # Ensure N is odd
    return N

def design_fir_filter(filter_type, fs, fc, stop_atten, transition_band):
    
    if filter_type in ['low pass', 'high pass']:
        fc_adjusted = fc
    else:
        fc_adjusted = [fc[0], fc[1]]

    window_type, window_constant = choose_window(stop_atten)
    N = calculate_N(transition_band, window_constant, fs)

    hd = ideal_impulse_response(filter_type, fc_adjusted, N, fs, transition_band)
    w = compute_window(N, window_type)
    h = np.array(hd) * np.array(w)

    indices = np.arange(-len(h)//2 +1, len(h)//2 +1)

    return indices, h


# Function to compute the ideal impulse response
def ideal_impulse_response(filter_type, fc, N, fs, transition_band):
    h = np.zeros(N)
    M = (N-1) // 2 # Ensure symmetry

    if filter_type in ['low pass', 'high pass']:
        fc_low = fc + transition_band/2
        fc_high = fc - transition_band/2
    elif filter_type == 'band pass':
        fc_low = fc[0] - transition_band/2
        fc_high = fc[1] + transition_band/2
    else:
        fc_low = fc[0] + transition_band/2
        fc_high = fc[1] - transition_band/2


    for n in range(N):
        if n == M:
            if filter_type == 'low pass':
                h[n] = (2 * fc_low / fs)
            elif filter_type == 'high pass':
                h[n] = 1 - 2 * fc_high / fs
            elif filter_type == 'band pass':
                h[n] = (2 * fc_high/fs) - (2 * fc_low/fs) 
            elif filter_type == 'band stop':
                old = (2 * (fc[1] + transition_band/2)/fs) - (2 * (fc[0] - transition_band/2)/fs)
                h[n] = 2 - (2 * (fc[1] - transition_band/2)/fs) - (2 * (fc[0] + transition_band/2)/fs) -old

        else:
            if filter_type == 'low pass':
                h[n] = np.sin(2 * np.pi * fc_low * (n - M) / fs) / (np.pi * (n - M))
            elif filter_type == 'high pass':
                h[n] = -np.sin(2 * np.pi * fc_high * (n - M) / fs) / (np.pi * (n - M))
            elif filter_type == 'band pass':               
                h_high = 2 * fc_high/fs * np.sin(2 * np.pi * fc_high * (n - M) / fs) / (2 * np.pi * (n - M) * fc_high / fs)
                h_low = 2 * fc_low/fs * np.sin(2* np.pi * fc_low * (n - M) / fs) / (2* np.pi * (n - M) * fc_low / fs)
                h[n] = h_high - h_low
            elif filter_type == 'band stop':
                h_high = 2 * fc_high/fs * np.sin(2 * np.pi * fc_high * (n - M) / fs) / (2 * np.pi * (n - M) * fc_high / fs)
                h_low = 2 * fc_low/fs * np.sin(2* np.pi * fc_low * (n - M) / fs) / (2* np.pi * (n - M) * fc_low / fs)
                h[n] =  h_low- h_high
    return h 

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

    if window_type == 'hamming':
        index = 0
        for n in range(-N//2, N//2): 
            window[index] = 0.54 + 0.46 * np.cos(2 * np.pi * n / N)
            index+=1
            
    elif window_type == 'hanning':
        index = 0
        for n in range(-N//2, N//2):  
            index = 0
            window[index] = 0.5 + 0.5 * np.cos(2 * np.pi * n / N)
            index+=1

    elif window_type == 'blackman':
        index = 0
        N = N - 1
        for n in range(-N//2, N//2):  
            window[index] = round(0.42 + (0.5 * np.cos(2 * np.pi * n/N)) + (0.08* np.cos(4 * np.pi * n /N)),6)
            index+=1
            
    else:
        window = np.ones(N) 

    return window
    


def apply_convolution(ecg_indices, ecg_vals, filter_indices, filter_coefficients, option):

    indices = np.arange(ecg_indices[0] + filter_indices[0], ecg_indices[-1] + filter_indices[-1] + 1)

    if(option == 'Direct'):
        y = direct_convolution(ecg_vals, filter_coefficients)
    else:
        y = fast_convolution( ecg_vals, filter_coefficients) #fft
        
    return indices, y

def direct_convolution(x, h):
    N = len(x)
    M = len(h)
    y = np.zeros(N + M - 1)
    
    # Perform the convolution
    for n in range(len(y)):
        for m in range(M):
            if 0 <= n - m < N:
                y[n] += h[m] * x[n - m]
    return y

def fast_convolution(x, h):
    N = len(x)
    M = len(h)
    N_pad = N + M - 1

    x_padded = np.pad(x, (0, N_pad - N), mode='constant')
    h_padded = np.pad(h, (0, N_pad - M), mode='constant')
    
    X = dft(x_padded)  
    H = dft(h_padded)  
    
    Y_freq = X * H
    
    y_padded = idft(Y_freq)  

    return np.real(y_padded[:N + M - 1])




def dft(x):
    N = len(x)
    X = np.zeros(N, dtype=complex)  
    
    for k in range(N):
        for n in range(N):
            X[k] += x[n] * np.exp(-2j * np.pi * k * n / N)
    
    return X


def idft(X):
    N = len(X)
    x = np.zeros(N, dtype=complex)  
    
    for n in range(N):
        for k in range(N):
            x[n] += X[k] * np.exp(2j * np.pi * k * n / N)
    
    return x / N 


