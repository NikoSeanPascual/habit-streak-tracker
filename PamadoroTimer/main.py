import customtkinter as ctk
import winsound

# --- COLOR PALETTE ---
COLOR_WORK = "#FF5252"
COLOR_SHORT_BREAK = "#4CAF50"
COLOR_LONG_BREAK = "#2196F3"
COLOR_BG = "#1A1A1B"
COLOR_CARD = "#2A2A2B"
TEXT_MAIN = "#FFFFFF"
TEXT_MUTED = "#B0B0B0"
BTN_SECONDARY = "#3E3E42"

class PolishedPomodoro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nikodoro App")
        self.geometry("450x700")
        self.configure(fg_color=COLOR_BG)

        self.timer_running = False
        self.after_id = None
        self.sessions_completed = 0

        self.work_mins = ctk.IntVar(value=25)
        self.short_break_mins = ctk.IntVar(value=5)
        self.long_break_mins = ctk.IntVar(value=15)
        self.current_time_sec = self.work_mins.get() * 60
        self.current_phase = "Work"

        self.setup_ui()

    def setup_ui(self):
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.ontop_switch = ctk.CTkSwitch(
            self.top_frame, text="Keep on top",
            command=self.toggle_always_on_top,
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        )
        self.ontop_switch.pack(side="right")

        self.status_label = ctk.CTkLabel(
            self, text="READY TO WORK?",
            font=ctk.CTkFont(size=35, weight="bold"),
            text_color=COLOR_WORK
        )
        self.status_label.pack(pady=(20, 0))

        self.timer_label = ctk.CTkLabel(
            self, text="25:00",
            font=ctk.CTkFont(size=90, weight="bold"),
            text_color=TEXT_MAIN
        )
        self.timer_label.pack(pady=(0, 10))

        # --- Progress Bar (Higher contrast track) ---
        self.progress = ctk.CTkProgressBar(
            self, width=350, height=12,
            progress_color=COLOR_WORK, fg_color="#404040"
        )
        self.progress.set(0)
        self.progress.pack(pady=10)

        # --- Main Controls ---
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            self.btn_frame, text="START", command=self.toggle_timer,
            fg_color=COLOR_WORK, hover_color="#D32F2F",
            font=ctk.CTkFont(size=16, weight="bold"), width=140, height=45, corner_radius=10,
            text_color="#FFFFFF"
        )
        self.start_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = ctk.CTkButton(
            self.btn_frame, text="RESET", command=self.reset_timer,
            fg_color=BTN_SECONDARY, hover_color="#4E4E52",
            width=100, height=45, corner_radius=10,
            text_color=TEXT_MAIN
        )
        self.reset_btn.grid(row=0, column=1, padx=10)

        # --- Settings Card ---
        self.settings_card = ctk.CTkFrame(self, fg_color=COLOR_CARD, corner_radius=15)
        self.settings_card.pack(padx=30, pady=20, fill="both", expand=True)

        ctk.CTkLabel(self.settings_card, text="CUSTOMIZE DURATIONS",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=TEXT_MAIN).pack(pady=(15, 10))

        self.create_slider_setting("Work", self.work_mins, 1, 60, COLOR_WORK)
        self.create_slider_setting("Short Break", self.short_break_mins, 1, 30, COLOR_SHORT_BREAK)
        self.create_slider_setting("Long Break", self.long_break_mins, 1, 45, COLOR_LONG_BREAK)

        # --- Footer Stats ---
        self.stats_label = ctk.CTkLabel(
            self, text="Sessions Completed: 0",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED
        )
        self.stats_label.pack(pady=15)

    def create_slider_setting(self, label, variable, from_, to, accent):
        frame = ctk.CTkFrame(self.settings_card, fg_color="transparent")
        frame.pack(fill="x", padx=25, pady=8)

        lbl = ctk.CTkLabel(frame, text=f"{label}: {variable.get()}m",
                           font=ctk.CTkFont(size=12, weight="bold"),
                           text_color=TEXT_MAIN)
        lbl.pack(side="top", anchor="w")

        slider = ctk.CTkSlider(
            frame, from_=from_, to=to, variable=variable,
            button_color=accent, progress_color=accent,
            button_hover_color="#FFFFFF",
            command=lambda val: self.update_settings_ui(lbl, label, val)
        )
        slider.pack(fill="x", pady=(5, 0))

    def update_settings_ui(self, label_obj, name, value):
        label_obj.configure(text=f"{name}: {int(value)}m")
        if not self.timer_running:
            self.reset_timer()

    def toggle_always_on_top(self):
        self.attributes("-topmost", self.ontop_switch.get())

    def play_alert(self):
        try:
            winsound.Beep(1000, 500)
        except:
            pass

    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_btn.configure(text="PAUSE", fg_color="#555555")
            self.run_countdown()
        else:
            self.timer_running = False
            self.start_btn.configure(text="RESUME", fg_color=COLOR_WORK)
            if self.after_id:
                self.after_cancel(self.after_id)

    def run_countdown(self):
        if self.current_time_sec > 0:
            mins, secs = divmod(self.current_time_sec, 60)
            self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")

            total = self.get_current_phase_total()
            self.progress.set(1 - (self.current_time_sec / total))

            self.current_time_sec -= 1
            self.after_id = self.after(1000, self.run_countdown)
        else:
            self.play_alert()
            self.handle_phase_completion()

    def get_current_phase_total(self):
        if self.current_phase == "Work": return self.work_mins.get() * 60
        if self.current_phase == "Short Break": return self.short_break_mins.get() * 60
        return self.long_break_mins.get() * 60

    def handle_phase_completion(self):
        if self.current_phase == "Work":
            self.sessions_completed += 1
            self.stats_label.configure(text=f"Sessions Completed: {self.sessions_completed}")
            if self.sessions_completed % 4 == 0:
                self.set_phase("Long Break", COLOR_LONG_BREAK)
            else:
                self.set_phase("Short Break", COLOR_SHORT_BREAK)
        else:
            self.set_phase("Work", COLOR_WORK)
        self.run_countdown()

    def set_phase(self, phase_name, color):
        self.current_phase = phase_name
        self.current_time_sec = self.get_current_phase_total()
        self.status_label.configure(text=phase_name.upper(), text_color=color)
        self.progress.configure(progress_color=color)
        self.start_btn.configure(fg_color=color, text="START")
        self.timer_running = False

    def reset_timer(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.timer_running = False
        self.current_phase = "Work"
        self.current_time_sec = self.work_mins.get() * 60

        self.timer_label.configure(text=f"{self.work_mins.get()}:00")
        self.status_label.configure(text="READY TO WORK?", text_color=COLOR_WORK)
        self.progress.set(0)
        self.start_btn.configure(text="START", fg_color=COLOR_WORK)


if __name__ == "__main__":
    app = PolishedPomodoro()
    app.mainloop()