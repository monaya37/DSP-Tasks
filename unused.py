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
