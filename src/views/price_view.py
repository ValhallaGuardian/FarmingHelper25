"""
Price View Module
=================
XML-based Price Tracker with Categories.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING, List, Dict

from src.utils.savegame_parser import SavegameParser
from src.data.constants import TRANSLATIONS_PL, INDEX_TO_MONTH, CATEGORY_DEFINITIONS, CATEGORY_LABELS_PL

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
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # --- LEFT PANEL (Controls) ---
        left_panel = ctk.CTkFrame(self, corner_radius=10)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkButton(left_panel, text="⬅ Menu", width=80, fg_color="#444", command=self._on_back_click).pack(anchor="w", padx=10, pady=10)
        
        ctk.CTkLabel(left_panel, text="USTAWIENIA GRY", font=("Roboto", 18, "bold"), text_color="#27ae60").pack(pady=(10, 5))
        
        self._lbl_path = ctk.CTkLabel(left_panel, text=self._get_short_path(self._config.get("save_game_path", "")), font=("Roboto", 11), text_color="gray")
        self._lbl_path.pack(pady=5)
        
        ctk.CTkButton(left_panel, text="Zmień folder savegame...", command=self._select_save_folder, fg_color="#555").pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(left_panel, text="🔄 ODŚWIEŻ LISTĘ", font=("Roboto", 12, "bold"), height=40, fg_color="#d35400", hover_color="#a04000", command=self._load_products_from_xml).pack(pady=20, padx=20, fill="x")
        
        self._btn_check = ctk.CTkButton(left_panel, text="🔍 SPRAWDŹ CENY", font=("Roboto", 16, "bold"), height=50, fg_color="#27ae60", hover_color="#1e8449", command=self._check_prices)
        self._btn_check.pack(pady=20, padx=20, fill="x")
        
        self._lbl_game_info = ctk.CTkLabel(left_panel, text="Wybierz save i wczytaj produkty.", font=("Roboto", 12), text_color="gray")
        self._lbl_game_info.pack(side="bottom", pady=20)

        # --- RIGHT PANEL (Categorized Tabs) ---
        right_container = ctk.CTkFrame(self, fg_color="transparent")
        right_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Search & Tools
        tools = ctk.CTkFrame(right_container, fg_color="transparent", height=30)
        tools.pack(fill="x", pady=(0, 5))
        
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", self._on_search_change)
        
        ctk.CTkEntry(tools, placeholder_text="🔍 Szukaj...", textvariable=self._search_var, width=200).pack(side="left")
        ctk.CTkButton(tools, text="Odznacz wszystko", width=120, height=28, fg_color="#c0392b", command=self._deselect_all).pack(side="right")

        # TAB VIEW (Categories)
        self._tabview = ctk.CTkTabview(right_container)
        self._tabview.pack(fill="both", expand=True)
        
        # Define tabs order
        self._tabs_keys = ["crops", "veggies", "animals", "production", "forage", "mods"]
        for key in self._tabs_keys:
            self._tabview.add(CATEGORY_LABELS_PL[key])

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

    def _get_category_for_product(self, filltype: str) -> str:
        """Determines category based on filltype name."""
        for cat, items in CATEGORY_DEFINITIONS.items():
            if filltype in items:
                return cat
        return "mods" # Fallback for everything else

    def _load_products_from_xml(self, silent: bool = False) -> None:
        path = self._config.get("save_game_path")
        if not path:
            if not silent: messagebox.showerror("Błąd", "Wybierz najpierw folder savegame!")
            return

        parser = SavegameParser(path)
        products = parser.get_available_products()
        
        if not products:
            if not silent: messagebox.showwarning("Pusto", "Brak produktów w economy.xml")
            return

        self._available_products = products
        self._search_var.set("")
        self._refresh_checkboxes()
        
        if not silent: messagebox.showinfo("Sukces", f"Wczytano {len(products)} produktów!")

    def _refresh_checkboxes(self, filter_text: str = "") -> None:
        # Clear all tabs first
        for key in self._tabs_keys:
            tab_name = CATEGORY_LABELS_PL[key]
            for widget in self._tabview.tab(tab_name).winfo_children():
                widget.destroy()
                
        self._checkboxes = {}
        owned_list = self._config.get("owned_products", [])
        
        # Create scrollable frames inside tabs if needed, or use grid
        # To simplify, we'll put checkboxes directly in tab frame with packing
        
        counts = {k: 0 for k in self._tabs_keys}
        
        for product in self._available_products:
            # Display name
            display_name = TRANSLATIONS_PL.get(product, product.replace("_", " ").title())
            
            # Filter
            if filter_text.lower() not in display_name.lower():
                continue
            
            # Determine category
            cat_key = self._get_category_for_product(product)
            tab_name = CATEGORY_LABELS_PL[cat_key]
            
            counts[cat_key] += 1
            
            is_owned = product in owned_list
            var = ctk.BooleanVar(value=is_owned)
            
            # Create Checkbox in appropriate tab
            cb = ctk.CTkCheckBox(
                self._tabview.tab(tab_name), 
                text=display_name, 
                variable=var, 
                command=lambda p=product: self._save_product_click(p)
            )
            # Use grid for columns or pack for list. Let's use pack for simplicity in tabs
            cb.pack(anchor="w", pady=2, padx=10)
            
            self._checkboxes[product] = var

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
        if messagebox.askyesno("Potwierdzenie", "Odznaczyć wszystko?"):
            self._config.set("owned_products", [])
            self._refresh_checkboxes(self._search_var.get())

    def _check_prices(self) -> None:
        path = self._config.get("save_game_path")
        if not path: return

        parser = SavegameParser(path)
        current_month_idx = parser.get_current_month_index()
        
        if current_month_idx is None:
            messagebox.showerror("Błąd", "Nie udało się ustalić miesiąca.")
            return
            
        current_month_name = INDEX_TO_MONTH.get(current_month_idx, "Nieznany")
        self._lbl_game_info.configure(text=f"W grze: {current_month_name}")

        owned = self._config.get("owned_products", [])
        seasonality = parser.analyze_economy_history()
        
        # Group results by category
        results = {k: {"hits": [], "misses": []} for k in self._tabs_keys}
        
        for prod in owned:
            cat = self._get_category_for_product(prod)
            prod_pl = TRANSLATIONS_PL.get(prod, prod.title())
            best_months = seasonality.get(prod, [])
            
            if not best_months:
                results[cat]["misses"].append(f"{prod_pl} (Brak danych)")
                continue
                
            if current_month_idx in best_months:
                results[cat]["hits"].append(prod_pl)
            else:
                future_months = [m for m in best_months if m > current_month_idx]
                next_idx = future_months[0] if future_months else best_months[0]
                next_name = INDEX_TO_MONTH.get(next_idx, "?")
                results[cat]["misses"].append(f"{prod_pl} ➔ {next_name}")
        
        self._show_report_popup(results, current_month_name)

    def _show_report_popup(self, results: Dict, current_month: str) -> None:
        popup = ctk.CTkToplevel(self)
        popup.title("Raport Rynkowy")
        popup.geometry("600x700")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text=f"MIESIĄC: {current_month.upper()}", font=("Roboto", 22, "bold"), text_color="#3B8ED0").pack(pady=10)
        
        scroll = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        has_any_hit = False
        
        # Iterate categories
        for cat_key in self._tabs_keys:
            data = results[cat_key]
            if not data["hits"] and not data["misses"]:
                continue
                
            cat_name = CATEGORY_LABELS_PL[cat_key]
            
            # Category Header
            ctk.CTkLabel(scroll, text=cat_name, font=("Roboto", 16, "bold"), text_color="#aaa").pack(anchor="w", pady=(15, 5))
            
            # Hits (Green)
            if data["hits"]:
                has_any_hit = True
                f_hit = ctk.CTkFrame(scroll, fg_color="#1e8449", corner_radius=6)
                f_hit.pack(fill="x", pady=2)
                for item in data["hits"]:
                    ctk.CTkLabel(f_hit, text=f"💰 {item}", font=("Roboto", 14, "bold"), text_color="white").pack(anchor="w", padx=10, pady=2)

            # Misses (Gray/Orange)
            if data["misses"]:
                f_miss = ctk.CTkFrame(scroll, fg_color="#2b2b2b", corner_radius=6)
                f_miss.pack(fill="x", pady=2)
                for item in data["misses"]:
                    ctk.CTkLabel(f_miss, text=f"⏳ {item}", font=("Roboto", 12), text_color="#bbb").pack(anchor="w", padx=10, pady=1)

        if not has_any_hit:
            ctk.CTkLabel(popup, text="Brak idealnych okazji w tym miesiącu.", text_color="gray").pack(side="bottom", pady=10)

    def _on_back_click(self) -> None:
        self._app.show_menu()