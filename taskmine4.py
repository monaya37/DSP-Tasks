import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class MovingAverageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Moving Average Computation")
        self.geometry("800x600")

        # Input fields
        ttk.Label(self, text="Input File:").pack(pady=5)
        self.input_file_entry = ttk.Entry(self, width=50)
        self.input_file_entry.pack(pady=5)
        ttk.Button(self, text="Browse", command=self.select_input_file).pack(pady=5)

        ttk.Label(self, text="Reference Output File:").pack(pady=5)
        self.output_file_entry = ttk.Entry(self, width=50)
        self.output_file_entry.pack(pady=5)
        ttk.Button(self, text="Browse", command=self.select_output_file).pack(pady=5)

        ttk.Label(self, text="Window Size (M):").pack(pady=5)
        self.window_size_var = tk.IntVar(value=3)
        ttk.Entry(self, textvariable=self.window_size_var).pack(pady=5)

        ttk.Button(self, text="Compute Moving Average", command=self.compute_moving_average).pack(pady=10)

        # Result display
        self.result_text = tk.Text(self, height=20, wrap=tk.WORD)
        self.result_text.pack(pady=10, fill="both", expand=True)

    def select_input_file(self):
        """Open a file dialog to select the input file."""
        filepath = filedialog.askopenfilename(title="Select Input File")
        if filepath:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, filepath)

    def select_output_file(self):
        """Open a file dialog to select the reference output file."""
        filepath = filedialog.askopenfilename(title="Select Output File")
        if filepath:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, filepath)

    def load_signal(self, filepath):
        """Load a signal from the specified file."""
        indices, values = [], []
        try:
            with open(filepath, 'r') as file:
                # Debug: Print the entire file content to verify
                file_content = file.read()
                print("File contents:")
                print(file_content)

                # Rewind the file pointer to start reading again
                file.seek(0)

                # Skip the first line (header)
                file.readline()

                # Skip the second line (another header or arbitrary value)
                file.readline()

                # Read the number of samples
                num_samples_line = file.readline().strip()
                print(f"Raw number of samples line: '{num_samples_line}'")

                # Ensure the number of samples is correctly parsed
                num_samples = int(num_samples_line) if num_samples_line.isdigit() else 0
                print(f"Number of samples: {num_samples}")

                # Read the actual data lines
                for _ in range(num_samples):
                    line = file.readline().strip()
                    if line:  # Avoid empty lines
                        index, value = map(float, line.split())
                        indices.append(int(index))
                        values.append(value)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal from {filepath}: {e}")
        return indices, values

    def compare_results(self, computed, reference_indices, reference_values, tolerance=1e-3):
        if len(computed) != len(reference_values):
            return False, f"Length mismatch: Expected {len(reference_values)}, got {len(computed)}"
        mismatches = [
            (reference_indices[i], computed[i], reference_values[i])
            for i in range(len(computed))
            if abs(computed[i] - reference_values[i]) > tolerance
        ]
        if mismatches:
            details = "\n".join(
                [f"Index {idx}: Computed={comp:.5f}, Expected={ref:.5f}" for idx, comp, ref in mismatches]
            )
            return False, f"Mismatches found:\n{details}"
        return True, "All values match."

    def compute_moving_average(self):
        """Compute and display the moving average."""
        input_file = self.input_file_entry.get()
        output_file = self.output_file_entry.get()
        if not input_file or not output_file:
            messagebox.showwarning("Warning", "Please select both input and reference output files!")
            return

        M = self.window_size_var.get()
        if M <= 0:
            messagebox.showerror("Error", "Window size must be greater than 0!")
            return

        # Load the input signal and reference output
        indices, values = self.load_signal(input_file)
        ref_indices, ref_values = self.load_signal(output_file)

        if len(indices) == 0 or len(values) == 0:
            messagebox.showerror("Error", "The input file seems empty or invalid.")
            return
        if len(ref_indices) == 0 or len(ref_values) == 0:
            messagebox.showerror("Error", "The reference output file seems empty or invalid.")
            return

        # Compute moving average
        moving_avg = []
        valid_indices = []  # Keep track of indices for valid moving averages
        for i in range(len(values)):
            if i < M - 1:
                continue  # Skip indices where averaging cannot be done
            avg = round(sum(values[i - M + 1:i + 1]) / M, 3)
            moving_avg.append(avg)
            valid_indices.append(indices[i])  # Record valid index

        # Display results
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, "Computed Moving Average Results (y(n))\n")
        self.result_text.insert(tk.END, "Index\tValue (y(n))\n")
        for idx, val in zip(valid_indices, moving_avg):
            self.result_text.insert(tk.END, f"{idx}\t{val:.5f}\n")

        # Compare with reference output
        pass_test, message = self.compare_results(moving_avg, ref_indices, ref_values)
        if pass_test:
            self.result_text.insert(tk.END, "\nTest Passed: Computed values match reference output.\n")
        else:
            self.result_text.insert(tk.END, f"\nTest Failed:\n{message}\n")

        messagebox.showinfo("Test Result", f"Moving Average Test: {'Passed' if pass_test else 'Failed'}\n{message}")

if __name__ == "__main__":
    app = MovingAverageApp()
    app.mainloop()
