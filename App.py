# App.py
import tkinter as tk
from task1 import Task1
from task2 import Task2
from task3 import Task3

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Signal Processing GUI")
        self.root.configure(padx=20, pady=20)

        # Create frames for buttons and main content
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        # Create buttons to switch between tabs using grid
        self.tab1_button = tk.Button(self.button_frame, text="Task 1", command=self.show_task1)
        self.tab1_button.grid(row=0, column=0, padx=(0, 0), pady=5)

        self.tab2_button = tk.Button(self.button_frame, text="Task 2", command=self.show_task2)
        self.tab2_button.grid(row=0, column=1, padx=(0, 0), pady=5)

        self.tab2_button = tk.Button(self.button_frame, text="Task 3", command=self.show_task3)
        self.tab2_button.grid(row=0, column=2, padx=(0, 0), pady=5)

        # Create frames for each tab
        self.task1_frame = Task1(self.root)  # Task1 is now a class
        self.task2_frame = Task2(self.root)  #
        self.task3_frame = Task3(self.root)  

        self.show_task1()  # Show Task 1 by default

    def show_task1(self):
        self.task2_frame.hide()  # Hide Task 2
        self.task3_frame.hide()  # Hide Task 3
        self.task1_frame.display()  # Call display method of Task1


    def show_task2(self):
        self.task1_frame.hide()  
        self.task3_frame.hide()  
        self.task2_frame.display() 

    def show_task3(self):
        self.task1_frame.hide()  
        self.task2_frame.hide()  
        self.task3_frame.display() 

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
