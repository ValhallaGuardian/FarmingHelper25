"""
Settings View Module
====================
Contains the settings screen for application configuration.
"""

import customtkinter as ctk
from tkinter import filedialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App


class SettingsView(ctk.CTkFrame):
    """
    Settings view for configuring application options.
    
    Allows users to:
    - Set savegame location
    - Configure default values
    """
    
    def __init__(self, parent: ctk.CTkFrame, app: "App") -> None:
        """
        Initialize the settings view.
        
        Args:
            parent: Parent widget container.
            app: Main application instance.
        """
        super().__init__(parent, fg_color="transparent")
        self._app = app
        self._config = app.config_manager
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the settings user interface."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Back button
        self.grid_rowconfigure(1, weight=0)  # Title
        self.grid_rowconfigure(2, weight=1)  # Settings container
        
        # Back button
        back_button = ctk.CTkButton(
            self,
            text="⬅ Menu",
            width=100,
            height=35,
            fg_color="#444444",
            hover_color="#333333",
            command=self._on_back_click
        )
        back_button.grid(row=0, column=0, sticky="nw", padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="⚙️ Ustawienia",
            font=("Roboto", 36, "bold"),
            text_color="#27ae60"
        )
        title_label.grid(row=1, column=0, pady=(10, 30))
        
        # Settings container
        settings_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        settings_frame.grid(row=2, column=0, sticky="nsew", padx=100, pady=(0, 50))
        settings_frame.grid_columnconfigure(0, weight=1)
        
        # --- Savegame Location Section ---
        self._create_savegame_section(settings_frame)
        
        # --- Default Values Section ---
        self._create_defaults_section(settings_frame)
        
        # --- Reset Section ---
        self._create_reset_section(settings_frame)
    
    def _create_savegame_section(self, parent: ctk.CTkFrame) -> None:
        """Create the savegame location settings section."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=30, pady=20)
        
        # Section title
        ctk.CTkLabel(
            section_frame,
            text="📁 Lokalizacja Savegame",
            font=("Roboto", 18, "bold"),
            text_color="#3B8ED0"
        ).pack(anchor="w", pady=(0, 10))
        
        # Input frame
        input_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        input_frame.pack(fill="x")
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Path entry
        self._path_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Wybierz folder savegame...",
            font=("Roboto", 13),
            height=40
        )
        self._path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Load current value
        current_path = self._config.get("save_game_path", "")
        if current_path:
            self._path_entry.insert(0, current_path)
        
        # Browse button
        browse_button = ctk.CTkButton(
            input_frame,
            text="Przeglądaj...",
            width=120,
            height=40,
            fg_color="#555555",
            hover_color="#444444",
            command=self._on_browse_click
        )
        browse_button.grid(row=0, column=1)
        
        # Help text
        ctk.CTkLabel(
            section_frame,
            text="Ścieżka do folderu zapisu gry (np. Documents/My Games/FarmingSimulator2025/savegame1)",
            font=("Roboto", 11),
            text_color="#666666"
        ).pack(anchor="w", pady=(5, 0))
    
    def _create_defaults_section(self, parent: ctk.CTkFrame) -> None:
        """Create the default values settings section."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=30, pady=20)
        
        # Section title
        ctk.CTkLabel(
            section_frame,
            text="📊 Wartości Domyślne",
            font=("Roboto", 18, "bold"),
            text_color="#3B8ED0"
        ).pack(anchor="w", pady=(0, 15))
        
        # Grid for defaults
        grid_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        grid_frame.pack(fill="x")
        grid_frame.grid_columnconfigure((0, 2), weight=1)
        grid_frame.grid_columnconfigure((1, 3), weight=0)
        
        # Wagon capacity
        ctk.CTkLabel(
            grid_frame,
            text="Pojemność paszowozu (L):",
            font=("Roboto", 13)
        ).grid(row=0, column=0, sticky="w", pady=8)
        
        self._wagon_entry = ctk.CTkEntry(grid_frame, width=120, justify="right")
        self._wagon_entry.insert(0, str(self._config.get("wagon_capacity", 24000)))
        self._wagon_entry.grid(row=0, column=1, pady=8, padx=(10, 30))
        self._wagon_entry.bind("<FocusOut>", self._on_wagon_change)
        
        # Bale sizes
        bale_settings = [
            ("Rozmiar belki siana (L):", "bale_hay", 5500),
            ("Rozmiar belki słomy (L):", "bale_straw", 7500),
            ("Rozmiar belki/kubła kiszonki (L):", "bale_silage", 5000),
        ]
        
        self._bale_entries = {}
        
        for i, (label, key, default) in enumerate(bale_settings):
            ctk.CTkLabel(
                grid_frame,
                text=label,
                font=("Roboto", 13)
            ).grid(row=i + 1, column=0, sticky="w", pady=8)
            
            entry = ctk.CTkEntry(grid_frame, width=120, justify="right")
            entry.insert(0, str(self._config.get(key, default)))
            entry.grid(row=i + 1, column=1, pady=8, padx=(10, 30))
            entry.bind("<FocusOut>", lambda e, k=key: self._on_bale_change(k))
            self._bale_entries[key] = entry
    
    def _create_reset_section(self, parent: ctk.CTkFrame) -> None:
        """Create the reset settings section."""
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(fill="x", padx=30, pady=20)
        
        # Separator
        separator = ctk.CTkFrame(section_frame, height=2, fg_color="#333333")
        separator.pack(fill="x", pady=(0, 20))
        
        # Reset button
        reset_button = ctk.CTkButton(
            section_frame,
            text="🔄 Przywróć Domyślne",
            font=("Roboto", 14),
            width=200,
            height=40,
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self._on_reset_click
        )
        reset_button.pack(anchor="w")
        
        ctk.CTkLabel(
            section_frame,
            text="Przywraca wszystkie ustawienia do wartości domyślnych",
            font=("Roboto", 11),
            text_color="#666666"
        ).pack(anchor="w", pady=(5, 0))
    
    def _on_browse_click(self) -> None:
        """Handle browse button click to select savegame folder."""
        folder_path = filedialog.askdirectory(
            title="Wybierz folder savegame"
        )
        if folder_path:
            self._path_entry.delete(0, "end")
            self._path_entry.insert(0, folder_path)
            self._config.set("save_game_path", folder_path)
    
    def _on_wagon_change(self, event=None) -> None:
        """Handle wagon capacity change."""
        try:
            value = int(self._wagon_entry.get())
            if value > 0:
                self._config.set("wagon_capacity", value)
        except ValueError:
            pass  # Invalid input, ignore
    
    def _on_bale_change(self, key: str) -> None:
        """Handle bale size change."""
        try:
            entry = self._bale_entries.get(key)
            if entry:
                value = int(entry.get())
                if value > 0:
                    self._config.set(key, value)
        except ValueError:
            pass  # Invalid input, ignore
    
    def _on_reset_click(self) -> None:
        """Handle reset to defaults button click."""
        from tkinter import messagebox
        
        if messagebox.askyesno(
            "Potwierdź Reset",
            "Czy na pewno chcesz przywrócić wszystkie ustawienia do wartości domyślnych?"
        ):
            self._config.reset_to_defaults()
            # Refresh the view
            self._app.show_settings()
    
    def _on_back_click(self) -> None:
        """Handle back button click."""
        self._app.show_menu()
