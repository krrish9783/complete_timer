import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Krishna@123",
            database="log"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE user = %s AND pass = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            connection.close()
            root.destroy()
            import tkinter as tk
            from PIL import Image, ImageTk
            import itertools
            import subprocess
            def show_main_window():
                main_window.deiconify()
            if 'main_window' not in globals():
                main_window = tk.Tk()
                main_window.title("Countdown Timer")
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
                    subprocess.Popen(["python", page_script])
                cooking_button = tk.Button(frame, text="Cooking", width=button_width, height=button_height,
                                           font=button_font, command=lambda: open_page("cooking.py"))
                cooking_button.config(bg="white", fg="red")
                workout_button = tk.Button(frame, text="Workout", width=button_width, height=button_height,
                                           font=button_font, command=lambda: open_page("workout.py"))
                workout_button.config(bg="green", fg="white")
                meditation_button = tk.Button(frame, text="Meditation", width=button_width, height=button_height,
                                              font=button_font, command=lambda: open_page("meditation.py"))
                meditation_button.config(bg="blue", fg="white")
                study_button = tk.Button(frame, text="Study", width=button_width, height=button_height,
                                         font=button_font, command=lambda: open_page("study.py"))
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
                developer_label = tk.Label(main_window, text="Developer: Kishnu Yadav", font=("Arial", 14), fg="gray")
                developer_label.pack(pady=10)
            main_window.mainloop()
        else:
            login_status.config(text="Invalid username or password")
    except Exception as e:
        login_status.config(text="Error connecting to the database")

def clear_inputs():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    login_status.config(text="")

root = tk.Tk()
root.geometry("800x300")
root.title("Login Page")

grid = tk.Frame(root)
grid.pack()

custom_font = ("Arial", 20)

username_label = ttk.Label(grid, text="Username:", font=custom_font)
username_entry = ttk.Entry(grid, font=custom_font)
username_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
username_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

password_label = ttk.Label(grid, text="Password:", font=custom_font)
password_entry = ttk.Entry(grid, show='*', font=custom_font)
password_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
password_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

login_button = ttk.Button(grid, text="Login", command=validate_login, style="TButton")
clear_button = ttk.Button(grid, text="Clear", command=clear_inputs, style="TButton")
login_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
clear_button.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

login_status = ttk.Label(grid, text="", font=custom_font)
login_status.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

grid.grid_columnconfigure(0, weight=1)
grid.grid_columnconfigure(1, weight=2)
grid.grid_rowconfigure(0, weight=1)
grid.grid_rowconfigure(1, weight=1)
grid.grid_rowconfigure(2, weight=1)
grid.grid_rowconfigure(3, weight=1)
grid.grid_rowconfigure(4, weight=1)

style = ttk.Style()
style.configure("TButton",
                font=custom_font,
                padding=(10, 10),
                foreground="white",
                background="green",
                relief="flat")

style.map("TButton",
          foreground=[("active", "white")],
          background=[("active", "red")])

root.mainloop()
