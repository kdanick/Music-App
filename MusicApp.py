import customtkinter as ctk
from tkinter import PhotoImage

class MusicPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Groove - Music Player")
        self.geometry("500x300")
        self.configure(padx=20, pady=20)

        # Display for current track
        self.track_label = ctk.CTkLabel(self, text="Now Playing: Track Name", font=("Arial", 18))
        self.track_label.pack(pady=(10, 20))

        # Control buttons (Play, Pause, Previous, Next)
        controls_frame = ctk.CTkFrame(self)
        controls_frame.pack(pady=(10, 20))

        self.prev_button = ctk.CTkButton(controls_frame, text="◄◄", command=self.previous_track)
        self.prev_button.grid(row=0, column=0, padx=10)

        self.play_button = ctk.CTkButton(controls_frame, text="Play", command=self.play_pause_track)
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = ctk.CTkButton(controls_frame, text="Pause", command=self.pause_track)
        self.pause_button.grid(row=0, column=2, padx=10)

        self.next_button = ctk.CTkButton(controls_frame, text="►►", command=self.next_track)
        self.next_button.grid(row=0, column=3, padx=10)

        # Volume control
        self.volume_label = ctk.CTkLabel(self, text="Volume", font=("Arial", 14))
        self.volume_label.pack(pady=(10, 5))

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.set_volume)
        self.volume_slider.pack()

        # Progress bar for track
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(pady=(20, 10))
        self.progress_bar.set(0.3)  # Example progress (30%)

    # Placeholder methods for button actions
    def play_pause_track(self):
        print("Play/Pause Track")

    def pause_track(self):
        print("Pause Track")

    def next_track(self):
        print("Next Track")

    def previous_track(self):
        print("Previous Track")

    def set_volume(self, value):
        print(f"Volume set to {value}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MusicPlayer()
    app.mainloop()
