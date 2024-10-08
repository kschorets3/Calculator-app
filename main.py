import tkinter as tk
import customtkinter as ctk
import math
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Initialize the main window
root = ctk.CTk()
root.title("Calculator")
root.geometry("450x500")

buttons_list = []   # List to keep track of all buttons

# Function for errors
def display_error(message):
    display.delete(0, tk.END)
    display.insert(0, f"Error: {message}")
    for btn in buttons_list:  
        btn.configure(state="disabled") # Disable all buttons
    root.after(1500, clear_error)   # Reenable buttons and clear error

# Function to clear error and reenable buttons
def clear_error():
    display.delete(0, tk.END)
    for btn in buttons_list:    
        btn.configure(state="normal")   # Reenable all buttons
        
# Create the display widget
display = ctk.CTkEntry(root, font=("Segoe", 30), justify="right")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

# Function to handle button clicks
def button_click(number):
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current + str(number))

# Function to clear the display
def clear_display():
    display.delete(0, tk.END)

# Backspace function
def backspace():
    current = display.get()
    if current:
        display.delete(len(current)-1, tk.END)
        
# Function to evaluate the expression
def evaluate_expression():
    try:
        result = eval(display.get())
        display.delete(0, tk.END)
        display.insert(0, str(result))
    except ZeroDivisionError:
        display_error("Division by zero")
    except SyntaxError:
        display_error("Invalid syntax")
    except NameError:
        display_error("Invalid variable name")
    except ValueError:
        display_error("Invalid value")
    except OverflowError:
        display_error("Result too large")
    except Exception as e:
        display_error(f"Unexpected error")

def process_last_number(operation):
    current = display.get()
    if not current:
        display_error("No input provided")
        return
    operators = ['+', '-', '*', '/']
    last_op_index = max([current.rfind(op) for op in operators])
    start_index = last_op_index + 1 if last_op_index != -1 else 0
    last_number = current[start_index:]
    try:
        if operation == '1':
            result = '0'
        elif operation == '2':
            result = float(last_number) / 100.0
        elif operation == '3':
            if float(last_number) == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = 1 / float(last_number)
        elif operation == '4':
            result = float(last_number) ** 2
        elif operation == '5':
            if float(last_number) < 0:
                raise ValueError("Cannot sqrt negative")
            result = math.sqrt(float(last_number))
        elif operation == '6':
            result = -float(last_number) if last_number[0] != '-' else last_number[1:]
        else:
            raise ValueError("Unknown operation")
        new_expression = current[:start_index] + str(result)
        display.delete(0, tk.END)
        display.insert(0, new_expression)
    except ValueError as e:
        display_error(str(e) if str(e) else "Invalid input")
    except ZeroDivisionError as e:
        display_error(str(e))
    except OverflowError:
        display_error("Result too large")
    except Exception as e:
        display_error(f"Unexpected error")

# Define button labels and positions
buttons = [
    ('%', 1, 0), ('CE', 1, 1), ('C', 1, 2), ('DEL', 1, 3),
    ('1/𝔁', 2, 0), ('𝔁²', 2, 1), ('√', 2, 2), ('/', 2, 3),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('*', 3, 3),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('+', 5, 3),
    ('+/-', 6, 0), ('0', 6, 1), ('.', 6, 2), ('=', 6, 3)]

# Define a dictionary to map button text to functions
button_functions = {
    '=': evaluate_expression,
    'C': clear_display,
    'DEL': backspace,
    'CE': lambda: process_last_number('1'),
    '%': lambda: process_last_number('2'),
    '1/𝔁': lambda: process_last_number('3'),
    '𝔁²': lambda: process_last_number('4'),
    '√': lambda: process_last_number('5'),
    '+/-': lambda: process_last_number('6')}

# Create and place buttons on the grid
for (text, row, col) in buttons:
    if text in button_functions:
        command = button_functions[text]
    else:
        command = lambda t=text: button_click(t)
    btn = ctk.CTkButton(root, text=text, font=("Segoe", 20), command=command)
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    buttons_list.append(btn)  # Add button to the list

# Configure grid weights 
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(7):
    root.grid_rowconfigure(i, weight=1)

# Start the main loop
root.mainloop()