import customtkinter as ctk

class ControlsFrame(ctk.CTkFrame):
    def __init__(self, master=None, update_timer_callback=None):
        super().__init__(master)
        self.update_timer_callback = update_timer_callback

        # Timer Labels
        self.current_time_label = ctk.CTkLabel(self, text="00:00", font=("Arial", 14))
        self.current_time_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

        self.total_time_label = ctk.CTkLabel(self, text="00:00", font=("Arial", 14))
        self.total_time_label.grid(row=0, column=6, padx=(5, 10), sticky="e")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=0, column=1, columnspan=5, sticky="ew", pady=(10, 0))

        # Control buttons
        self.create_control_buttons()

    def create_control_buttons(self):
        prev_button = ctk.CTkButton(self, text="◄◄", command=lambda: print("Previous Track"), width=50)
        prev_button.grid(row=1, column=1, padx=5, pady=20)

        self.play_pause_button = ctk.CTkButton(self, text="▶ Play", command=self.toggle_play_pause, height=40)
        self.play_pause_button.grid(row=1, column=2, padx=5, pady=20)

        next_button = ctk.CTkButton(self, text="►►", command=lambda: print("Next Track"), width=50)
        next_button.grid(row=1, column=3, padx=5, pady=20)

        # Volume control
        volume_label = ctk.CTkLabel(self, text="Volume", font=("Arial", 14))
        volume_label.grid(row=1, column=4, padx=(10, 5))

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, command=lambda value: print(f"Volume set to {value}"))
        self.volume_slider.grid(row=1, column=5, padx=(0, 10), sticky="ew")
        self.volume_slider.configure(width=150)

    def toggle_play_pause(self):
        global is_playing
        is_playing = not is_playing
        if is_playing:
            self.play_pause_button.configure(text="❚❚ Pause")
            print("Playing track...")
            self.update_timer_callback()
        else:
            self.play_pause_button.configure(text="▶ Play")
            print("Paused track.")
