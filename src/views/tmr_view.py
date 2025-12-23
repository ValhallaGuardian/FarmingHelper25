"""
TMR Calculator View Module
==========================
Contains the TMR feed calculator screen with full calculation logic.
"""

import math
import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from src.app import App


class TMRView(ctk.CTkFrame):
    """
    TMR (Total Mixed Ration) Calculator view.
    
    Provides two calculation modes:
    - Standard: Calculate full TMR load
    - Fill: Calculate remaining TMR based on already loaded ingredient
    
    Includes input fields for wagon capacity, bale sizes,
    and ingredient ratios with persistence via ConfigManager.
    """
    
    # Ingredient ratio limits (min, max percentages)
    LIMITS = {
        "hay": (20, 70),
        "silage": (20, 70),
        "straw": (1, 29),
        "mineral": (0, 5)
    }
    
    # Colors for visual identification of ingredients
    COLORS = {
        "hay": "#E69F00",      # Orange - Siano
        "straw": "#F0E442",    # Yellow - Słoma
        "silage": "#009E73",   # Green - Kiszonka
        "mineral": "#FFFFFF"   # White - Mineralna
    }
    
    # Polish labels for ingredients
    LABELS = {
        "hay": "Siano",
        "silage": "Kiszonka",
        "straw": "Słoma",
        "mineral": "Mineralna"
    }
    
    def __init__(self, parent: ctk.CTkFrame, app: "App") -> None:
        """
        Initialize the TMR calculator view.
        
        Args:
            parent: Parent widget container.
            app: Main application instance.
        """
        super().__init__(parent, fg_color="transparent")
        self._app = app
        self._config = app.config_manager
        
        # Entry references for standard tab
        self._std_entries: Dict[str, ctk.CTkEntry] = {}
        self._std_wagon: Optional[ctk.CTkComboBox] = None
        self._std_bale_hay: Optional[ctk.CTkEntry] = None
        self._std_bale_straw: Optional[ctk.CTkEntry] = None
        self._std_bale_silage: Optional[ctk.CTkEntry] = None
        self._std_result: Optional[ctk.CTkTextbox] = None
        
        # Entry references for fill tab
        self._fill_entries: Dict[str, ctk.CTkEntry] = {}
        self._fill_wagon: Optional[ctk.CTkComboBox] = None
        self._fill_bale_hay: Optional[ctk.CTkEntry] = None
        self._fill_bale_straw: Optional[ctk.CTkEntry] = None
        self._fill_bale_silage: Optional[ctk.CTkEntry] = None
        self._fill_result: Optional[ctk.CTkTextbox] = None
        self._fixed_var: Optional[ctk.StringVar] = None
        self._entry_fixed_amt: Optional[ctk.CTkEntry] = None
        
        self._setup_ui()
        self._load_saved_values()
    
    def _setup_ui(self) -> None:
        """Set up the calculator user interface."""
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
        back_button.place(x=20, y=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="🐄 Kalkulator TMR",
            font=("Roboto", 28, "bold"),
            text_color="#1f538d"
        )
        title_label.pack(pady=(20, 10))
        
        # Tab view for Standard and Fill modes
        self._tabview = ctk.CTkTabview(self)
        self._tabview.pack(padx=15, pady=(10, 15), fill="both", expand=True)
        
        # Create tabs
        self._tab_std = self._tabview.add("Standard")
        self._tab_fill = self._tabview.add("Uzupełnianie")
        
        # Initialize tabs
        self._init_standard_tab()
        self._init_fill_tab()
    
    def _create_wagon_input(self, parent: ctk.CTkFrame, row: int) -> ctk.CTkComboBox:
        """
        Create wagon capacity input with common presets.
        
        Args:
            parent: Parent frame.
            row: Grid row position.
            
        Returns:
            The wagon capacity combobox.
        """
        label = ctk.CTkLabel(
            parent,
            text="Pojemność Paszowozu:",
            font=("Roboto", 13),
            text_color="#bfbfbf"
        )
        label.grid(row=row, column=0, sticky="w", pady=6)
        
        combo = ctk.CTkComboBox(
            parent,
            values=["14000", "18000", "22000", "24000", "28000", "35000", "45000", "60000"],
            width=110,
            justify="right"
        )
        combo.grid(row=row, column=1, sticky="e", pady=6)
        
        return combo
    
    def _add_grid_input(
        self, parent: ctk.CTkFrame, row: int, text: str, default_val: int
    ) -> ctk.CTkEntry:
        """
        Create a labeled entry input in grid layout.
        
        Args:
            parent: Parent frame.
            row: Grid row position.
            text: Label text.
            default_val: Default value for entry.
            
        Returns:
            The entry widget.
        """
        label = ctk.CTkLabel(
            parent,
            text=text,
            font=("Roboto", 13),
            text_color="#bfbfbf"
        )
        label.grid(row=row, column=0, sticky="w", pady=6)
        
        entry = ctk.CTkEntry(parent, width=110, justify="right")
        entry.insert(0, str(default_val))
        entry.grid(row=row, column=1, sticky="e", pady=6)
        
        return entry
    
    def _add_spinbox_ratio(
        self, parent: ctk.CTkFrame, row: int, label: str, key: str
    ) -> ctk.CTkEntry:
        """
        Create a ratio input with increment/decrement buttons.
        
        Args:
            parent: Parent frame.
            row: Position index.
            label: Display label.
            key: Ingredient key (hay, silage, straw, mineral).
            
        Returns:
            The entry widget for the ratio value.
        """
        min_val, max_val = self.LIMITS[key]
        color = self.COLORS.get(key, "gray")
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        frame.grid_columnconfigure(1, weight=1)
        
        # Label with color indicator
        lbl = ctk.CTkLabel(
            frame,
            text=f"● {label} ({min_val}-{max_val}%)",
            font=("Roboto", 13),
            text_color=color
        )
        lbl.pack(side="left")
        
        # Spinbox frame
        spin_frame = ctk.CTkFrame(frame, fg_color="transparent")
        spin_frame.pack(side="right")
        
        # Entry for value
        entry = ctk.CTkEntry(spin_frame, width=50, justify="center")
        
        # Default value from config
        default = self._config.get_ratio(key)
        entry.insert(0, str(default))
        
        def change_val(delta: float) -> None:
            """Change value by delta, respecting limits."""
            try:
                current = float(entry.get())
                new_val = round(current + delta, 1)
                if min_val <= new_val <= max_val:
                    entry.delete(0, "end")
                    entry.insert(0, str(int(new_val) if new_val == int(new_val) else new_val))
            except ValueError:
                pass
        
        # Decrement button
        ctk.CTkButton(
            spin_frame,
            text="-",
            width=30,
            height=28,
            fg_color="#444444",
            command=lambda: change_val(-1)
        ).pack(side="left", padx=2)
        
        entry.pack(side="left", padx=2)
        
        # Increment button
        ctk.CTkButton(
            spin_frame,
            text="+",
            width=30,
            height=28,
            fg_color="#444444",
            command=lambda: change_val(1)
        ).pack(side="left", padx=2)
        
        return entry
    
    def _create_result_area(self, parent: ctk.CTkFrame) -> ctk.CTkTextbox:
        """
        Create the results display area.
        
        Args:
            parent: Parent frame.
            
        Returns:
            The textbox widget for results.
        """
        label = ctk.CTkLabel(
            parent,
            text="WYNIKI",
            font=("Roboto", 24, "bold"),
            text_color="white"
        )
        label.pack(pady=20, padx=20, anchor="nw")
        
        textbox = ctk.CTkTextbox(
            parent,
            font=("Roboto Mono", 15),
            text_color="#dce4ee",
            fg_color="#1e1e1e",
            corner_radius=5
        )
        textbox.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        textbox.configure(state="disabled")
        
        return textbox
    
    def _get_percents(self, entries: Dict[str, ctk.CTkEntry]) -> Optional[Dict[str, float]]:
        """
        Get percentage values from entry widgets and validate sum.
        
        Args:
            entries: Dictionary of ingredient entries.
            
        Returns:
            Dictionary of percentage values or None if invalid.
        """
        values = {}
        for key, entry in entries.items():
            try:
                values[key] = float(entry.get())
            except ValueError:
                messagebox.showerror("Błąd", f"Nieprawidłowa wartość dla: {self.LABELS.get(key, key)}")
                return None
        
        total = sum(values.values())
        if not (99.9 <= total <= 100.1):
            messagebox.showwarning(
                "Suma procentów",
                f"Suma procentów wynosi {total:.1f}%.\nPowinna wynosić 100%."
            )
        
        return values
    
    def _format_report(
        self,
        wagon: float,
        needed: Dict[str, float],
        percents: Dict[str, float],
        bale_hay: float,
        bale_straw: float,
        bale_silage: float,
        note: str = ""
    ) -> str:
        """
        Format the calculation results as a readable report.
        
        Args:
            wagon: Target wagon capacity.
            needed: Dictionary of needed amounts per ingredient.
            percents: Dictionary of percentage ratios.
            bale_hay: Hay bale size.
            bale_straw: Straw bale size.
            bale_silage: Silage bale/bucket size.
            note: Optional note to display at top.
            
        Returns:
            Formatted report string.
        """
        def calc_bales(amount: float, bale_size: float) -> tuple:
            """Calculate bales count and remainder."""
            if amount <= 0 or bale_size <= 0:
                return 0, 0
            count = math.floor(amount / bale_size)
            remainder = amount - (count * bale_size)
            return count, remainder
        
        hay_count, hay_rem = calc_bales(needed["hay"], bale_hay)
        straw_count, straw_rem = calc_bales(needed["straw"], bale_straw)
        silage_count, silage_rem = calc_bales(needed["silage"], bale_silage)
        
        txt = f"{note}\nCel: {wagon:,.0f} L\n" + "=" * 45 + "\n\n"
        
        txt += f"🟧 SIANO ({percents['hay']:.0f}%): {needed['hay']:,.0f} L\n"
        txt += f"   ➔ {hay_count} belek + {hay_rem:,.0f} L luzem\n\n"
        
        txt += f"🟨 SŁOMA ({percents['straw']:.0f}%): {needed['straw']:,.0f} L\n"
        txt += f"   ➔ {straw_count} belek + {straw_rem:,.0f} L luzem\n\n"
        
        txt += f"🟩 KISZONKA ({percents['silage']:.0f}%): {needed['silage']:,.0f} L\n"
        txt += f"   ➔ {silage_count} belek/kubłów + {silage_rem:,.0f} L luzem\n\n"
        
        txt += f"⬜ MINERALNA ({percents['mineral']:.0f}%): {needed['mineral']:,.0f} L\n"
        
        return txt
    
    def _init_standard_tab(self) -> None:
        """Initialize the Standard calculation tab."""
        self._tab_std.grid_columnconfigure(0, weight=1)
        self._tab_std.grid_columnconfigure(1, weight=2)
        self._tab_std.grid_rowconfigure(0, weight=1)
        
        # Left panel - inputs
        left = ctk.CTkFrame(self._tab_std, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Gear/Equipment inputs
        frame_gear = ctk.CTkFrame(left, fg_color="transparent")
        frame_gear.pack(fill="x")
        
        self._std_wagon = self._create_wagon_input(frame_gear, 0)
        self._std_bale_hay = self._add_grid_input(frame_gear, 1, "Belka Siana:", 5500)
        self._std_bale_straw = self._add_grid_input(frame_gear, 2, "Belka Słomy:", 7500)
        self._std_bale_silage = self._add_grid_input(frame_gear, 3, "Belka/Kubeł Kiszonki:", 5000)
        
        # Ratio inputs
        frame_ratios = ctk.CTkFrame(left, fg_color="transparent")
        frame_ratios.pack(fill="x", pady=20)
        
        ratio_config = [
            ("hay", "Siano"),
            ("silage", "Kiszonka"),
            ("straw", "Słoma"),
            ("mineral", "Mineralna")
        ]
        
        for i, (key, name) in enumerate(ratio_config):
            self._std_entries[key] = self._add_spinbox_ratio(frame_ratios, i, name, key)
        
        # Calculate button
        calc_button = ctk.CTkButton(
            left,
            text="OBLICZ",
            command=self._calc_standard,
            font=("Roboto", 16, "bold"),
            height=45,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        calc_button.pack(pady=20, fill="x")
        
        # Right panel - results
        right = ctk.CTkFrame(self._tab_std, fg_color="#1a1a1a", corner_radius=10)
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        
        self._std_result = self._create_result_area(right)
    
    def _init_fill_tab(self) -> None:
        """Initialize the Fill/Supplement calculation tab."""
        self._tab_fill.grid_columnconfigure(0, weight=1)
        self._tab_fill.grid_columnconfigure(1, weight=2)
        self._tab_fill.grid_rowconfigure(0, weight=1)
        
        # Left panel - inputs
        left = ctk.CTkFrame(self._tab_fill, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Gear/Equipment inputs
        frame_gear = ctk.CTkFrame(left, fg_color="transparent")
        frame_gear.pack(fill="x")
        
        self._fill_wagon = self._create_wagon_input(frame_gear, 0)
        self._fill_bale_hay = self._add_grid_input(frame_gear, 1, "Belka Siana:", 5500)
        self._fill_bale_straw = self._add_grid_input(frame_gear, 2, "Belka Słomy:", 7500)
        self._fill_bale_silage = self._add_grid_input(frame_gear, 3, "Belka/Kubeł Kiszonki:", 5000)
        
        # Fixed ingredient selection
        ctk.CTkLabel(
            left,
            text="CO WLANE?",
            font=("Roboto", 14, "bold")
        ).pack(pady=(10, 0), anchor="w")
        
        frame_fix = ctk.CTkFrame(left)
        frame_fix.pack(fill="x", pady=5)
        
        self._fixed_var = ctk.StringVar(value="silage")
        self._entry_fixed_amt = ctk.CTkEntry(
            frame_fix,
            placeholder_text="Ilość w L"
        )
        self._entry_fixed_amt.pack(side="bottom", fill="x", padx=5, pady=5)
        
        # Radio buttons for ingredient selection
        radio_frame = ctk.CTkFrame(frame_fix, fg_color="transparent")
        radio_frame.pack(fill="x")
        
        ctk.CTkRadioButton(
            radio_frame,
            text="Kiszonka",
            variable=self._fixed_var,
            value="silage",
            fg_color=self.COLORS["silage"]
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkRadioButton(
            radio_frame,
            text="Siano",
            variable=self._fixed_var,
            value="hay",
            fg_color=self.COLORS["hay"]
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkRadioButton(
            radio_frame,
            text="Słoma",
            variable=self._fixed_var,
            value="straw",
            fg_color=self.COLORS["straw"]
        ).grid(row=0, column=2, padx=5)
        
        # Ratio inputs
        frame_ratios = ctk.CTkFrame(left, fg_color="transparent")
        frame_ratios.pack(fill="x", pady=10)
        
        ratio_config = [
            ("hay", "Siano"),
            ("silage", "Kiszonka"),
            ("straw", "Słoma"),
            ("mineral", "Mineralna")
        ]
        
        for i, (key, name) in enumerate(ratio_config):
            self._fill_entries[key] = self._add_spinbox_ratio(frame_ratios, i, name, key)
        
        # Fill button
        fill_button = ctk.CTkButton(
            left,
            text="DOPEŁNIJ",
            command=self._calc_fill,
            font=("Roboto", 16, "bold"),
            height=45,
            fg_color="#E07A5F",
            hover_color="#C86A4F"
        )
        fill_button.pack(pady=20, fill="x")
        
        # Right panel - results
        right = ctk.CTkFrame(self._tab_fill, fg_color="#2b2b2b", corner_radius=10)
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        
        self._fill_result = self._create_result_area(right)
    
    def _load_saved_values(self) -> None:
        """Load saved values from config into UI elements."""
        # Wagon capacity
        wagon = str(self._config.get("wagon_capacity", 24000))
        self._std_wagon.set(wagon)
        self._fill_wagon.set(wagon)
        
        # Bale sizes
        bale_hay = str(self._config.get("bale_hay", 5500))
        bale_straw = str(self._config.get("bale_straw", 7500))
        bale_silage = str(self._config.get("bale_silage", 5000))
        
        # Update standard tab entries
        self._std_bale_hay.delete(0, "end")
        self._std_bale_hay.insert(0, bale_hay)
        self._std_bale_straw.delete(0, "end")
        self._std_bale_straw.insert(0, bale_straw)
        self._std_bale_silage.delete(0, "end")
        self._std_bale_silage.insert(0, bale_silage)
        
        # Update fill tab entries
        self._fill_bale_hay.delete(0, "end")
        self._fill_bale_hay.insert(0, bale_hay)
        self._fill_bale_straw.delete(0, "end")
        self._fill_bale_straw.insert(0, bale_straw)
        self._fill_bale_silage.delete(0, "end")
        self._fill_bale_silage.insert(0, bale_silage)
    
    def _save_current_values(self, entries: Dict[str, ctk.CTkEntry], wagon: str, 
                              bale_hay: str, bale_straw: str, bale_silage: str) -> None:
        """
        Save current input values to configuration.
        
        Args:
            entries: Dictionary of ratio entries.
            wagon: Wagon capacity value.
            bale_hay: Hay bale size.
            bale_straw: Straw bale size.
            bale_silage: Silage bale size.
        """
        try:
            # Save wagon capacity
            self._config.set("wagon_capacity", int(wagon))
            
            # Save bale sizes
            self._config.set("bale_hay", int(bale_hay))
            self._config.set("bale_straw", int(bale_straw))
            self._config.set("bale_silage", int(bale_silage))
            
            # Save ratios
            ratios = {}
            for key, entry in entries.items():
                ratios[key] = int(float(entry.get()))
            self._config.set_all_ratios(ratios)
            
        except ValueError:
            pass  # Ignore save errors for invalid values
    
    def _calc_standard(self) -> None:
        """Calculate standard TMR load."""
        try:
            wagon = float(self._std_wagon.get())
            bale_hay = float(self._std_bale_hay.get())
            bale_straw = float(self._std_bale_straw.get())
            bale_silage = float(self._std_bale_silage.get())
            
            percents = self._get_percents(self._std_entries)
            if not percents:
                return
            
            # Calculate needed amounts
            needed = {k: wagon * (v / 100) for k, v in percents.items()}
            
            # Save values to config
            self._save_current_values(
                self._std_entries, 
                self._std_wagon.get(),
                self._std_bale_hay.get(),
                self._std_bale_straw.get(),
                self._std_bale_silage.get()
            )
            
            # Display results
            self._std_result.configure(state="normal")
            self._std_result.delete("0.0", "end")
            self._std_result.insert(
                "0.0",
                self._format_report(wagon, needed, percents, bale_hay, bale_straw, bale_silage, "PEŁNY ZBIORNIK")
            )
            self._std_result.configure(state="disabled")
            
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadzono nieprawidłowe dane liczbowe.")
    
    def _calc_fill(self) -> None:
        """Calculate TMR based on already loaded ingredient."""
        try:
            wagon = float(self._fill_wagon.get())
            bale_hay = float(self._fill_bale_hay.get())
            bale_straw = float(self._fill_bale_straw.get())
            bale_silage = float(self._fill_bale_silage.get())
            
            base_type = self._fixed_var.get()
            base_amount = float(self._entry_fixed_amt.get())
            
            percents = self._get_percents(self._fill_entries)
            if not percents:
                return
            
            if percents[base_type] <= 0:
                messagebox.showerror("Błąd", f"Procent dla {self.LABELS[base_type]} musi być większy od 0.")
                return
            
            # Calculate total needed based on fixed ingredient
            total_needed = base_amount / (percents[base_type] / 100)
            
            if total_needed > wagon:
                messagebox.showerror(
                    "Przepełnienie",
                    f"Wymagane {total_needed:,.0f} L, a pojemność to tylko {wagon:,.0f} L"
                )
                return
            
            # Calculate needed amounts
            needed = {k: total_needed * (v / 100) for k, v in percents.items()}
            
            # Save values to config
            self._save_current_values(
                self._fill_entries,
                self._fill_wagon.get(),
                self._fill_bale_hay.get(),
                self._fill_bale_straw.get(),
                self._fill_bale_silage.get()
            )
            
            # Display results
            base_label = self.LABELS[base_type]
            self._fill_result.configure(state="normal")
            self._fill_result.delete("0.0", "end")
            self._fill_result.insert(
                "0.0",
                self._format_report(
                    total_needed, needed, percents, 
                    bale_hay, bale_straw, bale_silage,
                    f"BAZA: {base_amount:,.0f} L {base_label}"
                )
            )
            self._fill_result.configure(state="disabled")
            
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadzono nieprawidłowe dane liczbowe.")
    
    def _on_back_click(self) -> None:
        """Handle back button click."""
        self._app.show_menu()
