"""
Price View Module
=================
Tracking prices of commodities per 1000L.
"""

import customtkinter as ctk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App

class PriceView(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, app: "App") -> None:
        super().__init__(parent, fg_color="transparent")
        self._app = app
        self._config = app.config_manager
        self._entries = {}
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        # Back button
        ctk.CTkButton(
            self, text="⬅ Menu", width=100, height=35,
            fg_color="#444444", hover_color="#333333",
            command=self._on_back_click
        ).place(x=20, y=20)
        
        # Title
        ctk.CTkLabel(
            self, text="💰 Tracker Cen (na 1000L)", 
            font=("Roboto", 28, "bold"), text_color="#27ae60"
        ).pack(pady=(20, 30))

        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=15)
        main_frame.pack(padx=100, pady=10, fill="both", expand=True)

        # Inputs
        self._create_price_row(main_frame, "Siano", "hay", "#E69F00", 0)
        self._create_price_row(main_frame, "Kiszonka", "silage", "#009E73", 1)
        self._create_price_row(main_frame, "Słoma", "straw", "#F0E442", 2)
        self._create_price_row(main_frame, "Pasza Mineralna", "mineral", "#FFFFFF", 3)
        self._create_price_row(main_frame, "Gotowy TMR (Sprzedaż)", "tmr", "#3B8ED0", 4)

        # Info
        ctk.CTkLabel(
            self, text="Ceny są zapisywane automatycznie po zmianie pola.",
            text_color="gray"
        ).pack(pady=20)

    def _create_price_row(self, parent, label, key, color, row):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            container, text=f"● {label}", font=("Roboto", 16, "bold"),
            text_color=color, width=200, anchor="w"
        ).pack(side="left")

        entry = ctk.CTkEntry(
            container, width=150, font=("Roboto", 16), justify="right",
            placeholder_text="0"
        )
        entry.pack(side="right")
        
        # Load value
        val = self._config.get_price(key)
        entry.insert(0, str(val))
        
        # Save on change
        entry.bind("<FocusOut>", lambda e, k=key, ent=entry: self._save_price(k, ent))
        self._entries[key] = entry

    def _save_price(self, key, entry):
        try:
            val = float(entry.get())
            self._config.set_price(key, val)
        except ValueError:
            pass # Ignore invalid numbers

    def _on_back_click(self):
        self._app.show_menu()