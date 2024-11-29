import os
import customtkinter as ctk
import time
import pygame
from CTkListbox import *
from tkinter import filedialog
from mutagen.mp3 import MP3  # Import to get duration of MP3 files

pygame.mixer.init()

root = ctk.CTk()
root.title("Groove - Music Player")
root.geometry("800x610")
root.configure(padx=20, pady=20)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

total_duration = 0
is_playing = False
start_time = 0


def set_volume(value):
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)


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
            progress_bar.set(0.0)
            is_playing = False
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


sidebar_frame = ctk.CTkFrame(root)
sidebar_frame.grid(row=0, column=0, sticky="ns", padx=(0, 0))

search_bar = ctk.CTkEntry(sidebar_frame, placeholder_text="Search...", width=180)
search_bar.grid(row=0, column=0, sticky="ns", padx=(0, 0))

listbox = CTkListbox(sidebar_frame)
listbox.grid(row=1, column=0, sticky="ns", pady=10)
listbox.bind("<<ListboxSelect>>", lambda event: play_song())

manage_playlist_button = ctk.CTkButton(sidebar_frame, text="Manage Playlist",
                                       command=lambda: show_frame(manage_playlist_frame))
manage_playlist_button.grid(row=3, column=0, pady=5)

controls_frame = ctk.CTkFrame(root)
controls_frame.grid(row=1, column=0, columnspan=2, pady=(0, 0), sticky="ew")
controls_frame.grid_columnconfigure(0, weight=0)
controls_frame.grid_columnconfigure(1, weight=1)
controls_frame.grid_columnconfigure(2, weight=0)
controls_frame.grid_columnconfigure(3, weight=0)
controls_frame.grid_columnconfigure(4, weight=0)
controls_frame.grid_columnconfigure(5, weight=1)
controls_frame.grid_columnconfigure(6, weight=0)
controls_frame.grid_columnconfigure(7, weight=0)
controls_frame.grid_columnconfigure(8, weight=0)

current_time_label = ctk.CTkLabel(controls_frame, text="00:00", font=("Arial", 14))
current_time_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

total_time_label = ctk.CTkLabel(controls_frame, text="00:00", font=("Arial", 14))
total_time_label.grid(row=0, column=8, padx=(5, 10), sticky="e")

progress_bar = ctk.CTkProgressBar(controls_frame)
progress_bar.grid(row=0, column=1, columnspan=7, sticky="ew", pady=(10, 0))
progress_bar.set(0)
progress_bar.bind("<Button-1>", set_progress)

prev_button = ctk.CTkButton(controls_frame, text="◄◄", command=lambda: previous_song(), width=50)
prev_button.grid(row=1, column=2, padx=5, pady=20)

play_pause_button = ctk.CTkButton(controls_frame, text="▶ Play", command=lambda: toggle_play_pause(), height=40)
play_pause_button.grid(row=1, column=3, padx=5, pady=20)

next_button = ctk.CTkButton(controls_frame, text="►►", command=lambda: next_song(), width=50)
next_button.grid(row=1, column=4, padx=5, pady=20)

volume_label = ctk.CTkLabel(controls_frame, text="Volume", font=("Arial", 14))
volume_label.grid(row=1, column=6, padx=(10, 5))

volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=set_volume)
volume_slider.grid(row=1, column=7, padx=(0, 10), sticky="ew")
volume_slider.configure(width=150)

visual_frame = ctk.CTkFrame(root)
visual_frame.grid(row=0, column=1, sticky="nsew")
song_label = ctk.CTkLabel(visual_frame, text="Song", font=("Arial", 14))
song_label.pack()
create_playlist_frame = ctk.CTkFrame(root)
create_playlist_frame.grid(row=0, column=1, sticky="nsew")
manage_playlist_frame = ctk.CTkFrame(root)
manage_playlist_frame.grid(row=0, column=1, sticky="nsew")

add_songs_button = ctk.CTkButton(manage_playlist_frame, text="Add Songs", command=lambda: add_songs())
add_songs_button.grid(row=0, column=0, pady=5, padx=20)

# Routes to directories
songs_folder = "music/"
music_dir = os.path.dirname(os.path.realpath(__file__))
full_path_backslash = os.path.join(music_dir, songs_folder)
full_path = full_path_backslash.replace("\\", "/")

song_list = []

def show_frame(frame):
    frame.tkraise()


def add_songs():
    songs = filedialog.askopenfilenames(initialdir="music/", title="Choose a song",
                                        filetypes=(("mp3 Files", "*.mp3"),))
    if songs:
        for song in songs:
            song_name = os.path.basename(song).replace(".mp3", "")
            listbox.insert("end", song_name)
            song_list.append((song_name, song))
            # song_name = os.path.basename(song).replace(".mp3", "")
            # listbox.insert("end", song_name)

def filter_listbox(event):
    search_term = search_bar.get().lower()
    print(search_term)
    listbox.delete(0, "end")

    if search_term == "":
        for title, _ in song_list:
            listbox.insert("end", title)
    else:
        print("Entering else")
        for title, path in song_list:
            if search_term in title.lower():
                listbox.insert("end", title)

search_bar.bind("<Key>", filter_listbox)



def start_music(song_path, title):
    global total_duration, start_time
    show_frame(visual_frame)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play(loops=0)

    # Get duration of the song
    audio = MP3(song_path)
    total_duration = audio.info.length
    total_time_label.configure(text=time.strftime("%M:%S", time.gmtime(total_duration)))

    start_time = time.time()  # Initialize start time
    global is_playing
    is_playing = True
    play_pause_button.configure(text="❚❚ Pause")
    song_label.configure(text=title)
    progress_bar.set(0)  # Reset progress bar at the start

    update_timer()


def play_song():
    selected_song = listbox.get(listbox.curselection())
    song_path = f"{full_path}{selected_song}.mp3"

    index = listbox.curselection()
    start_music(song_path, selected_song)


def previous_song():
    previous_s = 0
    if listbox.curselection() == 0:
        previous_s = listbox.size()-1
        prev_song = listbox.get(previous_s)
        song_path = f"{full_path}{prev_song}.mp3"

    else:

        prev_song = listbox.get(listbox.curselection() - 1)
        song_path = f"{full_path}{prev_song}.mp3"

    index1 = listbox.curselection()
    index2 = listbox.curselection()-1

    if index2<0:
        index2 = previous_s

    listbox.deactivate(index1)
    listbox.activate(index2)
    start_music(song_path, prev_song)


def next_song():

    if listbox.curselection() + 2 > listbox.size():
        next_s = listbox.get(0)
        song_path = f"{full_path}{next_s}.mp3"

    else:

        next_s = listbox.get(listbox.curselection() + 1)
        song_path = f"{full_path}{next_s}.mp3"

    index1 = listbox.curselection()
    index2 = listbox.curselection()+1

    if (index2 + 1) > listbox.size():
        index2 = 0

    listbox.deactivate(index1)
    listbox.activate(index2)
    start_music(song_path, next_s)


def toggle_play_pause():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        play_pause_button.configure(text="▶ Play")
    else:
        pygame.mixer.music.unpause()
        play_pause_button.configure(text="❚❚ Pause")
    is_playing = not is_playing


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
root.mainloop()
