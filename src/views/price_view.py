"""
Price View Module
=================
XML-based Price Tracker. Reads savegame data to analyze economy.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING, List

from src.utils.savegame_parser import SavegameParser
from src.data.constants import TRANSLATIONS_PL, INDEX_TO_MONTH

if TYPE_CHECKING:
    from src.app import App

class PriceView(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, app: "App") -> None:
        super().__init__(parent, fg_color="transparent")
        self._app = app
        self._config = app.config_manager
        
        self._checkboxes = {}
        self._available_products = []
        
        self._setup_ui()
        
        # Auto-load products if path exists
        if self._config.get("save_game_path"):
            self._load_products_from_xml(silent=True)

    def _setup_ui(self) -> None:
        # Layout: 2 Columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT PANEL (Controls) ---
        left_panel = ctk.CTkFrame(self, corner_radius=10)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Back Button
        ctk.CTkButton(
            left_panel, text="⬅ Menu", width=80, fg_color="#444", 
            command=self._on_back_click
        ).pack(anchor="w", padx=10, pady=10)
        
        ctk.CTkLabel(left_panel, text="USTAWIENIA GRY", font=("Roboto", 18, "bold"), text_color="#27ae60").pack(pady=(10, 5))
        
        # Path Info
        self._lbl_path = ctk.CTkLabel(
            left_panel, 
            text=self._get_short_path(self._config.get("save_game_path", "")), 
            font=("Roboto", 11), text_color="gray"
        )
        self._lbl_path.pack(pady=5)
        
        ctk.CTkButton(left_panel, text="Zmień folder savegame...", command=self._select_save_folder, fg_color="#555").pack(pady=5, padx=20, fill="x")
        
        # Load Button
        ctk.CTkButton(
            left_panel, text="🔄 WCZYTAJ PRODUKTY", 
            font=("Roboto", 12, "bold"), height=40, fg_color="#d35400", hover_color="#a04000", 
            command=self._load_products_from_xml
        ).pack(pady=20, padx=20, fill="x")
        
        # Check Prices Button
        self._btn_check = ctk.CTkButton(
            left_panel, text="🔍 SPRAWDŹ CENY", 
            font=("Roboto", 16, "bold"), height=50, fg_color="#27ae60", hover_color="#1e8449", 
            command=self._check_prices
        )
        self._btn_check.pack(pady=20, padx=20, fill="x")
        
        self._lbl_game_info = ctk.CTkLabel(left_panel, text="Wybierz save i wczytaj produkty.", font=("Roboto", 12), text_color="gray")
        self._lbl_game_info.pack(side="bottom", pady=20)

        # --- RIGHT PANEL (List) ---
        right_container = ctk.CTkFrame(self, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Search Bar
        search_frame = ctk.CTkFrame(right_container, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 5))
        
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Arial", 16)).pack(side="left", padx=5)
        ctk.CTkEntry(search_frame, placeholder_text="Szukaj produktu...", textvariable=self._search_var).pack(side="left", fill="x", expand=True)
        ctk.CTkButton(search_frame, text="X", width=30, fg_color="#444", command=lambda: self._search_var.set("")).pack(side="left", padx=5)

        # Tools
        tools_frame = ctk.CTkFrame(right_container, fg_color="transparent", height=30)
        tools_frame.pack(fill="x", pady=(0, 5))
        self._lbl_count = ctk.CTkLabel(tools_frame, text="Produkty: 0", font=("Roboto", 12), text_color="gray")
        self._lbl_count.pack(side="left")
        ctk.CTkButton(tools_frame, text="Odznacz wszystko", width=120, height=24, fg_color="#c0392b", command=self._deselect_all).pack(side="right")

        # Scrollable List
        self._right_panel = ctk.CTkScrollableFrame(right_container, label_text="TWOJE MAGAZYNY (Zaznacz co posiadasz)")
        self._right_panel.pack(fill="both", expand=True)

    def _get_short_path(self, path: str) -> str:
        if not path: return "Nie wybrano"
        if len(path) > 30: return "..." + path[-27:]
        return path

    def _select_save_folder(self) -> None:
        path = filedialog.askdirectory(title="Wybierz folder savegame")
        if path:
            self._config.set("save_game_path", path)
            self._lbl_path.configure(text=self._get_short_path(path))
            self._load_products_from_xml()

    def _load_products_from_xml(self, silent: bool = False) -> None:
        path = self._config.get("save_game_path")
        if not path:
            if not silent: messagebox.showerror("Błąd", "Wybierz najpierw folder savegame!")
            return

        parser = SavegameParser(path)
        products = parser.get_available_products()
        
        if not products:
            if not silent: messagebox.showwarning("Pusto", "Nie znaleziono produktów w economy.xml lub plik nie istnieje.")
            return

        self._available_products = products
        self._search_var.set("")
        self._refresh_checkboxes()
        
        if not silent: messagebox.showinfo("Sukces", f"Wczytano {len(products)} produktów!")

    def _refresh_checkboxes(self, filter_text: str = "") -> None:
        for widget in self._right_panel.winfo_children():
            widget.destroy()
        self._checkboxes = {}
        
        owned_list = self._config.get("owned_products", [])
        visible_count = 0
        
        for product in self._available_products:
            # Translate for display
            display_name = TRANSLATIONS_PL.get(product, product.replace("_", " ").title())
            
            if filter_text.lower() not in display_name.lower():
                continue
            
            visible_count += 1
            is_owned = product in owned_list
            var = ctk.BooleanVar(value=is_owned)
            
            cb = ctk.CTkCheckBox(
                self._right_panel, 
                text=display_name, 
                variable=var, 
                command=lambda p=product: self._save_product_click(p)
            )
            cb.pack(anchor="w", pady=5, padx=10)
            self._checkboxes[product] = var
            
        self._lbl_count.configure(text=f"Wyświetlono: {visible_count}")

    def _save_product_click(self, product_key: str) -> None:
        is_checked = self._checkboxes[product_key].get()
        owned_list = self._config.get("owned_products", [])
        
        if is_checked and product_key not in owned_list:
            owned_list.append(product_key)
        elif not is_checked and product_key in owned_list:
            owned_list.remove(product_key)
            
        self._config.set("owned_products", owned_list)

    def _on_search_change(self, *args) -> None:
        self._refresh_checkboxes(self._search_var.get())

    def _deselect_all(self) -> None:
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz odznaczyć wszystko?"):
            self._config.set("owned_products", [])
            self._refresh_checkboxes(self._search_var.get())

    def _check_prices(self) -> None:
        path = self._config.get("save_game_path")
        if not path: return

        parser = SavegameParser(path)
        current_month_idx = parser.get_current_month_index()
        
        if current_month_idx is None:
            messagebox.showerror("Błąd", "Nie udało się ustalić miesiąca (brak environment.xml).")
            return
            
        current_month_name = INDEX_TO_MONTH.get(current_month_idx, "Nieznany")
        self._lbl_game_info.configure(text=f"W grze: {current_month_name}")

        owned = self._config.get("owned_products", [])
        seasonality = parser.analyze_economy_history()
        
        hits = []
        misses = []
        
        for prod in owned:
            best_months = seasonality.get(prod, [])
            prod_pl = TRANSLATIONS_PL.get(prod, prod.title())
            
            if not best_months:
                misses.append(f"{prod_pl} (Brak danych)")
                continue
                
            if current_month_idx in best_months:
                hits.append(prod_pl)
            else:
                # Calculate next best month
                future_months = [m for m in best_months if m > current_month_idx]
                next_idx = future_months[0] if future_months else best_months[0]
                next_name = INDEX_TO_MONTH.get(next_idx, "?")
                misses.append(f"{prod_pl} (Czekaj do: {next_name})")
        
        self._show_report_popup(hits, misses, current_month_name)

    def _show_report_popup(self, hits: List[str], misses: List[str], current_month: str) -> None:
        popup = ctk.CTkToplevel(self)
        popup.title("Raport Sprzedaży")
        popup.geometry("500x600")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text=f"MIESIĄC W GRZE: {current_month.upper()}", font=("Roboto", 20, "bold"), text_color="#3B8ED0").pack(pady=20)

        if hits:
            frame_hits = ctk.CTkFrame(popup, fg_color="#1e8449")
            frame_hits.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(frame_hits, text="💲 SPRZEDAWAJ TERAZ! 💲", font=("Roboto", 16, "bold"), text_color="white").pack(pady=5)
            for item in hits:
                ctk.CTkLabel(frame_hits, text=f"• {item}", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20)
            ctk.CTkLabel(frame_hits, text=" ", font=("Arial", 5)).pack()
        else:
            ctk.CTkLabel(popup, text="Brak idealnych okazji w tym miesiącu.", text_color="gray").pack(pady=5)

        if misses:
            frame_miss = ctk.CTkFrame(popup, fg_color="#2b2b2b")
            frame_miss.pack(fill="both", expand=True, padx=20, pady=10)
            ctk.CTkLabel(frame_miss, text="TRZYMAJ W MAGAZYNIE:", font=("Roboto", 14, "bold"), text_color="#e67e22").pack(pady=10)
            scroll = ctk.CTkScrollableFrame(frame_miss, fg_color="transparent")
            scroll.pack(fill="both", expand=True)
            for item in misses:
                ctk.CTkLabel(scroll, text=f"• {item}", font=("Roboto", 12)).pack(anchor="w", padx=10)

    def _on_back_click(self) -> None:
        self._app.show_menu()