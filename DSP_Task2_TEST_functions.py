#!/usr/bin/env python
# coding: utf-8
# %%


# %%

def ReadSignalFile(file_name):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples


# %%


def AddSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name="add.txt"  # write here the path of the add output file
    expected_indices,expected_samples=ReadSignalFile(file_name)          
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Addition Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Addition Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Addition Test case failed, your signal have different values from the expected one") 
            return
    print("Addition Test case passed successfully")

#AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt",indicies,samples) # call this function with your computed indicies and samples


# %%

def SubSignalSamplesAreEqual(userFirstSignal,userSecondSignal,Your_indices,Your_samples):
    if(userFirstSignal=='Signal1.txt' and userSecondSignal=='Signal2.txt'):
        file_name="subtract.txt" # write here the path of the subtract output file
        
    expected_indices,expected_samples=ReadSignalFile(file_name)   
    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Subtraction Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Subtraction Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Subtraction Test case failed, your signal have different values from the expected one") 
            return
    print("Subtraction Test case passed successfully")
    
#SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt",indicies,samples)  # call this function with your computed indicies and samples


# %%


def MultiplySignalByConst(User_Const,Your_indices,Your_samples):
    if(User_Const==5):
        file_name="mul5.txt"  # write here the path of the mul5 output file
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Multiply by "+str(User_Const)+ " Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Multiply by "+str(User_Const)+" Test case failed, your signal have different values from the expected one") 
            return
    print("Multiply by "+str(User_Const)+" Test case passed successfully")

#MultiplySignalByConst(5,indicies, samples)# call this function with your computed indicies and samples


# %%


def ShiftSignalByConst(Shift_value,Your_indices,Your_samples):
    if(Shift_value==3):  #x(n+k)
        file_name="advance3.txt" # write here the path of delay3 output file
    elif(Shift_value==-3): #x(n-k)
        file_name="delay3.txt" # write here the path of advance3 output file
        
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift by "+str(Shift_value)+" Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift by "+str(Shift_value)+" Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Shift by "+str(Shift_value)+" Test case failed, your signal have different values from the expected one") 
            return
    print("Shift by "+str(Shift_value)+" Test case passed successfully")

#ShiftSignalByConst(3,indicies,samples)  # call this function with your computed indicies and samples

# %%


def Folding(Your_indices,Your_samples):
    file_name = "folding.txt"  # write here the path of the folding output file
    expected_indices,expected_samples=ReadSignalFile(file_name)      
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Folding Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Folding Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Folding Test case failed, your signal have different values from the expected one") 
            return
    print("Folding Test case passed successfully")

#Folding(indicies,samples)  # call this function with your computed indicies and samples

# %%
# #Read Files
# def read_signals(file_path):
#     samples = {}
#     with open(file_path, 'r') as file:
#         for line in file:
#             number_of_samples = int(line.strip())
#             if(number_of_samples == 0):
#                 continue

#             for _ in range(number_of_samples):
#                 line = file.readline()
#                 index, value = map(float, line.strip().split()) #read every single line, converts the values from string to float
#                 samples[int(index)] = value

#         indices = list(samples.keys())
#         values = list(samples.values())
#     return indices, values, samples

# signalA = read_signals('Signal1.txt')
# signalB = read_signals('Signal2.txt')

# #print(signalA[2])
# import matplotlib.pyplot as plt

# def plot_signal(samples):
#     indices = list(samples.keys())
#     values = list(samples.values())
#     plt.figure(figsize=(10, 5))
#     plt.stem(indices, values)
#     plt.title('Signal Visualization')
#     plt.xlabel('Index')
#     plt.ylabel('Value')
#     plt.grid()
#     plt.show()

# def add_signals(signal_a, signal_b):

#     combined = {}

#     # Add values from the first signal
#     for index, value in signal_a[2].items():
#         combined[index] = value

#     # Add values from the second signal
#     for index, value in signal_b[2].items():
#         if index in combined:
#             combined[index] += value  # Sum the values for overlapping keys
#         else:
#             combined[index] = value  # Add new key-value pairs
#     # Convert the combined dictionary back to a sorted list
#     result = sorted(combined.items())
#     print(result)
#     indices = list(combined.keys())
#     values = list(combined.values())
#     plot_signal(combined)
#     return indices, values


# def sub_signals(signal_a, signal_b):

#     combined = {}

#     # Add values from the first signal
#     for index, value in signal_a[2].items():
#         combined[index] = value
#     #combined += signal_a[1]

#     # Add values from the second signal
#     for index, value in signal_b[2].items():
#         if index in combined:
#             combined[index] -= value  # Sum the values for overlapping keys
#         else:
#             combined[index] = value  # Add new key-value pairs
#     # Convert the combined dictionary back to a sorted list
#     combined = dict(sorted(combined.items()))
#     indices = list(combined.keys())
#     values = list(combined.values())
#     return indices, values


# def multiply_signals(signal_a, constant):

#     combined = {}
#     for index, value in signal_a[2].items():
#         combined[index] = value * constant

#     combined = dict(sorted(combined.items()))
#     indices = list(combined.keys())
#     values = list(combined.values())
#     return indices, values

# def shift_signal(signal_a, constant):

#     combined = {}
#     for index, value in signal_a[2].items():
#         combined[index + constant] = value 

#     combined = dict(sorted(combined.items()))
#     indices = list(combined.keys())
#     values = list(combined.values())
#     return indices, values

# def fold_signals(signal_a):

#     combined = {}

#     # Add values from the first signal
#     for index, value in signal_a[2].items():
#         combined[-index] = value 

#     combined = dict(sorted(combined.items()))
#     indices = list((combined.keys()))
#     values = list((combined.values()))
#     return indices, values

# #add_indices, add_values = add_signals(signalA, signalB)
# sub_indices, sub_values = sub_signals(signalA, signalB)
# mul_indices, mul_values = multiply_signals(signalA, 5)
# delay_indices, delay_values =shift_signal(signalA, -3)
# advance_indices, advnace_values =shift_signal(signalA, 3)
# fold_indices, fold_values = fold_signals(signalA,)


# #AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", add_indices, add_values) # call this function with your computed indicies and samples
# SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", sub_indices, sub_values)  # call this function with your computed indicies and samples
# MultiplySignalByConst(5,mul_indices, mul_values)# call this function with your computed indicies and samples
# ShiftSignalByConst(3,delay_indices, delay_values)  # call this function with your computed indicies and samples
# ShiftSignalByConst(-3,advance_indices, advnace_values)  # call this function with your computed indicies and samples
# Folding(fold_indices, fold_values) 

# from tkinter import *
# application = Tk()
# #w = Label(application, text='DSP TASK1 !')
# application.title('Counting Seconds')
# button = Button(application, text='add', width=25, command= add_signals(signalA, signalB))
# button.pack()
# application.mainloop()
