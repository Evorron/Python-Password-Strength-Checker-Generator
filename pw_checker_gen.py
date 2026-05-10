from tkinter import Tk, Label, Entry, Button, Checkbutton, Frame, Scale, StringVar, BooleanVar
from math import log2, floor    # Perform math operations
import re   # Regex search for password character sets
import secrets
import string

# ~~~~~~~~~~~~~~~~~~~~ Classes
# Password Structure Class
class pw_struct:
    def __init__(self, length, char_range):
        self.length = length
        self.char_range = char_range

    # Formulas
    def permutation(self):
        combinations = pow(self.length, self.char_range)
        return combinations

    def entropy(self):
        entropy_bits = floor((self.length) * log2(self.char_range))
        return entropy_bits

# ~~~~~~~~~~~~~~~~~~~~ Functions

# ~~~~~~~~~~~~~~~~~~~~ Left Frame Functions
# Get password structure
def pw_length(password_input):
    return len(password_input)

def get_range(password_input):
    char_range = 0

    # Lower case
    if re.search("[a-z]", password_input):
        char_range += 26
    
    if re.search("[A-Z]", password_input):
        char_range += 26
    if re.search("[0-9]", password_input):
        char_range += 10
     #if re.search <Symbols>

    return char_range

# Retrieve user-supplied password
def show_results(event=None):   # Keybind events will pass arguments, while normal callbacks will not, hence "event=None"
    # Ensure's that password variable is updated each time function is called via the submit button
    password = password_input.get()
    
    pw_info = pw_struct(pw_length(password), get_range(password))

    if pw_info.length >= 15:
        pw_label.config(text=f"""
Password Length: {pw_info.length} characters
It has {pw_info.permutation():,} combinations
Total Entropy Bits: ~{pw_info.entropy()}
""", justify="center")

    else:
        pw_label.config(text=f"Ensure your password has a minimum of 15 characters (Character count: {pw_info.length})")


# ~~~~~~~~~~~~~~~~~~~~ Right Frame Functions
# Sums up count of checkbox states, checks if all are "unchecked", "False", "0"
def checkbox_state(current_var):
  # Returns how many are still checked
    if sum(current_var.get() for current_var, _ in checkbox_vars) == 0:         
        current_var.set(True)

# Generate random password string based on user specified length
def generate_pw(pw_length=None):
    selected_char_sets = ""

    for var, char_set in checkbox_vars:
        if var.get():
            selected_char_sets += char_set


    password = "".join(secrets.choice(selected_char_sets) for i in range(int(pw_char_slider.get())))
    pw_var = StringVar(value=password)
    show_generated_pw.config(textvariable=pw_var)
    
def copy_pw_clipboard():
    try:
        main_window.clipboard_clear()                           # Clear the clipboard
        main_window.clipboard_append(show_generated_pw.get())   # Copy to clipboard
    except :
        pass
    


# Creating a Tkinter instance
main_window = Tk()

# Main application window
# main_window.minsize(width=1400, height=700)
main_window.title("Password Strength Checker")
main_window.minsize(1400, 700)

# ~~~~~~~~~~~~~~~~~~~~ Frames
# Left Frame
left_frame = Frame(main_window, width=700, height=700, bd=2, relief="solid", bg="#BBE1FA")
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)

# Right Frame
right_frame = Frame(main_window, width=700, height=350, bd=2, relief="solid", bg="#BBE1FA")
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Right Frame (Row 2)
right_frame_2 = Frame(main_window, width=700, height=350, bd=2, relief="solid", bg="#BBE1FA")
right_frame_2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")




# ~~~~~~~~~~~~~~~~~~~~ Widgets

# ~~~~~~~~~~~~~~~~~~~~ Left Frame Widgets
# Password Checker Label
pw_checker_header = Label(left_frame, text="Password Checker", height=3, relief="ridge", background="#3282B8").grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Password requirements Label
pw_requirements = Label(left_frame, text=f"""Requirements for a good password:
                        1. Minimum of 15 characters (The longer the better!)
                        2. Use passphrases (Combination of various words)
                        3. (Optional) Upper/Lower case letters, numbers, special characters can help
                        """).grid(row=1, column=0, sticky="nsew")

# # Password input
password_input = Entry(left_frame, width=50, font=("Arial", 15), relief="sunken")
password_input.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
password_input.bind("<Return>", show_results) # Bind "Enter" key to "submit" the entry value

# Submit button
button = Button(left_frame, text="Submit", command=show_results).grid(row=3, column=0, sticky="ns")

# Password Result Label
pw_label = Label(left_frame, text="", background="#0F4C75")
pw_label.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

# ~~~~~~~~~~~~~~~~~~~~ Right Frame Widgets
generate_pw_label = Label(right_frame, text="Generate Password", height=3, relief="ridge", background="#3282B8").grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=3)

pw_var = StringVar()
show_generated_pw = Entry(right_frame, textvariable=pw_var, relief="sunken")
show_generated_pw.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

generate_new_pw = Button(right_frame, text="New", command=generate_pw).grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
clipboard_copy = Button(right_frame, text="Copy To Clipboard", command=copy_pw_clipboard).grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

generator_settings = Frame(right_frame)
generator_settings.grid(row=2, column=0, sticky="nsew", padx=5, pady=5, columnspan=3)

slider_label = Label(generator_settings, text="Password Length:").grid(row=0, column=0)
characters = Label(generator_settings, text="Characters Used:").grid(row=1, column=0)

pw_char_slider = Scale(generator_settings, from_=15, to=50,orient="horizontal", command=generate_pw)
pw_char_slider.grid(row=0, column=1, padx=5, pady=5, columnspan=4, sticky="ew")

# Create checkbox control variables
checkbox_vars = []   # List to store BooleanVar() objects for each checkbox
checkbox_options = {"Uppercase": string.ascii_uppercase, 
                    "Lowercase": string.ascii_lowercase, 
                    "Numbers": string.digits, 
                    "Special-Characters": string.punctuation}  # Checkbox options

# Dynamically creating checkboxes using a loop
for index, (k, v) in enumerate(checkbox_options.items(), start=1):      # Enumerate over the "checkbox_options" list to retrieve (index, element) pair
    var = BooleanVar(value=True)                                       # Create BooleanVars for each checkbox (Value = 1 -> Checked when program executes)
    checkbox = Checkbutton(generator_settings, text=k, variable=var, command=lambda current_var=var: checkbox_state(current_var))
    # Uses the current iteration and state of BooleanVar "var", this prevents each iteration from using the same "var" value. i.e. It's the same as creating multiple BooleanVar => In this case, we are using a different "version" while using the same variable name
    checkbox.grid(row=1, column=index)                          # Element for setting widget text, Index for specifying grid layout
    checkbox_vars.append((var, v))                                   # Stores the control variable


# ~~~~~~~~~~~~~~~~~~~~ Grid Configurations
# Main Window Configs
main_window.rowconfigure(0, weight=1)
main_window.rowconfigure(1, weight=1)
main_window.columnconfigure((0,1), weight=1, uniform="main_window_frames")

# Left Frame Config
left_frame.columnconfigure(0, weight=1)
left_frame.rowconfigure(4, weight=1)

# Right Frame Config
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(2, weight=1)


# Starts application event loop (Allows program computer events)
main_window.mainloop()