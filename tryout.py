import shutil
import os
import customtkinter as ctk
import time
import pygame
from tkinter import messagebox  # Import messagebox for alerts

# Initialize pygame mixer
pygame.mixer.init()

# Initialize the main window
root = ctk.CTk()
root.title("Groove - Music Player")
root.geometry("800x610")
root.configure(padx=20, pady=20)

# Total duration of the track (change this as necessary)
total_duration = 230  # Set this to the actual track duration in seconds

# Variable to track playback state
is_playing = False
start_time = 0

def update_timer():
    global is_playing
    if is_playing:
        elapsed_time = time.time() - start_time
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        total_time = time.strftime("%M:%S", time.gmtime(total_duration))

        current_time_label.configure(text=current_time)
        total_time_label.configure(text=total_time)

        if elapsed_time < total_duration:
            progress_bar.set(elapsed_time / total_duration)
            root.after(1000, update_timer)
        else:
            progress_bar.set(1.0)
            is_playing = False
            play_pause_button.configure(text="▶ Play")

def toggle_play_pause():
    global is_playing, start_time
    is_playing = not is_playing

    if is_playing:
        if start_time == 0:
            pygame.mixer.music.load("C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/MY POWER (Official Audio).mp3")  # Replace with actual song path
            pygame.mixer.music.play(loops=0)
            start_time = time.time()
            play_pause_button.configure(text="❚❚ Pause")
            update_timer()
        else:
            pygame.mixer.music.unpause()
            play_pause_button.configure(text="❚❚ Pause")
            start_time = time.time() - (progress_bar.get() * total_duration)
            update_timer()
    else:
        pygame.mixer.music.pause()
        play_pause_button.configure(text="▶ Play")

def set_progress(event):
    new_value = (event.x / progress_bar.winfo_width())
    progress_bar.set(new_value)
    position = new_value * total_duration
    pygame.mixer.music.pause()
    pygame.mixer.music.set_pos(position)
    global start_time
    start_time = time.time() - position
    if is_playing:
        pygame.mixer.music.unpause()
        update_timer()

def set_volume(value):
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)

# Function to add the current song to the playlist folder
def add_to_playlist():
    current_song_path = "C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/MY POWER (Official Audio).mp3"  # Replace with variable for current song path
    playlist_folder = "C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/Playlist1"  # Define your playlist folder path

    if not os.path.exists(playlist_folder):
        os.makedirs(playlist_folder)

    song_name = os.path.basename(current_song_path)
    destination_path = os.path.join(playlist_folder, song_name)

    try:
        shutil.copy(current_song_path, destination_path)
        messagebox.showinfo("Added to Playlist", f"'{song_name}' has been added to your playlist!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add song: {e}")

# Function to open the playlists management window
def open_playlists_window():
    playlists_window = ctk.CTkToplevel(root)
    playlists_window.title("Manage Playlists")
    playlists_window.geometry("400x400")

    # Function to load and display playlists
    def load_playlists():
        playlists = []  # List to hold playlist names
        playlists_folder = "C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/"  # Folder containing playlists
        for item in os.listdir(playlists_folder):
            if os.path.isdir(os.path.join(playlists_folder, item)):
                playlists.append(item)
        return playlists

    # Create a frame to hold the playlists
    playlists_frame = ctk.CTkFrame(playlists_window)
    playlists_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Frame to display songs of a selected playlist
    song_display_frame = ctk.CTkFrame(playlists_window)
    song_display_frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Refresh the list of playlists
    def refresh_playlists():
        for widget in playlists_frame.winfo_children():
            widget.destroy()  # Clear the current list
        playlists = load_playlists()
        for playlist in playlists:
            button = ctk.CTkButton(playlists_frame, text=playlist, command=lambda p=playlist: load_playlist(p))
            button.pack(pady=5, fill="x")

    # Load playlists on startup
    refresh_playlists()

    # Function to load a selected playlist and display songs
    def load_playlist(playlist_name):
        playlist_path = os.path.join("C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/", playlist_name)
        songs = [song for song in os.listdir(playlist_path) if song.endswith(('.mp3', '.wav'))]  # Filter music files

        # Clear previous song list in the song display frame
        for widget in song_display_frame.winfo_children():
            widget.destroy()

        # Display the song names in the selected playlist
        if songs:
            for song in songs:
                song_label = ctk.CTkLabel(song_display_frame, text=song, font=("Arial", 14))
                song_label.pack(anchor="w", padx=10, pady=2)
        else:
            no_songs_label = ctk.CTkLabel(song_display_frame, text="No songs in this playlist.", font=("Arial", 14))
            no_songs_label.pack(anchor="center", padx=10, pady=20)

    # Function to delete the selected playlist
    def delete_playlist():
        selected_playlist = playlist_name_entry.get()
        if not selected_playlist:
            messagebox.showwarning("Input Error", "Please enter a playlist name to delete.")
            return

        playlist_path = os.path.join("C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/", selected_playlist)
        if os.path.exists(playlist_path):
            shutil.rmtree(playlist_path)  # Remove the entire directory
            messagebox.showinfo("Deleted Playlist", f"Playlist '{selected_playlist}' has been deleted.")
            refresh_playlists()
        else:
            messagebox.showerror("Error", f"Playlist '{selected_playlist}' does not exist.")

    # Entry to create a new playlist
    playlist_name_entry = ctk.CTkEntry(playlists_window, placeholder_text="Enter playlist name...")
    playlist_name_entry.pack(pady=10)

    # Button to create a new playlist
    create_button = ctk.CTkButton(playlists_window, text="Create Playlist", command=lambda: create_playlist(playlist_name_entry.get()))
    create_button.pack(pady=5)

    # Button to delete a selected playlist
    delete_button = ctk.CTkButton(playlists_window, text="Delete Playlist", command=delete_playlist)
    delete_button.pack(pady=5)

    # Function to create a new playlist
    def create_playlist(playlist_name):
        if not playlist_name:
            messagebox.showwarning("Input Error", "Please enter a playlist name.")
            return

        playlist_path = os.path.join("C:/Users/adhia/OneDrive/Documents/1st Year/MusicApp/music/", playlist_name)
        if not os.path.exists(playlist_path):
            os.makedirs(playlist_path)  # Create the directory for the new playlist
            messagebox.showinfo("Created Playlist", f"Playlist '{playlist_name}' has been created.")
            refresh_playlists()
        else:
            messagebox.showwarning("Warning", f"Playlist '{playlist_name}' already exists.")

# Create Sidebar Frame
def create_sidebar_frame():
    sidebar_frame = ctk.CTkFrame(root, width=200)
    sidebar_frame.grid(row=0, column=0, sticky="ns", padx=(0, 0))
    search_bar = ctk.CTkEntry(sidebar_frame, placeholder_text="Search...", width=180)
    search_bar.pack(pady=(10, 10))

    sidebar_buttons = [
        ("Recents", lambda: print("Recents clicked")),
        ("Music Library", lambda: print("Music Library clicked")),
        ("Favorites", lambda: print("Favorites clicked")),
        ("Play Queue", lambda: print("Play Queue clicked")),
        ("Playlists", open_playlists_window),  # Updated to open playlists management window
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

    volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=set_volume)
    volume_slider.grid(row=1, column=5, padx=(0, 10), sticky="ew")
    volume_slider.configure(width=150)

    # Add "Add to Playlist" button
    add_button = ctk.CTkButton(controls_frame, text="Add to Playlist", command=add_to_playlist)
    add_button.grid(row=1, column=6, padx=10, pady=20)

    return controls_frame

# Create frames
sidebar_frame = create_sidebar_frame()
visual_frame = create_visual_frame()
controls_frame = create_controls_frame()

progress_bar.set(0)
progress_bar.bind("<Button-1>", set_progress)

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root.mainloop()