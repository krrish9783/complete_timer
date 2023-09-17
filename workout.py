import tkinter as tk
import pygame
import subprocess
from tkinter import simpledialog

pygame.init()

window = tk.Tk()
window.title("Workout Timer")

window.geometry("1912x1010")
window.eval('tk::PlaceWindow . center')

frame = tk.Frame(window, bg="#f5f5f5")
frame.pack(expand=True, fill='both')

workout_exercises = [
    ("Push-ups", None),
    ("Jumping Jacks", None),
    ("Plank", None),
    ("Running", None),
]

running_sound = pygame.mixer.Sound("running.mp3")
attention_sound = pygame.mixer.Sound("attention.mp3")

current_timer = None
timer_running = False
message_blinking = False

running_sound_channel = None
attention_sound_channel = None

def get_duration(exercise):
    while True:
        duration = simpledialog.askinteger("Set Exercise Duration", f"Enter duration for {exercise[0]} (in seconds):")
        if duration is not None:
            return duration

def start_timer(exercise):
    global current_timer, timer_running
    if timer_running:
        stop_timer()
    duration = get_duration(exercise)
    current_timer = (exercise[0], duration)
    label.config(text=f"Exercise: {exercise[0]}\nTime: {format_time(duration)}", fg="#333", font=("Arial", 16, "bold"))
    countdown(duration)
    timer_running = True
    stop_button.config(state=tk.NORMAL)
    hide_message()
    play_running_sound()

def stop_timer():
    global current_timer, timer_running
    if timer_running:
        label.config(text="Timer stopped.", fg="red", font=("Arial", 16))
        window.after_cancel(timer_id)
        timer_running = False
        stop_button.config(state=tk.DISABLED)
        current_timer = None
        play_attention_sound()
        pygame.mixer.stop()

def countdown(seconds):
    global timer_id
    if seconds > 0:
        label.config(text=f"Time left: {format_time(seconds)}", fg="#008000", font=("Arial", 18, "bold"))
        timer_id = window.after(1000, countdown, seconds - 1)
    else:
        exercise, _ = current_timer
        display_message(exercise)
        play_alarm_sound()

def play_alarm_sound():
    alarm_sound = pygame.mixer.Sound("alarm.mp3")
    alarm_sound.play()


def display_message(exercise):
    global message_blinking
    message_label.config(text=f"{exercise} done!", fg="red", font=("Arial", 16, "bold"))
    message_blinking = True
    toggle_message(5)

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

def close_window():
    window.destroy()
    subprocess.Popen(["python", "main.py"])

def go_back_to_main_page():
    close_window()
    subprocess.Popen(["python", "main.py"])

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

buttons = []
for i, exercise in enumerate(workout_exercises):
    button = tk.Button(frame, text=exercise[0], font=("Times New Roman", 14, "bold"), bg="#008CBA", fg="white",
                       command=lambda exercise=exercise: start_timer(exercise))
    button.grid(row=i // 2, column=i % 2, pady=10, padx=10, sticky="nsew")
    buttons.append(button)

for i in range(2):
    frame.columnconfigure(i, weight=1)
    frame.rowconfigure(i, weight=1)

label = tk.Label(frame, text="", font=("Arial", 18, "bold"), fg="#008000")
label.grid(row=2, columnspan=2, pady=20)

stop_button = tk.Button(frame, text="Stop", font=("Arial", 14), state=tk.DISABLED, command=stop_timer, bg="#FF5733")
stop_button.grid(row=3, columnspan=2, pady=10)

back_button = tk.Button(frame, text="Back to Main Page", font=("Arial", 14), command=go_back_to_main_page, bg="#333")
back_button.grid(row=4, columnspan=2, pady=10)

message_label = tk.Label(frame, text="", font=("Arial", 16, "bold"), fg="white")
message_label.grid(row=5, columnspan=2, pady=20)

window.mainloop()
