import customtkinter as ctk
import time
import pygame

pygame.mixer.init()

# Initialize the main window
root = ctk.CTk()
root.title("Groove - Music Player")
root.geometry("800x610")
root.configure(padx=20, pady=20)

# Total duration of the track
total_duration = 230  # Set this to the actual track duration in seconds

# Variable to track playback state
is_playing = False
start_time = 0

# Function to update timer labels
def update_timer():
    if is_playing:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        total_time = time.strftime("%M:%S", time.gmtime(total_duration))

        current_time_label.configure(text=current_time)
        total_time_label.configure(text=total_time)

        # Update the progress bar
        progress_bar.set(elapsed_time / total_duration)

        root.after(1000, update_timer)  # Call this function again after 1 second

def toggle_play_pause():
    global is_playing, start_time
    is_playing = not is_playing
    if is_playing:
        if start_time == 0:  # If this is a new play
            pygame.mixer.music.load("music/MY POWER (Official Audio).mp3")
            pygame.mixer.music.play(loops=0)
            start_time = time.time()  # Record the start time
            play_pause_button.configure(text="❚❚ Pause")
            update_timer()  # Start updating the timer
        else:
            pygame.mixer.music.unpause()  # Resume from the paused position
            play_pause_button.configure(text="❚❚ Pause")
            start_time = time.time() - (progress_bar.get() * total_duration)  # Adjust start time for resuming
            update_timer()  # Ensure timer updates on resume
    else:
        pygame.mixer.music.pause()  # Pause music
        play_pause_button.configure(text="▶ Play")  # Update button text to "Play"

def set_progress(event):
    new_value = (event.x / progress_bar.winfo_width())
    progress_bar.set(new_value)
    if is_playing:
        pygame.mixer.music.pause()  # Pause music to set position
        position = new_value * total_duration  # Calculate the new position in seconds
        pygame.mixer.music.play(start=position)  # Start playing from the new position
        global start_time
        start_time = time.time() - position  # Adjust start time
        update_timer()  # Update the timer display

# Create Sidebar Frame
def create_sidebar_frame():
    sidebar_frame = ctk.CTkFrame(root, width=200)
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=(0, 0))

    # Search bar
    search_bar = ctk.CTkEntry(sidebar_frame, placeholder_text="Search...", width=180)
    search_bar.pack(pady=(10, 10))

    # Sidebar buttons
    sidebar_buttons = [
        ("Recents", lambda: print("Recents clicked")),
        ("Music Library", lambda: print("Music Library clicked")),
        ("Favorites", lambda: print("Favorites clicked")),
        ("Play Queue", lambda: print("Play Queue clicked")),
        ("Playlists", lambda: print("Playlists clicked")),
    ]

    for text, command in sidebar_buttons:
        button = ctk.CTkButton(sidebar_frame, text=text, command=command, width=180)
        button.pack(pady=(5, 0))

    return sidebar_frame

# Create Visual Frame
def create_visual_frame():
    visual_frame = ctk.CTkFrame(root)
    visual_frame.grid(row=0, column=1, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)

    track_name = "Track Name"
    track_label = ctk.CTkLabel(visual_frame, text=f"Now Playing: {track_name}", font=("Arial", 18))
    track_label.pack(pady=(10, 20))

    return visual_frame

# Create Controls Frame
def create_controls_frame():
    controls_frame = ctk.CTkFrame(root)
    controls_frame.grid(row=1, column=0, columnspan=2, pady=(0, 0), sticky="ew")

    controls_frame.grid_columnconfigure(0, weight=1)
    controls_frame.grid_columnconfigure(1, weight=0)
    controls_frame.grid_columnconfigure(2, weight=0)
    controls_frame.grid_columnconfigure(3, weight=0)
    controls_frame.grid_columnconfigure(4, weight=0)
    controls_frame.grid_columnconfigure(5, weight=0)

    global current_time_label, total_time_label
    current_time_label = ctk.CTkLabel(controls_frame, text="00:00", font=("Arial", 14))
    current_time_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

    total_time_label = ctk.CTkLabel(controls_frame, text="00:00", font=("Arial", 14))
    total_time_label.grid(row=0, column=6, padx=(5, 10), sticky="e")

    global progress_bar
    progress_bar = ctk.CTkProgressBar(controls_frame)
    progress_bar.grid(row=0, column=1, columnspan=5, sticky="ew", pady=(10, 0))

    prev_button = ctk.CTkButton(controls_frame, text="◄◄", command=lambda: print("Previous Track"), width=50)
    prev_button.grid(row=1, column=1, padx=5, pady=20)

    global play_pause_button
    play_pause_button = ctk.CTkButton(controls_frame, text="▶ Play", command=toggle_play_pause, height=40)
    play_pause_button.grid(row=1, column=2, padx=5, pady=20)

    next_button = ctk.CTkButton(controls_frame, text="►►", command=lambda: print("Next Track"), width=50)
    next_button.grid(row=1, column=3, padx=5, pady=20)

    volume_label = ctk.CTkLabel(controls_frame, text="Volume", font=("Arial", 14))
    volume_label.grid(row=1, column=4, padx=(10, 5))

    volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=lambda value: print(f"Volume set to {value}"))
    volume_slider.grid(row=1, column=5, padx=(0, 10), sticky="ew")
    volume_slider.configure(width=150)

    return controls_frame

# Create frames
sidebar_frame = create_sidebar_frame()
visual_frame = create_visual_frame()
controls_frame = create_controls_frame()

# Bind mouse click to set progress
progress_bar.set(0)
progress_bar.bind("<Button-1>", set_progress)

# Start the timer
update_timer()

# Start the GUI main loop
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root.mainloop()
