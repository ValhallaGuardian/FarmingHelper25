"""
Menu View Module
================
Contains the main menu screen with navigation buttons.
"""

import customtkinter as ctk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App


class MenuView(ctk.CTkFrame):
    """
    Main menu view with navigation to different app sections.
    
    Displays the application title and buttons for:
    - TMR Calculator
    - Settings
    - Exit
    """
    
    def __init__(self, parent: ctk.CTkFrame, app: "App") -> None:
        """
        Initialize the menu view.
        
        Args:
            parent: Parent widget container.
            app: Main application instance for navigation.
        """
        super().__init__(parent, fg_color="transparent")
        self._app = app
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the menu user interface."""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Spacer top
        self.grid_rowconfigure(1, weight=0)  # Title
        self.grid_rowconfigure(2, weight=0)  # Subtitle
        self.grid_rowconfigure(3, weight=0)  # Buttons frame
        self.grid_rowconfigure(4, weight=2)  # Spacer bottom
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🌾 Farming Helper 25 🌾",
            font=("Roboto", 48, "bold"),
            text_color="#3B8ED0"
        )
        title_label.grid(row=1, column=0, pady=(0, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self,
            text="by Valhalla",
            font=("Roboto", 20),
            text_color="#808080"
        )
        subtitle_label.grid(row=2, column=0, pady=(0, 50))
        
        # Buttons container
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=3, column=0, pady=20)
        
        # TMR Calculator button
        tmr_button = ctk.CTkButton(
            buttons_frame,
            text="🐄  Kalkulator TMR",
            font=("Roboto", 24, "bold"),
            width=400,
            height=80,
            corner_radius=15,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self._on_tmr_click
        )
        tmr_button.pack(pady=15)

        # Price Tracker button
        prices_button = ctk.CTkButton(
            buttons_frame,
            text="💰  Ekonomia / Ceny",
            font=("Roboto", 24, "bold"),
            width=400,
            height=80,
            corner_radius=15,
            fg_color="#d35400", 
            hover_color="#a04000",
            command=self._on_prices_click
        )
        prices_button.pack(pady=15)
        
        # Settings button
        settings_button = ctk.CTkButton(
            buttons_frame,
            text="⚙️  Ustawienia",
            font=("Roboto", 24, "bold"),
            width=400,
            height=80,
            corner_radius=15,
            fg_color="#27ae60",
            hover_color="#1e8449",
            command=self._on_settings_click
        )
        settings_button.pack(pady=15)
        
        # Exit button
        exit_button = ctk.CTkButton(
            buttons_frame,
            text="🚪  Wyjście",
            font=("Roboto", 24, "bold"),
            width=400,
            height=80,
            corner_radius=15,
            fg_color="#c0392b",
            hover_color="#922b21",
            command=self._on_exit_click
        )
        exit_button.pack(pady=15)
        
        # Version info at bottom
        version_label = ctk.CTkLabel(
            self,
            text="Wersja 1.0.0",
            font=("Roboto", 12),
            text_color="#555555"
        )
        version_label.grid(row=4, column=0, sticky="s", pady=20)
    
    def _on_tmr_click(self) -> None:
        """Handle TMR Calculator button click."""
        self._app.show_tmr_calculator()
    
    def _on_settings_click(self) -> None:
        """Handle Settings button click."""
        self._app.show_settings()
    
    def _on_exit_click(self) -> None:
        """Handle Exit button click."""
        self._app.exit_app()

    def _on_prices_click(self) -> None:
        self._app.show_prices()
