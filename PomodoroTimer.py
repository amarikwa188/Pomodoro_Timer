import sys

from tkinter import Tk
from tkinter.ttk import Notebook, Frame, Label, Button
import time
import threading

from pomodoro_settings import Settings

from typing import Callable

class Pomodoro:
    """
    Represents an instance of the pomodoro timer application.
    """
    def __init__(self, p_time, s_time, l_time) -> None:
        """
        Initializes an instance of the timer.
        
        :param p_time: the duration of the pomodoro timer
        :param s_time: the duration of the short break
        :param l_time: the duration of the long break
        """
        self.root: Tk = Tk()
        self.root.geometry("400x200+430+200")
        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False)
        self.TIMER_FONT: tuple = ("Helvetica", 40)
        self.COUNTER_FONT: tuple = ("Helvetica", 10)

        self.notebook: Notebook = Notebook(self.root)

        self.pomodoro_tab: Frame = Frame(self.notebook)
        self.short_break_tab: Frame = Frame(self.notebook)
        self.long_break_tab: Frame = Frame(self.notebook)

        self.notebook.add(self.pomodoro_tab, text="Pomodoro")
        self.notebook.add(self.short_break_tab, text="Short Break")
        self.notebook.add(self.long_break_tab, text="Long Break")

        self.notebook.pack(expand=1, fill="both")

        self.pomodoros: int = 0

        # pomodoro tab
        self.p_time: int = p_time # minutes
        self.p_timer_text: Label = Label(self.pomodoro_tab, text=f"{p_time:02d}:00", font=self.TIMER_FONT)
        self.p_timer_text.place(relx=0.5, rely=0.3, anchor="center")

        self.p_skip_button: Button = Button(self.pomodoro_tab, text="Skip", command=self.skip('p'))
        self.p_skip_button.place(relx=0.5, rely=0.63, anchor="center")

        self.p_reset_button: Button = Button(self.pomodoro_tab, text="Reset", command=self.reset('p'))
        self.p_reset_button.place(relx=0.9, rely=0.9, anchor="center")

        self.pomodoro_counter: Label = Label(self.pomodoro_tab, text=f"Pomodoros: {self.pomodoros}", font=self.COUNTER_FONT)
        self.pomodoro_counter.place(relx=0.12, rely=0.92, anchor="center")

        self.p_running: bool = False
        self.p_current_time: int = self.p_time * 60

        # short break
        self.s_time: int = s_time
        self.s_timer_text: Label = Label(self.short_break_tab, text=f"{s_time}:00", font=self.TIMER_FONT)
        self.s_timer_text.place(relx=0.5, rely=0.3, anchor="center")

        self.s_skip_button: Button = Button(self.short_break_tab, text="Skip", command=self.skip('s'))
        self.s_skip_button.place(relx=0.5, rely=0.63, anchor="center")

        self.s_reset_button: Button = Button(self.short_break_tab, text="Reset", command=self.reset('s'))
        self.s_reset_button.place(relx=0.9, rely=0.9, anchor="center")

        self.s_pomodoro_counter: Label = Label(self.short_break_tab, text=f"Pomodoros: {self.pomodoros}", font=self.COUNTER_FONT)
        self.s_pomodoro_counter.place(relx=0.12, rely=0.92, anchor="center")

        self.s_running: bool = False
        self.s_current_time: int = self.s_time * 60

        # long break
        self.l_time: int = l_time
        self.l_timer_text: Label = Label(self.long_break_tab, text=f"{l_time:02d}:00", font=self.TIMER_FONT)
        self.l_timer_text.place(relx=0.5, rely=0.3, anchor="center")

        self.l_skip_button: Button = Button(self.long_break_tab, text="Skip", command=self.skip('l'))
        self.l_skip_button.place(relx=0.5, rely=0.63, anchor="center")

        self.l_reset_button: Button = Button(self.long_break_tab, text="Reset", command=self.reset('l'))
        self.l_reset_button.place(relx=0.9, rely=0.9, anchor="center")

        self.l_pomodoro_counter: Label = Label(self.long_break_tab, text=f"Pomodoros: {self.pomodoros}", font=self.COUNTER_FONT)
        self.l_pomodoro_counter.place(relx=0.12, rely=0.92, anchor="center")

        self.l_running: bool = False
        self.l_current_time: int = self.l_time * 60

        self.start_timer('p')()

        self.root.mainloop()


    def start_timer(self, tab: str) -> Callable:
        """
        Starts the appropriate timer.
        
        :param tab: the current timer tab
        :return: a function which starts the timer of the given tab
        """
        def inner():
            if tab == 'p':
                if self.p_running:
                    self.p_running = False
                else:
                    thread = threading.Thread(target=self.start(tab))
                    self.p_running = True
                    thread.start()
            elif tab == 's':
                if self.s_running:
                    self.s_running = False
                else:
                    thread = threading.Thread(target=self.start(tab))
                    self.s_running = True
                    thread.start()
            else:
                if self.l_running:
                    self.l_running = False
                else:
                    thread = threading.Thread(target=self.start(tab))
                    self.l_running = True
                    thread.start()

        return inner
    

    def start(self, tab: str) -> Callable:
        """
        Handles the timer countdown.

        :param tab: the current timer tab
        :return: a function which reduces the timer of the given tab
        """
        def inner():
            if tab == 'p':
                total_seconds: int = self.p_current_time
                while total_seconds > 0 and self.p_running:
                    minutes, seconds = divmod(total_seconds, 60)
                    self.p_timer_text.config(text=f"{minutes:02d}:{seconds:02d}")
                    total_seconds -= 1
                    self.root.update()
                    self.p_current_time = total_seconds
                    time.sleep(1)

                if total_seconds == 0:
                    self.switch(tab)
            elif tab == 's':
                total_seconds: int = self.s_current_time
                while total_seconds > 0 and self.s_running:
                    minutes, seconds = divmod(total_seconds, 60)
                    self.s_timer_text.config(text=f"{minutes:02d}:{seconds:02d}")
                    total_seconds -= 1
                    self.root.update()
                    self.s_current_time = total_seconds
                    time.sleep(1)

                if total_seconds == 0:
                    self.switch(tab)    
            elif tab == 'l':
                total_seconds: int = self.l_current_time
                while total_seconds > 0 and self.l_running:
                    minutes, seconds = divmod(total_seconds, 60)
                    self.l_timer_text.config(text=f"{minutes:02d}:{seconds:02d}")
                    total_seconds -= 1
                    self.root.update()
                    self.l_current_time = total_seconds
                    time.sleep(1)

                if total_seconds == 0:
                    self.switch(tab)

        return inner


    def skip(self, tab: str) -> Callable:
        """
        Skips to the next timer.

        :param tab: the current timer tab
        :return: a function which skips the timer of the given tab
        """
        time.sleep(1)

        def inner():
            if tab == 'p' and self.p_running: 
                self.switch(tab)
            elif tab == 's' and self.s_running:
                self.switch(tab)
            elif tab == 'l' and self.l_running:
                self.switch(tab)

        return inner
    

    def switch(self, tab: str) -> None:
        """
        Handles the switching of tabs

        :param tab: the current timer tab
        """
        if tab == 'p':
            self.pomodoros += 1
            self.pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")
            self.s_pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")
            self.l_pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")

            if self.pomodoros % 4 == 0:
                # switch to long break
                self.reset_timer(tab)
                self.root.update()
                self.notebook.select(self.long_break_tab)
                self.start_timer('l')()
            else:
                # switch to short break
                self.reset_timer(tab)
                self.root.update()
                self.notebook.select(self.short_break_tab)
                self.start_timer('s')()

        else:
            self.reset_timer(tab)
            self.root.update()
            self.notebook.select(self.pomodoro_tab)
            self.start_timer('p')()


    def reset(self, tab: str) -> Callable:
        """
        Resets the entire timer.

        :param tab: the current timer tab
        :return: a function which resets the given timer and entire application
        """
        def inner():
            if self.p_running:
                self.reset_timer('p')
            elif self.s_running:
                self.reset_timer('s')
            elif self.l_running:
                self.reset_timer('l')
            
            self.notebook.select(self.pomodoro_tab)
            self.pomodoros = 0
            self.pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")
            self.s_pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")
            self.l_pomodoro_counter.config(text=f"Pomodoros: {self.pomodoros}")
            time.sleep(1)
            self.start_timer('p')()
                 
        return inner

    
    def reset_timer(self, tab: str) -> None:
        """
        Resets a specific tab's timer

        :param tab: the current timer tab
        """
        if tab == 'p':
            self.p_running = False
            self.p_current_time = self.p_time * 60
            self.p_timer_text.config(text=f"{self.p_time:02d}:00")
        elif tab == 's':
            self.s_running = False
            self.s_current_time = self.s_time * 60
            self.s_timer_text.config(text=f"{self.s_time:02d}:00")
        elif tab == 'l':
            self.l_running = False
            self.l_current_time = self.l_time * 60
            self.l_timer_text.config(text=f"{self.l_time:02d}:00")
            
    
if __name__ == "__main__":
    # initialize settings object
    settings = Settings()

    # gather timer durations from settings
    pomodoro: int = settings.pomodoro_time
    short: int = settings.short_time
    long: int = settings.long_time

    # settings window is closed, end program
    if pomodoro == 0:
        sys.exit()

    # create timer instance with appropriate durations
    pom: Pomodoro = Pomodoro(pomodoro, short, long)
    pom.p_running = False
    pom.s_running = False
    pom.l_running = False
    