import customtkinter as ctk

class SidebarFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.width = 200
        self.configure(width=self.width)

        # Search bar
        self.search_bar = ctk.CTkEntry(self, placeholder_text="Search...", width=180)
        self.search_bar.pack(pady=(10, 10))

        # Sidebar buttons
        self.sidebar_buttons = [
            ("Recents", self.on_recents_click),
            ("Music Library", self.on_music_library_click),
            ("Favorites", self.on_favorites_click),
            ("Play Queue", self.on_play_queue_click),
            ("Playlists", self.on_playlists_click),
        ]

        for text, command in self.sidebar_buttons:
            button = ctk.CTkButton(self, text=text, command=command, width=180)
            button.pack(pady=(5, 0))

    def on_recents_click(self):
        print("Recents clicked")

    def on_music_library_click(self):
        print("Music Library clicked")

    def on_favorites_click(self):
        print("Favorites clicked")

    def on_play_queue_click(self):
        print("Play Queue clicked")

    def on_playlists_click(self):
        print("Playlists clicked")
