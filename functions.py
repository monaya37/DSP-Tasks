import os
import matplotlib.pyplot as plt
from task1_files.DSP_Task2_TEST_functions import *


def PlotSignal(samples, ax, canvas):
    ax.clear()
    
    indices = list(samples.keys())
    values = list(samples.values())
    
    ax.stem(indices, values)
    ax.set_title("Signal Visualization")
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.grid()
    canvas.draw()

def ReadSignals(file_path):
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


def ReadSignalValues(file_path):
    signal_values = []
    indices = []
    
    with open(file_path, 'r') as file:
        for idx, line in enumerate(file):  # `idx` will be the line number (index)
            # Strip any whitespace or newline characters and convert to integer
            stripped_line = line.strip()
            if stripped_line.isdigit():
                signal_values.append(int(stripped_line))
                indices.append(idx)  # Store the index (line number)
            else:
                print(f"Skipping invalid line: {line}")
    
    return indices, signal_values

# read multiple files from a dir
def ReadSignalsFromDir(signals_dir, max_files=5):

    signals_data = []
    try:
        txt_files = [f for f in os.listdir(signals_dir) if f.endswith('.txt')]
        for i, file_name in enumerate(txt_files[:max_files]):
            file_path = os.path.join(signals_dir, file_name)
            signals_data.append(ReadSignalValues(file_path))
    except FileNotFoundError:
        print(f"Error: Directory '{signals_dir}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred while processing the directory: {e}")
    return signals_data

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

def CompareOutput(Your_indices, Your_samples, file_name):

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        print("Comparing Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if (Your_indices[i] != expected_indices[i]):
            print("Comparing Test case failed, your signal have different indicies from the expected one")


def CompareOutput(Your_indices, Your_samples, output_file):
    expected_indices, expected_samples = ReadSignalFile(output_file)
    if (len(expected_samples) != len(Your_samples)) and (len(expected_indices) != len(Your_indices)):
        print("Compare Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if (Your_indices[i] != expected_indices[i]):
            print("Compare Test case failed, your signal have different indicies from the expected one")
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Comparing Test case failed, your signal have different values from the expected one")
            return
    print("Comparing Test case passed successfully")


