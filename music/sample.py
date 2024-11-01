import customtkinter as ctk
import time
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Initialize the main window
root = ctk.CTk()
root.title("Groove - Music Player")
root.geometry("800x610")
root.configure(padx=20, pady=20)

# MusicPlayer class definition
class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.track_list = ["MY POWER (Official Audio).mp3", "Rema-OZEBA.mp3", "Rihanna-Stay.mp3"]
        self.current_track_index = 0
        self.is_playing = False
        self.start_time = 0

        self.track_label = ctk.CTkLabel(master, text="No track playing", font=("Arial", 18))
        self.track_label.pack(pady=(10, 20))

        self.play_button = ctk.CTkButton(master, text="▶ Play", command=self.toggle_play_pause)
        self.play_button.pack()

        self.back_button = ctk.CTkButton(master, text="◄◄", command=self.previous_track)
        self.back_button.pack()

        self.next_button = ctk.CTkButton(master, text="►►", command=self.next_track)
        self.next_button.pack()

        self.current_time_label = ctk.CTkLabel(master, text="00:00", font=("Arial", 14))
        self.current_time_label.pack(side='left')

        self.total_time_label = ctk.CTkLabel(master, text="00:00", font=("Arial", 14))
        self.total_time_label.pack(side='right')

        self.progress_bar = ctk.CTkProgressBar(master)
        self.progress_bar.pack(fill='x', pady=(10, 0))

        self.volume_slider = ctk.CTkSlider(master, from_=0, to=100, command=self.set_volume)
        self.volume_slider.pack(pady=(10, 0))

        self.create_scrolling_text()

    def create_scrolling_text(self):
        self.track_name = self.track_list[self.current_track_index]
        self.scrolling_text = self.track_name + "   "
        self.scroll_pos = 0
        self.label_width = 25
        self.direction = 1
        self.track_label.configure(text=self.scrolling_text[self.scroll_pos:self.scroll_pos + self.label_width])
        self.update_scrolling_text()

    def update_scrolling_text(self):
        self.track_label.configure(text=self.scrolling_text[self.scroll_pos:self.scroll_pos + self.label_width])
        self.scroll_pos += self.direction
        if self.scroll_pos >= len(self.scrolling_text) - self.label_width:
            self.direction = -1
        elif self.scroll_pos <= 0:
            self.direction = 1
        self.master.after(100, self.update_scrolling_text)

    def toggle_play_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.configure(text="▶ Play")
        else:
            if self.start_time == 0:
                self.load_track()
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_button.configure(text="❚❚ Pause")
            self.start_time = time.time() - (self.progress_bar.get() * self.get_track_duration())
            self.update_timer()

    def load_track(self):
        pygame.mixer.music.load(self.track_list[self.current_track_index])
        self.track_label.configure(text=f"Now Playing: {os.path.basename(self.track_list[self.current_track_index])}")

    def get_track_duration(self):
        return pygame.mixer.Sound(self.track_list[self.current_track_index]).get_length()

    def update_timer(self):
        if self.is_playing:
            elapsed_time = time.time() - self.start_time
            current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
            total_time = time.strftime("%M:%S", time.gmtime(self.get_track_duration()))
            self.current_time_label.configure(text=current_time)
            self.total_time_label.configure(text=total_time)

            if elapsed_time < self.get_track_duration():
                self.progress_bar.set(elapsed_time / self.get_track_duration())
                self.master.after(1000, self.update_timer)
            else:
                self.progress_bar.set(1.0)
                self.is_playing = False
                self.play_button.configure(text="▶ Play")

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.track_list)
        self.load_track()
        if self.is_playing:
            pygame.mixer.music.play()

    def previous_track(self):
        self.current_track_index = (self.current_track_index - 1) % len(self.track_list)
        self.load_track()
        if self.is_playing:
            pygame.mixer.music.play()

    def set_volume(self, value):
        volume = float(value) / 100  # Scale the value to be between 0 and 1
        pygame.mixer.music.set_volume(volume)

# Create and run the music player
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MusicPlayer(root)
    root.mainloop()
