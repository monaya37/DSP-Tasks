import matplotlib.pyplot as plt
from DSP_Task2_TEST_functions import *


class functions:

  


    # Functions
    def plot_signal(samples):
        indices = list(samples.keys())
        values = list(samples.values())
        plt.figure(figsize=(10, 5))
        plt.stem(indices, values)
        plt.title("Signal Visualization")
        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.grid()
        plt.show()

    def read_signals(file_path):
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
            functions.plot_signal(samples)
        return indices, values, samples

    def add_signals(signal_a, signal_b):
        combined = {}

        for index, value in signal_a[2].items():
            combined[index] = value

        for index, value in signal_b[2].items():
            if index in combined:
                combined[index] += value  # Sum the values for overlapping keys
            else:
                combined[index] = value  # Add new key-value pairs

        combined = dict(sorted(combined.items()))
        indices = list(combined.keys())
        values = list(combined.values())
        return indices, values, combined

    def sub_signals(signal_a, signal_b):
        combined = {}

        for index, value in signal_a[2].items():
            combined[index] = value

        for index, value in signal_b[2].items():
            if index in combined:
                combined[index] -= value
            else:
                combined[index] = -value

        combined = dict(sorted(combined.items()))
        indices = list(combined.keys())
        values = list(combined.values())
        return indices, values, combined

    def multiply_signals(signal_a, constant):
        combined = {}
        for index, value in signal_a[2].items():
            combined[index] = value * constant

        combined = dict(sorted(combined.items()))
        indices = list(combined.keys())
        values = list(combined.values())
        return indices, values, combined

    def shift_signal(signal_a, constant):
        combined = {}
        for index, value in signal_a[2].items():
            combined[index + -1 * constant] = value

        combined = dict(sorted(combined.items()))
        indices = list(combined.keys())
        values = list(combined.values())
        return indices, values, combined

    def fold_signals(signal_a):
        combined = {}
        for index, value in signal_a[2].items():
            combined[-index] = value

        combined = dict(sorted(combined.items()))
        indices = list(combined.keys())
        values = list(combined.values())
        return indices, values, combined
