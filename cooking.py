import tkinter as tk
import pygame
import subprocess
from tkinter import simpledialog

pygame.init()

window = tk.Tk()
window.title("Cooking Timer")

window.geometry("1912x1010")
window.eval('tk::PlaceWindow . center')

frame = tk.Frame(window, bg="lightgray")
frame.pack(expand=True, fill='both')

cooking_items = [
    ("Noodles", None),
    ("Egg", None),
    ("Boiling Water", None)
]

running_sound = pygame.mixer.Sound("running.mp3")
attention_sound = pygame.mixer.Sound("attention.mp3")
noodles_voice_sound = pygame.mixer.Sound("nod_voice.wav")
egg_voice_sound = pygame.mixer.Sound("egg_voice.wav")
water_voice_sound = pygame.mixer.Sound("wat_voice.wav")

current_timer = None
timer_running = False
message_blinking = False

running_sound_channel = None
attention_sound_channel = None
voice_sound_channel = None

def get_duration(item):
    while True:
        time = simpledialog.askfloat("Set Timer", f"Enter time for {item[0]} (in minutes):")
        if time is not None:
            return time

def start_timer(item, time):
    global current_timer, timer_running
    if timer_running:
        stop_timer()
    current_timer = (item[0], time)
    label.config(text=f"Timer for {item[0]}: {time} minutes", fg="black", font=("Helvetica", 16, "bold"))
    countdown(time * 60)
    timer_running = True
    stop_button.config(state=tk.NORMAL)
    hide_message()
    play_running_sound()

def stop_timer():
    global current_timer, timer_running
    if timer_running:
        label.config(text="Timer stopped.", fg="red", font=("Helvetica", 16))
        window.after_cancel(timer_id)
        timer_running = False
        stop_button.config(state=tk.DISABLED)
        current_timer = None
        play_attention_sound()
        pygame.mixer.stop()
        stop_voice_sound()

def countdown(seconds):
    global timer_id
    if seconds > 0:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        label.config(text=f"Time left: {minutes}:{remaining_seconds:02}", fg="green", font=("Helvetica", 18, "bold"))
        timer_id = window.after(1000, countdown, seconds - 1)
    else:
        item, _ = current_timer
        display_message(item)

def display_message(item):
    global message_blinking
    message_label.config(text=f"{item} is ready!", fg="red", font=("Helvetica", 16, "bold"))
    message_blinking = True
    toggle_message(5)
    play_voice_sound(item)

def toggle_message(count):
    global message_blinking
    if count > 0:
        if message_label.cget("fg") == "red":
            message_label.config(fg="white")
        else:
            message_label.config(fg="red")
        window.after(500, toggle_message, count - 1)
    else:
        message_label.config(fg="red")
        message_blinking = False

def hide_message():
    global message_blinking
    if message_blinking:
        message_label.config(fg="white")
        window.after(100, hide_message)

def clear_message():
    global message_blinking
    message_label.config(text="", fg="white")
    message_blinking = False

def play_running_sound():
    global running_sound_channel
    running_sound_channel = running_sound.play()

def play_attention_sound():
    global attention_sound_channel
    attention_sound_channel = attention_sound.play()

def play_voice_sound(item):
    global voice_sound_channel
    if item == "Noodles":
        voice_sound_channel = noodles_voice_sound.play(-1)
    elif item == "Egg":
        voice_sound_channel = egg_voice_sound.play(-1)
    elif item == "Boiling Water":
        voice_sound_channel = water_voice_sound.play(-1)

def stop_voice_sound():
    global voice_sound_channel
    if voice_sound_channel is not None:
        pygame.mixer.stop()

def close_window():
    window.destroy()
    subprocess.Popen(["python", "main.py"])

buttons = []
for item in cooking_items:
    button = tk.Button(frame, text=item[0], font=("Helvetica", 16, "bold"), bg="lightblue", command=lambda item=item: start_timer(item, get_duration(item)))
    button.pack(pady=10, expand=True, fill='both')
    buttons.append(button)

label = tk.Label(frame, text="", font=("Helvetica", 18, "bold"), fg="green")
label.pack(pady=20)

stop_button = tk.Button(frame, text="Stop", font=("Helvetica", 14), state=tk.DISABLED, command=stop_timer)
stop_button.pack(pady=10, expand=True, fill='both')

back_button = tk.Button(frame, text="Back to Main Page", font=("Helvetica", 14), command=close_window)
back_button.pack(pady=10, expand=True, fill='both')

message_label = tk.Label(frame, text="", font=("Helvetica", 18, "bold"), fg="white")
message_label.pack(pady=20)

window.mainloop()
