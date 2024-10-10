import customtkinter as ctk
import time
from frames.sidebar_frame import SidebarFrame
from frames.visual_frame import VisualFrame
from frames.controls_frame import ControlsFrame

# Initialize the main window
root = ctk.CTk()
root.title("Groove - Music Player")
root.iconbitmap("images/apple_music_android_logo_icon_134021.ico")
root.geometry("800x610")
root.configure(padx=20, pady=20)

# Total duration of the track (e.g., 230 seconds = 3 minutes and 50 seconds)
total_duration = 230  # Set this to the actual track duration in seconds

# Variable to track playback state
is_playing = False

# Function to update timer labels
def update_timer():
    if is_playing:
        elapsed_time = controls_frame.progress_bar.get() * total_duration
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        total_time = time.strftime("%M:%S", time.gmtime(total_duration))

        controls_frame.current_time_label.configure(text=current_time)
        controls_frame.total_time_label.configure(text=total_time)

        # Call this function again after 1000 milliseconds (1 second)
        root.after(1000, update_timer)

# Create frames
sidebar_frame = SidebarFrame(root)
sidebar_frame.grid(row=0, column=0, sticky="ns", padx=(0, 0))

visual_frame = VisualFrame(root)
visual_frame.grid(row=0, column=1, sticky="nsew")

controls_frame = ControlsFrame(root, update_timer_callback=update_timer)
controls_frame.grid(row=1, column=0, columnspan=2, pady=(0, 0), sticky="ew")

# Configure grid weight
root.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
root.grid_columnconfigure(1, weight=2)  # Allow column 1 (visual_frame) to expand

# Start the GUI main loop
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    root.mainloop()
