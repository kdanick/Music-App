import customtkinter as ctk

# Initialize the main window
root = ctk.CTk()
root.title("Groove - Music Player")
root.iconbitmap("images/apple_music_android_logo_icon_134021.ico")
root.geometry("800x600")
root.configure(padx=20, pady=20)

# Sidebar frame (1/3 of the width)
sidebar_frame = ctk.CTkFrame(root, width=200)  # Set a width for the sidebar
sidebar_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))

# Hamburger button to toggle sidebar width
toggle_button = ctk.CTkButton(root, text="☰", command=lambda: toggle_sidebar(sidebar_frame), width=30, height=30)
toggle_button.grid(row=0, column=0, sticky="nw")  # Position in the top left corner

# Visual frame (2/3 of the width)
visual_frame = ctk.CTkFrame(root)
visual_frame.grid(row=0, column=1, sticky="nsew")  # Fill all available space

# Configure grid weight to make the visual frame expand
root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
root.grid_columnconfigure(1, weight=2)  # Allow column 1 (visual_frame) to expand

# Display for current track
track_name = "Track Name"  # Set the current track name
track_label = ctk.CTkLabel(visual_frame, text=f"Now Playing: {track_name}", font=("Arial", 18))
track_label.pack(pady=(10, 20))

# Control buttons (Previous, Play/Pause, Next)
controls_frame = ctk.CTkFrame(root)
controls_frame.grid(row=1, column=0, columnspan=2, pady=(10, 10), sticky="ew")  # Pack the controls frame at the bottom

# Configure grid weights for the controls frame
controls_frame.grid_columnconfigure(0, weight=1)  # Track name label
controls_frame.grid_columnconfigure(1, weight=0)  # Previous button
controls_frame.grid_columnconfigure(2, weight=0)  # Play/Pause button
controls_frame.grid_columnconfigure(3, weight=0)  # Next button
controls_frame.grid_columnconfigure(4, weight=0)  # Volume label
controls_frame.grid_columnconfigure(5, weight=0)  # Volume slider (fixed width)

# Track name label on the left of the Previous button
track_label_left = ctk.CTkLabel(controls_frame, text=track_name, font=("Arial", 14))
track_label_left.grid(row=0, column=0, padx=(10, 5), sticky="w")  # Add a little padding on the right

# Previous button
prev_button = ctk.CTkButton(controls_frame, text="◄◄", command=lambda: print("Previous Track"), width=50)
prev_button.grid(row=0, column=1, padx=5)

# Play/Pause button
play_pause_button = ctk.CTkButton(controls_frame, text="▶ Play/Pause", command=lambda: print("Play/Pause"), height=40)
play_pause_button.grid(row=0, column=2, padx=5)

# Next button
next_button = ctk.CTkButton(controls_frame, text="►►", command=lambda: print("Next Track"), width=50)
next_button.grid(row=0, column=3, padx=5)

# Volume control label and slider
volume_label = ctk.CTkLabel(controls_frame, text="Volume", font=("Arial", 14))
volume_label.grid(row=0, column=4, padx=(10, 5))  # Add a little padding on the right

# Fixed width for the volume slider
volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=lambda value: print(f"Volume set to {value}"))
volume_slider.grid(row=0, column=5, padx=(0, 10), sticky="ew")  # Fill horizontally
volume_slider.configure(width=150)  # Set a fixed width for the slider

# Progress bar for track
progress_bar = ctk.CTkProgressBar(controls_frame)
progress_bar.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(10, 0))  # Pack the progress bar at the bottom

# Function to update progress bar and track progress based on mouse click
progress_bar.bind("<Button-1>", lambda event: set_progress(event, progress_bar))  # Left mouse button click
progress_bar.bind("<B1-Motion>", lambda event: set_progress(event, progress_bar))  # Mouse drag while button is held down

# Function to toggle sidebar width
def toggle_sidebar(sidebar):
    if sidebar.winfo_width() == 200:
        sidebar.configure(width=50)  # Collapse to a smaller width
    else:
        sidebar.configure(width=200)  # Expand to full width

# Function to set progress based on mouse click
def set_progress(event, progress_bar):
    # Calculate the new progress based on where the mouse was clicked
    new_value = (event.x / progress_bar.winfo_width())
    progress_bar.set(new_value)

# Start the GUI main loop
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root.mainloop()
