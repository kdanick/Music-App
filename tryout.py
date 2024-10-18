import customtkinter as ctk
import time
import pygame

pygame.mixer.init()

# Initialize the main window
root = ctk.CTk()
root.title("Groove - Music Player")
root.geometry("800x610")
root.configure(padx=20, pady=20)

# Variable to track playback state
is_playing = False
start_time = 0

track_name = "MY POWER (Official Audio).mp3"

scrolling_text = track_name + "   "  # Add space to loop back smoothly
scroll_pos = 0  # Current position of the scrolling text
direction = 1  # 1 for right, -1 for left
label_width = 25  # Number of characters to display at a time
space_padding = 5  # Additional space on each side

# Load the audio file to get its duration
sound = pygame.mixer.Sound(f"music/{track_name}")
total_duration = sound.get_length()

def update_timer():
    global is_playing  # Ensure we are referring to the global is_playing variable
    if is_playing:
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        total_time = time.strftime("%M:%S", time.gmtime(total_duration))  # Display the total track duration

        current_time_label.configure(text=current_time)
        total_time_label.configure(text=total_time)  # Always show total time

        if elapsed_time < total_duration:
            progress_bar.set(elapsed_time / total_duration)
            root.after(1000, update_timer)  # Update every second
        else:
            progress_bar.set(1.0)
            is_playing = False
            play_pause_button.configure(text="▶ Play")


def update_scrolling_text():
    global scroll_pos, direction

    # Get the substring to display
    display_text = scrolling_text[scroll_pos:scroll_pos + label_width]
    track_label.configure(text=display_text)  # Update the label with the current text

    # Update scroll position based on direction
    scroll_pos += direction

    # Check bounds to reverse direction if necessary
    if scroll_pos >= len(scrolling_text) - label_width:
        direction = -1  # Change direction to left
    elif scroll_pos <= 0:
        direction = 1  # Change direction to right

    root.after(550, update_scrolling_text)

def toggle_play_pause():
    global is_playing, start_time
    is_playing = not is_playing

    if is_playing:
        if start_time == 0:  # New play
            pygame.mixer.music.load(f"music/{track_name}")
            pygame.mixer.music.play(loops=0)
            start_time = time.time()  # Record the start time
            play_pause_button.configure(text="❚❚ Pause")
            update_timer()  # Start updating the timer
        else:  # Resume from pause
            pygame.mixer.music.unpause()
            play_pause_button.configure(text="❚❚ Pause")
            start_time = time.time() - (progress_bar.get() * total_duration)  # Adjust for resuming
            update_timer()  # Resume timer updates
    else:  # Pause the music
        pygame.mixer.music.pause()
        play_pause_button.configure(text="▶ Play")


def set_progress(event):
    new_value = (event.x / progress_bar.winfo_width())  # Get the new progress percentage
    progress_bar.set(new_value)

    position = new_value * total_duration  # Calculate the new position in seconds

    # Pause to set the position
    pygame.mixer.music.pause()
    pygame.mixer.music.set_pos(position)  # Set the position in the track

    # Adjust the start_time to continue from the new position
    global start_time
    start_time = time.time() - position  # Adjust start time for resuming

    # Resume if the music was playing
    if is_playing:
        pygame.mixer.music.unpause()
        update_timer()  # Update the timer immediately

def set_volume(value):
    volume = float(value) / 100  # Scale the value to be between 0 and 1
    pygame.mixer.music.set_volume(volume)

# Connect this to the volume slider command
volume_slider = ctk.CTkSlider(root, from_=0, to=100, command=set_volume)


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

    track_label = ctk.CTkLabel(visual_frame, text=f"Now Playing: {track_name}", font=("Arial", 18))
    track_label.pack(pady=(10, 20))

    return visual_frame

# Create Controls Frame
def create_controls_frame():
    controls_frame = ctk.CTkFrame(root)
    controls_frame.grid(row=1, column=0, columnspan=2, pady=(0, 0), sticky="ew")

    controls_frame.grid_columnconfigure(0, weight=0)
    controls_frame.grid_columnconfigure(1, weight=0)
    controls_frame.grid_columnconfigure(2, weight=1)
    controls_frame.grid_columnconfigure(3, weight=0)
    controls_frame.grid_columnconfigure(4, weight=0)
    controls_frame.grid_columnconfigure(5, weight=0)
    controls_frame.grid_columnconfigure(6, weight=1)
    controls_frame.grid_columnconfigure(7, weight=1)
    controls_frame.grid_columnconfigure(8, weight=0)

    global current_time_label, total_time_label, track_label  # Declare track_label as global
    current_time_label = ctk.CTkLabel(controls_frame, text="00:00", font=("Arial", 14))
    current_time_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

    total_time_label = ctk.CTkLabel(controls_frame, text="00:00", font=("Arial", 14))
    total_time_label.grid(row=0, column=8, padx=(5, 10), sticky="e")

    global progress_bar
    progress_bar = ctk.CTkProgressBar(controls_frame)
    progress_bar.grid(row=0, column=0, columnspan=8, sticky="ew", pady=(10, 0), padx=(60,10))

    # Create a frame to contain the marquee
    marquee_frame = ctk.CTkFrame(controls_frame, width=300)  # Adjust width and height as needed
    marquee_frame.grid(row=1, column=7, columnspan=2, sticky="ew", padx=10)

    track_label = ctk.CTkLabel(marquee_frame, text="", font=("Arial", 14))
    track_label.pack(pady=10, fill='x')  # Use pack for better positioning

    prev_button = ctk.CTkButton(controls_frame, text="◄◄", command=lambda: print("Previous Track"), width=50)
    prev_button.grid(row=1, column=3, padx=(10, 5), pady=20)

    global play_pause_button
    play_pause_button = ctk.CTkButton(controls_frame, text="▶ Play", command=toggle_play_pause, height=40)
    play_pause_button.grid(row=1, column=4, padx=5, pady=20)

    next_button = ctk.CTkButton(controls_frame, text="►►", command=lambda: print("Next Track"), width=50)
    next_button.grid(row=1, column=5, padx=5, pady=20)

    volume_label = ctk.CTkLabel(controls_frame, text="Volume", font=("Arial", 14))
    volume_label.grid(row=1, column=0, padx=(5, 0), sticky="e")

    volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=set_volume)
    volume_slider.grid(row=1, column=1, padx=(0, 10), sticky="ew")
    volume_slider.configure(width=150)

    return controls_frame

# Create frames
sidebar_frame = create_sidebar_frame()
visual_frame = create_visual_frame()
controls_frame = create_controls_frame()

# Bind mouse click to set progress
progress_bar.set(0)
progress_bar.bind("<Button-1>", set_progress)

update_scrolling_text()

# Start the GUI main loop
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root.mainloop()
