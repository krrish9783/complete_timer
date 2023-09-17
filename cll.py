import tkinter as tk
from PIL import Image, ImageTk
import itertools
import subprocess

main_window = tk.Tk()
main_window.title("Countdown Timer")

def destroy_current_window():
    main_window.destroy()

main_window.geometry("1912x1010")
main_window.eval('tk::PlaceWindow . center')

background_images = ["workout.png", "cooking.png", "med1.png", "study.png"]

frame = tk.Frame(main_window)
frame.pack(expand=True, fill='both')

background_label = tk.Label(frame)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def update_background():
    for bg_image in itertools.cycle(background_images):
        img = Image.open(bg_image)
        photo = ImageTk.PhotoImage(img)
        background_label.configure(image=photo)
        background_label.image = photo
        main_window.update()
        main_window.after(1000)

main_window.after(0, update_background)

button_width = 20
button_height = 5
button_font = ('Helvetica', 14)

def open_page(page_script):
    destroy_current_window()
    subprocess.Popen(["python", page_script])

cooking_button = tk.Button(frame, text="Cooking", width=button_width, height=button_height, font=button_font, command=lambda: open_page("cooking.py"))
cooking_button.config(bg="white", fg="red")

workout_button = tk.Button(frame, text="Workout", width=button_width, height=button_height, font=button_font, command=lambda: open_page("workout.py"))
workout_button.config(bg="green", fg="white")

meditation_button = tk.Button(frame, text="Meditation", width=button_width, height=button_height, font=button_font, command=lambda: open_page("meditation.py"))
meditation_button.config(bg="blue", fg="white")

study_button = tk.Button(frame, text="Study", width=button_width, height=button_height, font=button_font, command=lambda: open_page("study.py"))
study_button.config(bg="white", fg="green")

def on_button_click(button):
    button.config(bg="lightgray", fg="black")
    main_window.after(1000, lambda: button.config(bg="red", fg="white"))

cooking_button.bind("<Button-1>", on_button_click)
workout_button.bind("<Button-1>", on_button_click)
meditation_button.bind("<Button-1>", on_button_click)
study_button.bind("<Button-1>", on_button_click)

cooking_button.grid(row=0, column=0, padx=5, pady=5)
workout_button.grid(row=0, column=1, padx=5, pady=5)
meditation_button.grid(row=1, column=0, padx=5, pady=5)
study_button.grid(row=1, column=1, padx=5, pady=5)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

main_window.mainloop()
