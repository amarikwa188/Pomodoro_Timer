import json

import tkinter as tk
from tkinter import ttk

class Settings:
    def __init__(self) -> None:
        """
        Inititalises an instance of the settings window.
        """
        self.root = tk.Tk()
        self.root.geometry("210x160+520+200")
        self.root.title("Set Timers")
        self.root.resizable(False, False)
        self.FONT = ("Helvetica", 12)
        self.SPINBOX_FONT = ("Helvetica", 10)

        try:
            with open("pomodoro_settings_data.json", "r") as file:
                settings = json.load(file)
                self.pomodoro_setting = settings[0]
                self.short_setting = settings[1]
                self.long_setting = settings[2]
                
        except FileNotFoundError:
            self.pomodoro_setting = 25
            self.short_setting = 5
            self.long_setting = 15

        self.prompt_text = ttk.Label(self.root, text="Set prefered times:")
        self.prompt_text.grid(row=0, column=0, padx=5, pady=5) 

        self.pomodoro_text = ttk.Label(self.root, text="Pomodoro",
                                       font=self.FONT)
        self.pomodoro_text.grid(row=1, column=0, padx=5, pady=5, sticky="NWSE")

        var = tk.DoubleVar(value=self.pomodoro_setting)
        self.pomodoro_set = tk.Spinbox(self.root, from_=5, to=60,
                                       state="readonly", textvariable=var,
                                       font=self.SPINBOX_FONT, width=10,
                                       relief="sunken", increment=5)
        self.pomodoro_set.grid(row=1, column=1, pady=5)

        self.short_text = ttk.Label(self.root, text="Short Break", font=self.FONT)
        self.short_text.grid(row=2, column=0, padx=5, pady=5, sticky="NSWE")

        var = tk.DoubleVar(value=self.short_setting)
        self.short_set = tk.Spinbox(self.root, from_=5, to=59,
                                    state="readonly", textvariable=var,
                                    font=self.SPINBOX_FONT, width=10,
                                    relief="sunken")
        self.short_set.grid(row=2, column=1, padx=5, pady=5)

        self.long_text = ttk.Label(self.root, text="Long Break", font=self.FONT)
        self.long_text.grid(row=3, column=0, padx=5, pady=5, sticky="NSWE")

        var = tk.DoubleVar(value=self.long_setting)
        self.long_set = tk.Spinbox(self.root, from_=5, to=59,
                                    state="readonly", textvariable=var,
                                    font=self.SPINBOX_FONT, width=10,
                                    relief="sunken")
        self.long_set.grid(row=3, column=1, padx=5, pady=5)

        self.start_button = ttk.Button(self.root, text="Start", command=self.initiate)
        self.start_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="WE")

        self.pomodoro_time = 0
        self.short_time = 0
        self.long_time = 0

        self.root.mainloop()

    def initiate(self) -> None:
        """
        Sets the timer configurations and saves them to a JSON file.
        """
        self.pomodoro_time = int(self.pomodoro_set.get())
        self.short_time = int(self.short_set.get())
        self.long_time = int(self.long_set.get())

        with open("pomodoro_settings_data.json", "w") as file:
            json.dump([self.pomodoro_time, self.short_time, self.long_time], file)

        self.root.destroy()
