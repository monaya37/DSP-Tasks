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
