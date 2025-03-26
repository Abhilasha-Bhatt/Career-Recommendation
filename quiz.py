from tkinter import *
from PIL import Image, ImageTk
import time
import pygame 
import os 
import sys

# Initialize sound system
pygame.mixer.init()

# Get the base directory for bundled files
base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

win = Tk()
win.title("AI Career Recommendation Quiz")
win.geometry("800x600")
win.maxsize(800, 600)  # Lock screen size

i = 0  # Track question index

career_images = {
    "Software Engineer": os.path.join(base_path, "software_bg.jpg"),
    "Data Scientist": os.path.join(base_path, "data_bg.jpg"),
    "Graphic Designer": os.path.join(base_path, "design_bg.jpg"),
    "Marketing Manager": os.path.join(base_path, "marketing_bg.jpg"),
}

# Load images dynamically
default_bg = Image.open(os.path.join(base_path, "default_bg.jpg")).resize((800, 600))
default_bg = ImageTk.PhotoImage(default_bg)

bg_label = Label(win, image=default_bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to play sound
def play_click_sound():
    pygame.mixer.Sound(os.path.join(base_path, "click.wav")).play()

# Questions & Answers
var1 = IntVar(value=0)
var2 = IntVar(value=0)
var3 = StringVar(value="")

questions = [
    ("Do you enjoy solving problems?", var1, [("Yes", 1), ("No", 0)]),
    ("Do you like working with data?", var2, [("Yes", 1), ("No", 0)]),
    ("Do you prefer creativity or logic?", var3, [("Creativity", "Creativity"), ("Logic", "Logic")])
]

frames = []
for text, var, options in questions:
    frame = Frame(win, bg="white")
    Label(frame, text=text, font=("Arial", 16, "bold"), bg="white").pack(pady=20)
    for opt_text, opt_value in options:
        Radiobutton(frame, text=opt_text, variable=var, value=opt_value, bg="white", font=("Arial", 12)).pack()
    frames.append(frame)

# Progress Label
progress_label = Label(win, text="Question 1/3", font=("Arial", 14, "bold"), bg="white")
progress_label.place(relx=0.5, rely=0.1, anchor=CENTER)

# Show first question
frames[0].place(relx=0.5, rely=0.4, anchor=CENTER)

# Function to show the next question
def next():
    global i
    play_click_sound()
    frames[i].place_forget()
    i += 1
    frames[i].place(relx=0.5, rely=0.4, anchor=CENTER)
    progress_label.config(text=f"Question {i+1}/{len(frames)}")

    b1.config(state=NORMAL if i > 0 else DISABLED)
    if i == len(frames) - 1:
        b2.pack_forget()
        b3.pack(fill="x", side="right", expand=True)

# Function to show the previous question
def previous():
    global i
    play_click_sound()
    frames[i].place_forget()
    i -= 1
    frames[i].place(relx=0.5, rely=0.4, anchor=CENTER)
    progress_label.config(text=f"Question {i+1}/{len(frames)}")

    b1.config(state=DISABLED if i == 0 else NORMAL)
    if i < len(frames) - 1:
        b2.pack(fill="x", side="right", expand=True)
        b3.pack_forget()

# Function to update background with a fade effect
def change_background(image_path):
    try:
        new_image = Image.open(image_path).resize((800, 600))
        new_bg = ImageTk.PhotoImage(new_image)
        bg_label.config(image=new_bg)
        bg_label.image = new_bg  # Keep reference
    except:
        pass  # If image not found, keep existing background

# Animated text reveal
def reveal_text(text, index=0):
    if index < len(text):
        result_label.config(text=text[:index+1])
        win.after(100, reveal_text, text, index + 1)  # Reveal next letter

# Function to display career result
def submit():
    global i
    play_click_sound()
    answers = [var1.get(), var2.get(), var3.get()]

    # Hide last question
    frames[i].place_forget()
    progress_label.place_forget()  # Hide progress label

    # Determine career
    if answers == [1, 0, "Logic"]:
        career = "Software Engineer"
    elif answers == [1, 1, "Logic"]:
        career = "Data Scientist"
    elif answers == [0, 0, "Creativity"]:
        career = "Graphic Designer"
    else:
        career = "Marketing Manager"  

    # Fade effect when changing background
    change_background(career_images.get(career, "default_bg.jpg"))

    # Show result with animated text
    reveal_text(f"Your recommended career: {career}")

    btn.pack_forget()

# Result label (hidden initially)
result_label = Label(win, text="", font=("Arial", 18, "bold"), bg="white", fg="black")
result_label.place(relx=0.5, rely=0.5, anchor=CENTER)

# Navigation buttons with better UI
btn = Frame(win, bg="white")
b1 = Button(btn, text="Previous", command=previous, state=DISABLED, font=("Arial", 12), bg="#FFCCCB", padx=10, pady=5)
b1.pack(fill="x", side="left", expand=True)

b2 = Button(btn, text="Next", command=next, font=("Arial", 12), bg="#90EE90", padx=10, pady=5)
b2.pack(fill="x", side="right", expand=True)

b3 = Button(btn, text="Get Career Recommendation", command=submit, font=("Arial", 12), bg="#ADD8E6", padx=10, pady=5)

btn.pack(fill="x", side="bottom")

win.mainloop()
