#!/usr/bin/env python3
"""
Farming Helper 25 by Valhalla
=============================
Entry point for the application.
A modular farming assistant for Farming Simulator 25.
"""

import customtkinter as ctk
from src.app import App


def main() -> None:
    """Initialize and run the Farming Helper 25 application."""
    # Configure appearance
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Create and run the application
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
