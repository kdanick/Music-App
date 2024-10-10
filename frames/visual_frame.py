import customtkinter as ctk

class VisualFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.track_label = ctk.CTkLabel(self, text="Now Playing: Track Name", font=("Arial", 18))
        self.track_label.pack(pady=(10, 20))
