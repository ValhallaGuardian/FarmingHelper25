"""
Main Application Module
=======================
Contains the main App class that manages the window and navigation.
"""

import os
import sys
import customtkinter as ctk
from typing import Optional, Type

from src.utils.config_manager import ConfigManager
from src.views.menu_view import MenuView
from src.views.tmr_view import TMRView
from src.views.settings_view import SettingsView


class App(ctk.CTk):
    """
    Main application class for Farming Helper 25.
    
    Manages the main window, navigation between views,
    and application-wide configuration.
    """
    
    # Window configuration
    WINDOW_TITLE = "Farming Helper 25 by Valhalla"
    DEFAULT_WIDTH = 1100
    DEFAULT_HEIGHT = 750
    MIN_WIDTH = 900
    MIN_HEIGHT = 600
    
    def __init__(self) -> None:
        """Initialize the main application window."""
        super().__init__()
        
        # Configure main window
        self.title(self.WINDOW_TITLE)
        self.geometry(f"{self.DEFAULT_WIDTH}x{self.DEFAULT_HEIGHT}")
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        
        # Set application icon if available
        self._set_icon()
        
        # Initialize configuration manager
        self._config_manager = ConfigManager()
        
        # Container for views
        self._container = ctk.CTkFrame(self, fg_color="transparent")
        self._container.pack(fill="both", expand=True)
        
        # Current active view reference
        self._current_view: Optional[ctk.CTkFrame] = None
        
        # Show main menu on startup
        self.show_menu()
    
    def _set_icon(self) -> None:
        """Set the application icon if available."""
        # Determine application path
        if getattr(sys, 'frozen', False):
            app_path = sys._MEIPASS
        else:
            app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        icon_path = os.path.join(app_path, "logo.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass  # Ignore icon errors
    
    @property
    def config_manager(self) -> ConfigManager:
        """Get the configuration manager instance."""
        return self._config_manager
    
    def _clear_container(self) -> None:
        """Clear all widgets from the container."""
        if self._current_view is not None:
            self._current_view.pack_forget()
            self._current_view.destroy()
            self._current_view = None
    
    def _show_view(self, view_class: Type[ctk.CTkFrame], **kwargs) -> None:
        """
        Display a view in the container.
        
        Args:
            view_class: The view class to instantiate.
            **kwargs: Additional arguments to pass to the view.
        """
        self._clear_container()
        self._current_view = view_class(self._container, app=self, **kwargs)
        self._current_view.pack(fill="both", expand=True)
    
    def show_menu(self) -> None:
        """Navigate to the main menu view."""
        self._show_view(MenuView)
    
    def show_tmr_calculator(self) -> None:
        """Navigate to the TMR calculator view."""
        self._show_view(TMRView)
    
    def show_settings(self) -> None:
        """Navigate to the settings view."""
        self._show_view(SettingsView)
    
    def exit_app(self) -> None:
        """Close the application."""
        self.quit()
