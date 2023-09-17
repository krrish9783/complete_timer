import tkinter as tk
import pygame
import subprocess
from tkinter import simpledialog

pygame.init()

window = tk.Tk()
window.title("Study Timer")

window.geometry("1912x1010")

frame = tk.Frame(window, padx=20, pady=20)
frame.pack(expand=True, fill='both')

study_sessions = [
    ("Reading", 1),
    ("Coding", 1),
    ("Writing", 1),
    ("Other", 1),
]

attention_sound = pygame.mixer.Sound("alarm.mp3")

current_timer = None
timer_running = False
message_blinking = False

coding_sound_channel = None
alarm_sound_channel = None


coding_session_active = False

def start_timer(session, time=None):
    global current_timer, timer_running
    if timer_running:
        stop_timer()
    if time is None:
        custom_time = simpledialog.askinteger("Custom Time", f"Enter custom time in minutes for {session}:")
        if custom_time is not None:
            time = custom_time
        else:
            return
    current_timer = (session, time)
    label.config(text=f"Study: {session}\nTime: {format_time(time)}", font=("Arial", 16, "bold"))
    countdown(time * 60)
    timer_running = True
    stop_button.config(state=tk.NORMAL)
    hide_message()
    if session == "Coding":
        play_coding_sound()

def stop_timer():
    global current_timer, timer_running
    if timer_running:
        label.config(text="Timer stopped.", font=("Arial", 16))
        window.after_cancel(timer_id)
        timer_running = False
        stop_button.config(state=tk.DISABLED)
        current_timer = None
        if coding_session_active:
            stop_coding_sound()
        else:
            stop_voice_sound()
        pygame.mixer.stop()

def countdown(seconds):
    global timer_id
    if seconds > 0:
        label.config(text=f"Time left: {format_time(seconds)}", font=("Times New Roman", 18, "bold"))
        timer_id = window.after(1000, countdown, seconds - 1)
    else:
        session, _ = current_timer
        display_message(session)
        if session == "Coding":
            stop_coding_sound()
        play_alarm_sound()

def display_message(session):
    global message_blinking
    message_label.config(text=f"{session} complete!", font=("Arial", 16, "bold"))
    message_blinking = True
    toggle_message(5)

def toggle_message(count):
    global message_blinking
    if count > 0:
        if message_label.cget("fg") == "black":
            message_label.config(fg="white")
        else:
            message_label.config(fg="black")
        window.after(500, toggle_message, count - 1)
    else:
        message_label.config(fg="black")
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

def play_coding_sound():
    global coding_sound_channel, coding_session_active
    coding_sound_channel = pygame.mixer.Sound("coding.mp3").play(-1)
    coding_session_active = True

def stop_coding_sound():
    global coding_sound_channel, coding_session_active
    if coding_sound_channel is not None:
        pygame.mixer.stop()
        coding_session_active = False

def play_alarm_sound():
    global alarm_sound_channel
    alarm_sound_channel = attention_sound.play()

def stop_voice_sound():
    global voice_sound_channel
    if voice_sound_channel is not None:
        pygame.mixer.stop()

def close_window():
    window.destroy()
    subprocess.Popen(["python", "main.py"])

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def set_custom_time():
    global study_sessions
    custom_time = simpledialog.askinteger("Custom Time", "Enter custom time in minutes:")
    if custom_time is not None:
        for i, (session, _) in enumerate(study_sessions):
            study_sessions[i] = (session, custom_time)

buttons = []
for session, _ in study_sessions:
    button = tk.Button(frame, text=session, width=10, font=("Arial", 14, "bold"), bg="white", fg="black", activebackground="lime",
                       command=lambda session=session: start_timer(session))
    button.pack(pady=10, expand=True, fill='both')
    buttons.append(button)

label = tk.Label(frame, text="", font=("Arial", 18, "bold"))
label.pack(pady=20)

stop_button = tk.Button(frame, text="Stop", font=("Arial", 14), state=tk.DISABLED, width=10, bg="white", fg="black", activebackground="red",
                       command=stop_timer)
stop_button.pack(pady=10, expand=True, fill='both')


back_button = tk.Button(frame, text="Back to Main Page", font=("Arial", 14), width=15, bg="white", fg="black", activebackground="#333",
                        command=close_window)
back_button.pack(pady=10, expand=True, fill='both')

message_label = tk.Label(frame, text="", font=("Arial", 16, "bold"))
message_label.pack(pady=20)

window.mainloop()
