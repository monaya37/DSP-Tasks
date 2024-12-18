# App.py
import tkinter as tk
from task1 import Task1
from task2 import Task2
from task3 import Task3
from task4 import Task4
from task5 import Task5
from task6 import Task6
from task7 import Task7

class App:
    def __init__(self, root):

        self.root = root
        self.root.title("Digital Signal Processing GUI")
        self.root.geometry("800x800")
        self.root.configure(padx=20, pady=20)

        large_font = ('Helvetica', 14)
        self.pady = 5
        # Create frames for buttons and main content
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        # Create buttons to switch between tabs using grid
        self.tab1_button = tk.Button(self.button_frame, text="Task 1", command=self.show_task1, font=large_font)
        self.tab1_button.grid(row=0, column=0, padx=(0, 0), pady=self.pady)

        self.tab2_button = tk.Button(self.button_frame, text="Task 2", command=self.show_task2, font=large_font)
        self.tab2_button.grid(row=0, column=1, padx=(0, 0), pady=self.pady)

        self.tab3_button = tk.Button(self.button_frame, text="Task 3", command=self.show_task3, font=large_font)
        self.tab3_button.grid(row=0, column=2, padx=(0, 0), pady=self.pady)

        self.tab4_button = tk.Button(self.button_frame, text="Task 4", command=self.show_task4, font=large_font)
        self.tab4_button.grid(row=0, column=3, padx=(0, 0), pady=self.pady)

        self.tab5_button = tk.Button(self.button_frame, text="Task 5", command=self.show_task5, font=large_font)
        self.tab5_button.grid(row=0, column=4, padx=(0, 0), pady=self.pady)

        self.tab6_button = tk.Button(self.button_frame, text="Task 6", command=self.show_task6, font=large_font)
        self.tab6_button.grid(row=0, column=5, padx=(0, 0), pady=self.pady)

        self.tab7_button = tk.Button(self.button_frame, text="Task 7", command=self.show_task7, font=large_font)
        self.tab7_button.grid(row=0, column=6, padx=(0, 0), pady=self.pady)

        # Create frames for each tab
        self.task1_frame = Task1(self.root)  # Task1 is now a class
        self.task2_frame = Task2(self.root)  #
        self.task3_frame = Task3(self.root)  
        self.task4_frame = Task4(self.root)  
        self.task5_frame = Task5(self.root)  
        self.task6_frame = Task6(self.root)  
        self.task7_frame = Task7(self.root)  

        self.show_task7()  # Show Task 1 by default

    def show_task1(self):
        self.task2_frame.hide()  # Hide Task 2
        self.task3_frame.hide()  # Hide Task 3
        self.task4_frame.hide()  # Hide Task 3
        self.task5_frame.hide() 
        self.task6_frame.hide()
        self.task7_frame.hide()
        self.task1_frame.display()  # Call display method of Task1


    def show_task2(self):
        self.task1_frame.hide()  
        self.task3_frame.hide()  
        self.task4_frame.hide()  
        self.task5_frame.hide()
        self.task6_frame.hide() 
        self.task7_frame.hide()
        self.task2_frame.display() 


    def show_task3(self):
        self.task1_frame.hide()  
        self.task2_frame.hide()  
        self.task4_frame.hide()  
        self.task5_frame.hide() 
        self.task6_frame.hide() 
        self.task7_frame.hide()
        self.task3_frame.display() 


    def show_task4(self):
        self.task1_frame.hide()  
        self.task2_frame.hide()  
        self.task3_frame.hide()  
        self.task5_frame.hide() 
        self.task6_frame.hide() 
        self.task7_frame.hide()
        self.task4_frame.display() 

    def show_task5(self):
        self.task1_frame.hide()  
        self.task2_frame.hide()  
        self.task3_frame.hide()  
        self.task4_frame.hide() 
        self.task6_frame.hide() 
        self.task7_frame.hide()
        self.task5_frame.display() 

    def show_task6(self):
        self.task1_frame.hide()  
        self.task2_frame.hide()  
        self.task3_frame.hide()  
        self.task4_frame.hide() 
        self.task5_frame.hide() 
        self.task7_frame.hide()
        self.task6_frame.display() 

    def show_task7(self):
        self.task1_frame.hide()  
        self.task2_frame.hide()  
        self.task3_frame.hide()  
        self.task4_frame.hide() 
        self.task5_frame.hide() 
        self.task6_frame.hide()
        self.task7_frame.display() 

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
