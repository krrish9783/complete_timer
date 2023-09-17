import tkinter as tk
import pygame
import subprocess
from tkinter import simpledialog

pygame.init()

window = tk.Tk()
window.title("Meditation Timer")

window.geometry("1912x1010")
window.eval('tk::PlaceWindow . center')

frame = tk.Frame(window, bg="#f5f5f5")
frame.pack(expand=True, fill='both')

meditation_exercises = [
    ("Deep Breathing", 1),
    ("Body Scan", 1),
    ("Guided Meditation", 1),
    ("Sleeping", None),
]

meditation_sound = pygame.mixer.Sound("med.mp3")
sleeping_sound = pygame.mixer.Sound("sleeping.mp3")
attention_sound = pygame.mixer.Sound("attention.mp3")
alarm_sound = pygame.mixer.Sound("alarm.mp3")

current_timer = None
timer_running = False
message_blinking = False

meditation_sound_channel = None
attention_sound_channel = None

alarm_scheduled = None

def get_duration(exercise):

    while True:
        duration = simpledialog.askinteger("Set Exercise Duration", f"Enter duration for {exercise[0]} (in minutes):")
        if duration is not None:
            return duration

def start_timer(exercise, time):
    global current_timer, timer_running, alarm_scheduled
    if timer_running:
        stop_timer()
    current_timer = (exercise, time)
    label.config(text=f"Meditation: {exercise}\nTime: {format_time(time * 60)}", fg="#333", font=("Arial", 16, "bold"))
    countdown(time * 60)
    timer_running = True
    stop_button.config(state=tk.NORMAL)
    hide_message()
    if exercise == "Sleeping":
        play_sleeping_sound()
        alarm_scheduled = window.after(time * 60 * 1000, play_alarm_sound)
    else:
        play_meditation_sound()

def stop_timer():
    global current_timer, timer_running, alarm_scheduled
    if timer_running:
        label.config(text="Timer stopped.", fg="red", font=("Arial", 16))
        window.after_cancel(timer_id)
        timer_running = False
        stop_button.config(state=tk.DISABLED)
        if current_timer[0] == "Sleeping":
            if alarm_scheduled is not None:
                window.after_cancel(alarm_scheduled)
            play_alarm_sound()
        else:
            play_attention_sound()
        current_timer = None
        pygame.mixer.stop()
        alarm_scheduled = None

def countdown(seconds):
    global timer_id
    if seconds > 0:
        label.config(text=f"Time left: {format_time(seconds)}", fg="#008000", font=("Arial", 18, "bold"))
        timer_id = window.after(1000, countdown, seconds - 1)
    else:
        exercise, _ = current_timer
        display_message(exercise)

def display_message(exercise):
    global message_blinking
    message_label.config(text=f"{exercise} complete!", fg="red", font=("Arial", 16, "bold"))
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

def play_meditation_sound():
    global meditation_sound_channel
    meditation_sound_channel = meditation_sound.play()

def play_sleeping_sound():
    global meditation_sound_channel
    meditation_sound_channel = sleeping_sound.play()

def play_attention_sound():
    global attention_sound_channel
    attention_sound_channel = attention_sound.play()

def play_alarm_sound():
    global meditation_sound_channel
    meditation_sound_channel = alarm_sound.play()

def close_window():
    window.destroy()
    subprocess.Popen(["python", "main.py"])

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

buttons = []
for exercise, time in meditation_exercises:
    button = tk.Button(frame, text=exercise, font=("Arial", 14, "bold"), bg="#008CBA", fg="white",
                       command=lambda exercise=exercise, time=time: start_timer(exercise, get_duration((exercise, time))))
    button.pack(pady=10, expand=True, fill='both')
    buttons.append(button)

label = tk.Label(frame, text="", font=("Arial", 18, "bold"), fg="#008000")
label.pack(pady=20)

stop_button = tk.Button(frame, text="Stop", font=("Arial", 14), state=tk.DISABLED, command=stop_timer, bg="#FF5733")
stop_button.pack(pady=10, expand=True, fill='both')

back_button = tk.Button(frame, text="Back to Main Page", font=("Arial", 14), command=close_window, bg="#333")
back_button.pack(pady=10, expand=True, fill='both')

message_label = tk.Label(frame, text="", font=("Arial", 16, "bold"), fg="white")
message_label.pack(pady=20)

window.mainloop()
