import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

# Function to compute the ideal impulse response
def ideal_impulse_response(filter_type, fc, N, fs):
    h = np.zeros(N)
    M = (N - 1) // 2  # Ensure symmetry

    for n in range(N):
        if n == M:
            if filter_type == 'low':
                h[n] = 2 * fc / fs
            elif filter_type == 'high':
                h[n] = 1 - 2 * fc / fs
            elif filter_type == 'bandpass':
                h[n] = 2 * (fc[1] - fc[0]) / fs
            elif filter_type == 'bandstop':
                h[n] = 1 - 2 * (fc[1] - fc[0]) / fs
        else:
            if filter_type == 'low':
                h[n] = np.sin(2 * np.pi * fc * (n - M) / fs) / (np.pi * (n - M))
            elif filter_type == 'high':
                h[n] = -np.sin(2 * np.pi * fc * (n - M) / fs) / (np.pi * (n - M))
            elif filter_type == 'bandpass':
                h[n] = (np.sin(2 * np.pi * fc[1] * (n - M) / fs) - np.sin(2 * np.pi * fc[0] * (n - M) / fs)) / (np.pi * (n - M))
            elif filter_type == 'bandstop':
                h[n] = (np.sin(2 * np.pi * fc[0] * (n - M) / fs) - np.sin(2 * np.pi * fc[1] * (n - M) / fs)) / (np.pi * (n - M))

    return h

# Function to choose window type based on stop-band attenuation
def choose_window(stop_atten):
    if stop_atten <= 21:
        return 'rectangular', 0.9
    elif stop_atten <= 44:
        return 'hanning', 3.1
    elif stop_atten <= 53:
        return 'hamming', 3.3
    else:
        return 'blackman', 5.5

# Function to compute the window
def compute_window(N, window_type):
    if window_type == 'hamming':
        return 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(N) / (N - 1))
    elif window_type == 'hanning':
        return 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N) / (N - 1))
    elif window_type == 'blackman':
        return (0.42 - 0.5 * np.cos(2 * np.pi * np.arange(N) / (N - 1)) +
                0.08 * np.cos(4 * np.pi * np.arange(N) / (N - 1)))
    else:
        return np.ones(N)  # Rectangular window

# Function to design the FIR filter
def design_fir_filter(filter_type, fs, fc, stop_atten, transition_band):
    delta_f = transition_band / fs  # Normalized transition band

    # Choose appropriate window type based on stop-band attenuation
    window_type, window_constant = choose_window(stop_atten)

    # Calculate N dynamically based on the transition width
    N = int(np.ceil(window_constant / delta_f))
    if N % 2 == 0:
        N += 1  # Ensure N is odd

    # Adjust cut-off frequencies
    if filter_type in ['low', 'high']:
        fc_adjusted = fc
    else:
        fc_adjusted = [fc[0], fc[1]]

    # Compute impulse response and window
    hd = ideal_impulse_response(filter_type, fc_adjusted, N, fs)
    w = compute_window(N, window_type)

    # Compute filter coefficients
    h = hd * w

    return h, window_type, N

# GUI Window
class FilterDesignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FIR Filter Designer")

        # Input Fields
        ttk.Label(root, text="Filter Type (low, high, bandpass, bandstop):").grid(row=0, column=0, sticky='w')
        self.filter_type = ttk.Entry(root)
        self.filter_type.grid(row=0, column=1)

        ttk.Label(root, text="Sampling Frequency (Hz):").grid(row=1, column=0, sticky='w')
        self.fs = ttk.Entry(root)
        self.fs.grid(row=1, column=1)

        ttk.Label(root, text="Stop Band Attenuation (dB):").grid(row=2, column=0, sticky='w')
        self.stop_atten = ttk.Entry(root)
        self.stop_atten.grid(row=2, column=1)

        ttk.Label(root, text="Transition Band (Hz):").grid(row=3, column=0, sticky='w')
        self.transition_band = ttk.Entry(root)
        self.transition_band.grid(row=3, column=1)

        ttk.Label(root, text="Cut-off Frequency (Hz) or Range [f1, f2] (comma-separated):").grid(row=4, column=0, sticky='w')
        self.fc = ttk.Entry(root)
        self.fc.grid(row=4, column=1)

        # Buttons
        ttk.Button(root, text="Design Filter", command=self.design_filter).grid(row=5, column=0, pady=10)
        ttk.Button(root, text="Exit", command=root.destroy).grid(row=5, column=1, pady=10)

    def design_filter(self):
        try:
            filter_type = self.filter_type.get().lower()
            fs = float(self.fs.get())
            stop_atten = float(self.stop_atten.get())
            transition_band = float(self.transition_band.get())

            # Parse cut-off frequency
            fc_input = self.fc.get()
            if ',' in fc_input:
                fc = [float(f) for f in fc_input.split(',')]
            else:
                fc = float(fc_input)

            # Design filter
            h, window_type, N = design_fir_filter(filter_type, fs, fc, stop_atten, transition_band)

            # Generate indices for coefficients
            indices = np.arange(-len(h)//2, len(h)//2 + 1)

            # Ensure indices match the length of h
            if len(indices) > len(h):
                indices = indices[:-1]  # Trim extra index if lengths differ

            # Display Results
            result_text = f"Window Type: {window_type}\nNumber of Coefficients (N): {len(h)}\n\nFilter Coefficients with Indices:\n"
            result_text += '\n'.join(f"{i} {coef:.10f}" for i, coef in zip(indices, h))
            
            messagebox.showinfo("Filter Coefficients", result_text)

            # Save coefficients to file
            np.savetxt("FIR_Coefficients.txt", np.column_stack((indices, h)), fmt="%d %.10f")

            # Plot Coefficients
            plt.figure(figsize=(8, 4))
            plt.stem(indices, h, use_line_collection=True)
            plt.title("Filter Coefficients")
            plt.xlabel("Index")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))

# # Main Execution
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = FilterDesignerApp(root)
#     root.mainloop()
