import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, messagebox, Button, Entry, Label
from Test_Cases_5.signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift

class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing App")
        
        # Data storage
        self.indices = []
        self.values = []
        self.amplitude = []
        self.phase = []
        self.freq = []
        
        # Reference data (to be loaded from the txt comparison file)
        self.reference_amplitude = []
        self.reference_phase = []
        
        # Initialize UI
        self.init_ui()

    def init_ui(self):
        load_button = Button(self.root, text="Load Signal Data", command=self.load_signal_file)
        load_button.pack(pady=10)
        
        comparison_button = Button(self.root, text="Load Reference Comparison File", command=self.load_comparison_file)
        comparison_button.pack(pady=10)
        
        sampling_label = Label(self.root, text="Enter Sampling Frequency (Hz):")
        sampling_label.pack(pady=5)
        
        self.sampling_entry = Entry(self.root)
        self.sampling_entry.pack(pady=5)
        
        compute_button = Button(self.root, text="Compute Fourier Transform", command=self.compute_fourier_transform)
        compute_button.pack(pady=10)

    def load_signal_file(self):
        file_path = filedialog.askopenfilename(title="Select Signal Data File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.load_signal_data(file_path)

    def load_signal_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.indices = []
                self.values = []
                for line in file:
                    try:
                        index, value = map(float, line.strip().split())
                        self.indices.append(index)
                        self.values.append(value)
                    except ValueError:
                        print(f"Skipping malformed line: {line.strip()}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal data: {e}")

    def load_comparison_file(self):
        file_path = filedialog.askopenfilename(title="Select Reference Comparison File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.load_comparison_data(file_path)

    def load_comparison_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.reference_amplitude = []
                self.reference_phase = []
                for line in file:
                    print(f"Processing line: '{line.strip()}'")
                    parts = line.strip().split()
                    if len(parts) == 2:  # Ensure two parts per line
                        try:
                            amplitude = float(parts[0].replace('f', '').strip())
                            phase = float(parts[1].replace('f', '').strip())
                            self.reference_amplitude.append(amplitude)
                            self.reference_phase.append(phase)
                        except ValueError:
                            continue
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load comparison data: {e}")

    def compute_fourier_transform(self):
        try:
            if not self.indices or not self.values:
                raise ValueError("No signal data loaded. Please load a valid signal data file first.")
            
            # Get the sampling frequency from the user input
            sampling_frequency = float(self.sampling_entry.get())
            if sampling_frequency <= 0:
                raise ValueError("Sampling frequency must be a positive number.")
            
            # Perform Fourier Transform
            signal = np.array(self.values)
            fft_result = np.fft.fft(signal)
            self.amplitude = np.abs(fft_result)
            self.phase = np.angle(fft_result)
            
            # Normalize phases to [-π, π]
            self.phase = (self.phase + np.pi) % (2 * np.pi) - np.pi

            # Compute frequency bins
            self.freq = np.fft.fftfreq(len(signal), d=1/sampling_frequency)
            
            print("Computed Fourier Transform")
            print("Frequency\tAmplitude\tPhase")
            for i, (amp, ph) in zip(self.freq, zip(self.amplitude, self.phase)):
                print(f"{i:.2f}\t{amp:.5f}\t{ph:.5f}")
            
            # Compare with reference data
            if self.reference_amplitude and self.reference_phase:
                amplitude_match = SignalComapreAmplitude(self.amplitude, self.reference_amplitude)
                phase_match = SignalComaprePhaseShift(self.phase, self.reference_phase)
                
                print("Amplitude Comparison:", "Match" if amplitude_match else "Mismatch")
                print("Phase Comparison:", "Match" if phase_match else "Mismatch")
                
                if amplitude_match and phase_match:
                    messagebox.showinfo("Comparison Result", "Amplitude and Phase match successfully!")
                else:
                    messagebox.showwarning("Comparison Result", "Amplitude or Phase mismatch detected.")
            
            # Plot the results (Amplitude and Phase)
            self.plot_results()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute Fourier Transform: {e}")

    def plot_results(self):
        try:
            # Create a new figure
            plt.figure(figsize=(12, 8))
            
            # Amplitude Spectrum Plot
            plt.subplot(2, 1, 1)
            plt.stem(self.freq, self.amplitude, basefmt=" ", label='Computed Amplitude', use_line_collection=True)
            plt.stem(self.freq[:len(self.reference_amplitude)], self.reference_amplitude, basefmt=" ", linefmt='r--', markerfmt='ro', label='Reference Amplitude', use_line_collection=True)
            plt.title('Amplitude Spectrum')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.grid(True)

            # Phase Spectrum Plot
            plt.subplot(2, 1, 2)
            plt.stem(self.freq, self.phase, basefmt=" ", label='Computed Phase', use_line_collection=True)
            plt.stem(self.freq[:len(self.reference_phase)], self.reference_phase, basefmt=" ", linefmt='r--', markerfmt='ro', label='Reference Phase', use_line_collection=True)
            plt.title('Phase Spectrum')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Phase (radians)')
            plt.legend()
            plt.grid(True)

            # Adjust layout for better spacing
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot results: {e}")


if __name__ == "__main__":
    root = Tk()
    app = SignalProcessingApp(root)
    root.mainloop()
