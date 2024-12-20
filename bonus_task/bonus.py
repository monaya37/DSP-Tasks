import numpy as np
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class bonus:
    def __init__(self, root):

        self.root = root

        # Create GUI Components
        self.frame = tk.Frame(root)
        self.frame.grid(row=1, column=0, sticky="nsew")

        self.pady = 1

        large_font = ('Helvetica', 14)


        # Define the button style
        style = ttk.Style()
        style.configure('Large.TButton', font=large_font)

        # Generate the signal
        generate_button = ttk.Button(self.frame, text="Generate Signal", command=self.run, style='Large.TButton')
        generate_button.grid(row=8, column=0, columnspan=2, rowspan=1, pady=10)


        # Figure and canvas for plotting
        self.fig, self.axs = plt.subplots(2, 2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, pady=10)

        self.autoX = None
        self.autoY = None
        self.noiseX = None
        self.noiseY = None
        self.finalX = None
        self.finalY = None

    def plot(self, samples):
        self.ax.clear()

        indices = list(samples.keys())
        values = list(samples.values())

        self.ax.plot(indices, values, marker='o', linestyle='-', color='b')
        self.ax.set_title("Filter Coefficients")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Coefficient Value")
        self.ax.grid(True)
        self.canvas.draw()
    

    def plot_results(self):

        # Amplitude Spectrum Plot
        self.axs[0].plot(self.autoX, self.autoY, basefmt=" ", label='Computed Amplitude')
        self.axs[0].set_title('Amplitude Spectrum')
        self.axs[0].set_xlabel('Frequency (Hz)')
        self.axs[0].set_ylabel('Amplitude')
        self.axs[0].legend()
        self.axs[0].grid(True)

        # Phase Spectrum Plot
        self.axs[1].plot(self.noiseX, self.noiseY, basefmt=" ", label='Computed Phase')
        self.axs[1].set_title('Phase Spectrum')
        self.axs[1].set_xlabel('Frequency (Hz)')
        self.axs[1].set_ylabel('Phase (radians)')
        self.axs[1].legend()
        self.axs[1].grid(True)

        # Phase Spectrum Plot
        self.axs[2].plot(self.finalX, self.finalY, basefmt=" ", label='Computed Phase')
        self.axs[2].set_title('Phase Spectrum')
        self.axs[2].set_xlabel('Frequency (Hz)')
        self.axs[2].set_ylabel('Phase (radians)')
        self.axs[2].legend()
        self.axs[2].grid(True)

        #self.fig.tight_layout()
        self.canvas.draw()  # Render the plot on the canvas


    def correlation(self, signal1, signal2):

        values1 = signal1
        values2 = signal2
        N = len(values1)

        samples = {}
        for n in range(N):
            counter = 0
            for k in range(N):
                counter += values1[k]* values2[k]
            values2 = self.shift_left(values2)
            samples[n] = counter / N

        samples = self.calculate_normalization(values1, values2, samples)
        indices = list(samples.keys())
        values = list(samples.values())
        
        return samples, indices, values


    def shift_left(self, list):
        return np.roll(list, -1)


        
    def calculate_normalization(self, a, b, rj):
            N = len(rj)
            p = {}
            
            squares1 = sum([x**2 for x in a])
            squares2 = sum([x**2 for x in b])
            normalization_factor = (1/N) * (math.sqrt(abs(squares1 * squares2)))

            for k in range(N):
                p[k] = rj[k]/ normalization_factor
            return p


    def add_signals(self, signal_a, signal_b):
        combined = {}

        index = 0
        for value in signal_a:
            combined[index] = value
            index =+1

        index = 0
        for value in signal_b:
            combined[index] += value  # Sum the values for overlapping keys
            index =+1

        combined = dict(sorted(combined.items()))
        indices = list(combined.keys())
        values = list(combined.values())
        return indices, values, combined
    
    def run(self):
    
        sampling_rate = 100
        t = np.linspace(0, 1, int(sampling_rate))
        amplitude = 1
        frequency = 1
        signal = amplitude * np.sin(2 * np.pi * frequency * t)

        sine_corr, _, _ = self.correlation(signal ,signal)
        self.autoX = np.array(list(sine_corr.keys()))
        self.autoY = list(sine_corr.values())
        self.plot_results()

        indices, values, noise = self.ReadSignals('noise.txt')
        print('noise', noise)
        self.noiseX = list(sine_corr.keys())
        self.noiseY = list(sine_corr.values())
        self.plot_results()



        _,_,new_signal = self.add_signals(sine_corr, noise)
        print('new_signal', new_signal)
        self.autoX = list(new_signal.keys())
        self.autoY = list(new_signal.values())
        self.plot_results()
        self.plot(new_signal)

        _, _ , final_corr = self.correlation(new_signal, sine_corr)
        print('sine_corr+ noise', sine_corr)
        self.finalX = list(final_corr.keys())
        self.finalY = list(final_corr.values())
        self.plot_results()

        self.plot(new_signal)






    def ReadSignals(self, file_path):
        samples = {}
        with open(file_path, "r") as file:
            for line in file:
                number_of_samples = int(line.strip())
                if number_of_samples == 0:
                    continue

                for _ in range(number_of_samples):
                    line = file.readline()
                    # read every single line, converts the values from string to float
                    index, value = map(float, line.strip().split())
                    samples[int(index)] = value

            indices = list(samples.keys())
            values = list(samples.values())
        return indices, values, samples


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = bonus(root)
    root.mainloop()






