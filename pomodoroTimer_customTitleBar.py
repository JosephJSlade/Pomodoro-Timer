import tkinter as tk

class CustomWindow:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove default title bar
        
        # Set the background color of the window
        self.root.config(bg="gray43")
        
        # Custom title bar frame
        self.title_bar = tk.Frame(root, bg="gray33", relief="raised", bd=2)
        self.title_bar.pack(side=tk.TOP, fill=tk.X)

        # Title bar label
        self.title_label = tk.Label(self.title_bar, text="Pomodoro Timer", bg="gray33", fg="white", font=("Helvetica", 12))
        self.title_label.pack(side=tk.LEFT, padx=10)

        # Close button
        self.close_button = tk.Button(self.title_bar, text="X", bg="brown4", fg="white", command=root.quit)
        self.close_button.pack(side=tk.RIGHT, padx=5)
        
        # Minimize button
        self.minimize_button = tk.Button(self.title_bar, text="_", bg="dark slate blue", fg="white", command=self.minimize)
        self.minimize_button.pack(side=tk.RIGHT, padx=5)

        # Make title bar draggable
        self.title_bar.bind("<B1-Motion>", self.move_window)

        # Content of the window
        self.app = PomodoroTimer(root)

    def minimize(self):
        self.root.iconify()

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root}+{event.y_root}')

class PomodoroTimer:
    def __init__(self, root):
        self.root = root

        # Timer settings
        self.work_duration = 25 * 60  # 25 minutes
        self.short_break_duration = 5 * 60  # 5 minutes
        self.long_break_duration = 30 * 60  # 30 minutes
        self.cycles = 0
        self.is_paused = False
        self.is_running = False
        self.current_time = 0

        # Main content frame
        self.content_frame = tk.Frame(root, bg="gray43")
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))  # Adjusted padding for custom title bar

        # Create GUI elements
        self.label = tk.Label(self.content_frame, text="Pomodoro Timer", font=("Helvetica", 24), bg="gray43")
        self.label.pack(pady=20)

        self.time_label = tk.Label(self.content_frame, text="00:00", font=("Helvetica", 48), bg="gray43")
        self.time_label.pack()

        self.cycle_label = tk.Label(self.content_frame, text="Cycle: 0", font=("Helvetica", 18), bg="gray43")
        self.cycle_label.pack(pady=10)

        # Buttons with custom background colors
        self.start_button = tk.Button(self.content_frame, text="Start", command=self.start_timer, bg="gray33", font=("Helvetica", 14))
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.pause_button = tk.Button(self.content_frame, text="Pause", command=self.pause_timer, bg="gray33", font=("Helvetica", 14), state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=20)

        self.reset_button = tk.Button(self.content_frame, text="Reset", command=self.reset_timer, bg="gray33", font=("Helvetica", 14))
        self.reset_button.pack(side=tk.LEFT, padx=20)

        self.resume_button = tk.Button(self.content_frame, text="Resume", command=self.resume_timer, bg="gray33", font=("Helvetica", 14), state=tk.DISABLED)
        self.resume_button.pack(side=tk.LEFT, padx=20)

    # Start the timer
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.cycles += 1
            self.current_time = self.work_duration
            self.update_timer()

    # Pause the timer
    def pause_timer(self):
        self.is_paused = True
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.NORMAL)

    # Resume the timer
    def resume_timer(self):
        self.is_paused = False
        self.resume_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.update_timer()

    # Reset the timer
    def reset_timer(self):
        self.is_running = False
        self.is_paused = False
        self.cycles = 0
        self.current_time = 0
        self.update_labels("00:00", "Cycle: 0")
        self.pause_button.config(state=tk.DISABLED)
        self.resume_button.config(state=tk.DISABLED)

    # Update the timer
    def update_timer(self):
        if not self.is_paused and self.is_running:
            minutes, seconds = divmod(self.current_time, 60)
            self.update_labels(f"{minutes:02d}:{seconds:02d}", f"Cycle: {self.cycles}")
            if self.current_time > 0:
                self.current_time -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_complete()

    # Timer complete logic
    def timer_complete(self):
        if self.cycles % 4 == 0:
            self.current_time = self.long_break_duration
            self.update_labels("Long Break", f"Cycle: {self.cycles}")
        else:
            self.current_time = self.short_break_duration
            self.update_labels("Short Break", f"Cycle: {self.cycles}")
        self.start_timer()

    # Update the GUI labels
    def update_labels(self, time_text, cycle_text):
        self.time_label.config(text=time_text)
        self.cycle_label.config(text=cycle_text)
        self.pause_button.config(state=tk.NORMAL)

# Main GUI loop
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomWindow(root)
    root.mainloop()
