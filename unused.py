def mulitply_signals(a, b):
    c = []
    for n in range(len(a)):
        c.append(np.real(a[n] * b[n]))
    return c
####################################################################
def dft(self, values):

    N = len(values)
    samples = np.zeros(N, dtype=complex)

    for n in range(N):
        counter = 0
        for k in range(N):
            xk = values[k]
            counter += xk * np.exp(-2j * np.pi * k * n / N) 

        samples[n] = counter
    return samples
####################################################################

def correlation_fast(self, signal1, signal2, output_file):

    _, values1 = signal1
    _, values2 = signal2
    N = len(values1)

    signal1 = self.dft(values1)
    signal2 = self.dft(values2)
    FD = self.mulitply_signals(signal1, np.conj(signal2))

    
    samples = {}
    for n in range(N):
        counter = 0
        for k in range(N):
            xk = FD[k]
            counter += (xk * np.exp(1j* 2 * np.pi * k * n/N))
        samples[n] = np.real(counter)/N/N
    

    samples = calculate_normalization(values1, values2, samples)
    indices = list(samples.keys())
    values = list(samples.values())
    Compare_Signals(output_file,indices, values)   
    #self.plot_signals(indices, values)
    return
####################################################################

 # # Figure and canvas for plotting
self.fig, self.ax = plt.subplots()
self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)



#######################################################################


        # Compute the frequency response using FFT
        N = len(coefficients)
        frequency_response = np.fft.fft(coefficients, N)

        # Frequency axis (assume fs = 1 Hz for simplicity)
        freq = np.fft.fftfreq(N, d=1)  # Frequency axis in Hz

        # Compute the magnitude of the frequency response
        magnitude = np.abs(frequency_response)


        # Plot the magnitude response
        self.ax.plot(freq[:N // 2], magnitude[:N // 2], label="Frequency Response")
        # Highlight the passband and stopband with adjusted transparency
        if filter_type == 'low':
            self.ax.axvspan(0, fc_low, color='green', alpha=0.1, label='Passband')  # More transparent
            self.ax.axvspan(fc_low, 0.5, color='red', alpha=0.5, label='Stopband')  # Less transparent
        elif filter_type == 'high':
            self.ax.axvspan(0, fc_high, color='red', alpha=0.5, label='Stopband')  # Less transparent
            self.ax.axvspan(fc_high, 0.5, color='green', alpha=0.1, label='Passband')  # More transparent
        elif filter_type == 'bandpass':
            self.ax.axvspan(0, fc_low, color='red', alpha=0.5, label='Stopband')  # Less transparent
            self.ax.axvspan(fc_low, fc_high, color='green', alpha=0.3, label='Passband')  # Medium transparency
            self.ax.axvspan(fc_high, 0.5, color='red', alpha=0.5, label='Stopband')  # Less transparent
        elif filter_type == 'bandstop':
            self.ax.axvspan(0, fc_low, color='green', alpha=0.3, label='Passband')  # Medium transparency
            self.ax.axvspan(fc_low, fc_high, color='red', alpha=0.7, label='Stopband')  # Less transparent
            self.ax.axvspan(fc_high, 0.5, color='green', alpha=0.3, label='Passband')  # Medium transparency


        self.ax.set_title("Frequency Response of the Filter")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude")
        self.ax.grid(True)
        self.canvas.draw()




#####################################################33

import numpy as np
import matplotlib.pyplot as plt

# Generate a sample signal and filter
signal = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
filter_kernel = np.array([0.1, 0.2, 0.3, 0.2, 0.1])

# Method 1: Time-Domain Convolution using np.convolve
conv_time_domain = np.convolve(signal, filter_kernel, mode='full')

# Method 2: Frequency-Domain Convolution using FFT
# Zero-padding to the size of the next power of 2 greater than the sum of the lengths of the signal and the filter
n = len(signal) + len(filter_kernel) - 1
signal_padded = np.pad(signal, (0, n - len(signal)))
filter_kernel_padded = np.pad(filter_kernel, (0, n - len(filter_kernel)))

# Convert both signal and filter to frequency domain
signal_fft = np.fft.fft(signal_padded)
filter_fft = np.fft.fft(filter_kernel_padded)

# Multiply in frequency domain
product_fft = signal_fft * filter_fft

# Convert back to time domain using inverse FFT
conv_freq_domain = np.fft.ifft(product_fft)

# Ensure the result is real-valued (since convolution should produce real values)
conv_freq_domain = np.real(conv_freq_domain)

# Plotting the results
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title('Time-Domain Convolution')
plt.plot(conv_time_domain)
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.subplot(1, 2, 2)
plt.title('Frequency-Domain Convolution')
plt.plot(conv_freq_domain)
plt.xlabel('Samples')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()








def convolve(ecg_indices, ecg_vals, h_indices, h_vals):

    y = {}
    #signal --> ecg
    #signal2 --> h
    if(ecg_indices[0] <= h_indices[0]):
        print('in here')
        h = ecg_indices, ecg_vals
        x = h_indices, h_vals
        start = ecg_indices[0]
        end = h_indices[-1] + ecg_indices[-1]
    else:
        x = ecg_indices, ecg_vals
        h = h_indices, h_vals
        start = h_indices[0]
        end =  h_indices[-1] + ecg_indices[-1]
    

    for n in range(start, end+1):
        y[n] = 0
        for k in x[0]:
            if((n - k) in h[0]):
                y[n] += x[1][k] * h[1][n-k]

    indices = list(y.keys())
    values = list(y.values())

    return indices, values


def dft(values):

    N = len(values)
    samples = np.zeros(N, dtype=complex)

    for n in range(N):
        counter = 0
        for k in range(N):
            xk = values[k]
            counter += xk * np.exp(-2j * np.pi * k * n / N) 

        samples[n] = counter

    amplitude = np.round(np.abs(samples), 12)  # Round to 12 decimal places
    phase = np.angle(samples)  

        # Normalize phases to [-π, π]
    phase = (phase + np.pi) % (2 * np.pi) - np.pi
    return samples


def idft(input_signal):

    amplitudes = np.array(input_signal[0])
    shifts = np.array(input_signal[1])

    N = (len(shifts))

    samples = {}
    counter = 0
    # x = A * e^ theta *j 
    X = amplitudes * np.exp(1j * shifts)
    for n in range(N):
        counter = 0
        for k in range(N):
            xk = X[k]
            counter = counter + (xk * np.exp(1j* 2 * np.pi * k * n/N))

        samples[n] = round(np.real((counter)/N))

    
    amplitude = list(samples.values())
    return amplitude
