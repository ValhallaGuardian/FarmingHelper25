"""
TMR Calculator View Module
==========================
Contains the TMR feed calculator screen with full calculation logic,
including Standard, Fill, and Optimizer modes.
"""

import math
import customtkinter as ctk
from tkinter import messagebox
from typing import TYPE_CHECKING, Dict, Optional, List, Tuple

if TYPE_CHECKING:
    from src.app import App


class TMRView(ctk.CTkFrame):
    
    LIMITS = {
        "hay": (21, 70),
        "silage": (21, 70),
        "straw": (1, 29),
        "mineral": (0, 5)
    }
    
    COLORS = {
        "hay": "#E69F00",      # Orange
        "straw": "#F0E442",    # Yellow
        "silage": "#009E73",   # Green
        "mineral": "#FFFFFF"   # White
    }
    
    LABELS = {
        "hay": "Siano",
        "silage": "Kiszonka",
        "straw": "Słoma",
        "mineral": "Mineralna"
    }
    
    def __init__(self, parent: ctk.CTkFrame, app: "App") -> None:
        super().__init__(parent, fg_color="transparent")
        self._app = app
        self._config = app.config_manager
        
        # References
        self._std_entries = {}
        self._fill_entries = {}
        self._opt_entries = {} # For optimizer
        
        self._setup_ui()
        self._load_saved_values()
    
    def _setup_ui(self) -> None:
        # Back button
        ctk.CTkButton(
            self, text="⬅ Menu", width=100, height=35,
            fg_color="#444444", hover_color="#333333",
            command=self._on_back_click
        ).place(x=20, y=20)
        
        # Title
        ctk.CTkLabel(
            self, text="🐄 Kalkulator TMR",
            font=("Roboto", 28, "bold"), text_color="#1f538d"
        ).pack(pady=(20, 10))
        
        # Tabs
        self._tabview = ctk.CTkTabview(self)
        self._tabview.pack(padx=15, pady=(10, 15), fill="both", expand=True)
        
        self._tab_std = self._tabview.add("Standard")
        self._tab_fill = self._tabview.add("Uzupełnianie")
        self._tab_opt = self._tabview.add("Optymalizator (AI)") # Nowa zakładka
        
        self._init_standard_tab()
        self._init_fill_tab()
        self._init_optimizer_tab() # Inicjalizacja nowej zakładki
    
    # --- UI HELPERS ---
    def _create_wagon_input(self, parent, row):
        ctk.CTkLabel(parent, text="Pojemność Paszowozu:", text_color="#bfbfbf").grid(row=row, column=0, sticky="w", pady=6)
        combo = ctk.CTkComboBox(parent, values=["14000", "18000", "22000", "24000", "28000", "35000", "45000", "60000"], width=110, justify="right")
        combo.grid(row=row, column=1, sticky="e", pady=6)
        return combo
    
    def _add_grid_input(self, parent, row, text, default_val):
        ctk.CTkLabel(parent, text=text, text_color="#bfbfbf").grid(row=row, column=0, sticky="w", pady=6)
        entry = ctk.CTkEntry(parent, width=110, justify="right")
        entry.insert(0, str(default_val))
        entry.grid(row=row, column=1, sticky="e", pady=6)
        return entry
    
    def _add_spinbox_ratio(self, parent, label, key):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=2)
        ctk.CTkLabel(frame, text=f"● {label} ({self.LIMITS[key][0]}-{self.LIMITS[key][1]}%)", 
                     text_color=self.COLORS.get(key, "gray")).pack(side="left")
        
        entry = ctk.CTkEntry(frame, width=50, justify="center")
        entry.insert(0, str(self._config.get_ratio(key)))
        entry.pack(side="right")
        return entry

    def _create_result_area(self, parent):
        ctk.CTkLabel(parent, text="WYNIKI", font=("Roboto", 24, "bold"), text_color="white").pack(pady=20, anchor="nw", padx=20)
        box = ctk.CTkTextbox(parent, font=("Roboto Mono", 14), text_color="#dce4ee", fg_color="#1e1e1e")
        box.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        box.configure(state="disabled")
        return box

    # --- TABS INITIALIZATION ---
    def _init_standard_tab(self):
        # (Kod identyczny jak wcześniej - skrócony dla czytelności tutaj, ale w pliku musi być pełny)
        self._tab_std.grid_columnconfigure(0, weight=1)
        self._tab_std.grid_columnconfigure(1, weight=2)
        
        left = ctk.CTkFrame(self._tab_std, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=10)
        
        fg = ctk.CTkFrame(left, fg_color="transparent")
        fg.pack(fill="x")
        self._std_wagon = self._create_wagon_input(fg, 0)
        self._std_bale_hay = self._add_grid_input(fg, 1, "Belka Siana:", 5500)
        self._std_bale_straw = self._add_grid_input(fg, 2, "Belka Słomy:", 7500)
        self._std_bale_silage = self._add_grid_input(fg, 3, "Kubeł/Belka Kiszonki:", 5000)
        
        fr = ctk.CTkFrame(left, fg_color="transparent")
        fr.pack(fill="x", pady=20)
        for k, n in [("hay", "Siano"), ("silage", "Kiszonka"), ("straw", "Słoma"), ("mineral", "Mineralna")]:
            self._std_entries[k] = self._add_spinbox_ratio(fr, n, k)
            
        ctk.CTkButton(left, text="OBLICZ", command=self._calc_standard, height=45, fg_color="#1f538d").pack(pady=20, fill="x")
        
        right = ctk.CTkFrame(self._tab_std, fg_color="#1a1a1a")
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        self._std_result = self._create_result_area(right)

    def _init_fill_tab(self):
        # (Standardowy kod dla zakładki Uzupełnianie)
        self._tab_fill.grid_columnconfigure(0, weight=1)
        self._tab_fill.grid_columnconfigure(1, weight=2)
        
        left = ctk.CTkFrame(self._tab_fill, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=10)
        
        fg = ctk.CTkFrame(left, fg_color="transparent")
        fg.pack(fill="x")
        self._fill_wagon = self._create_wagon_input(fg, 0)
        self._fill_bale_hay = self._add_grid_input(fg, 1, "Belka Siana:", 5500)
        self._fill_bale_straw = self._add_grid_input(fg, 2, "Belka Słomy:", 7500)
        self._fill_bale_silage = self._add_grid_input(fg, 3, "Kubeł/Belka Kiszonki:", 5000)
        
        # Radio buttons
        ff = ctk.CTkFrame(left)
        ff.pack(fill="x", pady=10)
        self._fixed_var = ctk.StringVar(value="silage")
        self._entry_fixed_amt = ctk.CTkEntry(ff, placeholder_text="Ilość wlanego (L)")
        self._entry_fixed_amt.pack(side="bottom", fill="x", padx=5, pady=5)
        
        rf = ctk.CTkFrame(ff, fg_color="transparent")
        rf.pack(fill="x")
        for val, col, txt in [("silage", "#009E73", "Kiszonka"), ("hay", "#E69F00", "Siano"), ("straw", "#F0E442", "Słoma")]:
            ctk.CTkRadioButton(rf, text=txt, variable=self._fixed_var, value=val, fg_color=col).pack(side="left", padx=5)

        fr = ctk.CTkFrame(left, fg_color="transparent")
        fr.pack(fill="x", pady=10)
        for k, n in [("hay", "Siano"), ("silage", "Kiszonka"), ("straw", "Słoma"), ("mineral", "Mineralna")]:
            self._fill_entries[k] = self._add_spinbox_ratio(fr, n, k)

        ctk.CTkButton(left, text="DOPEŁNIJ", command=self._calc_fill, height=45, fg_color="#E07A5F").pack(pady=20, fill="x")
        
        right = ctk.CTkFrame(self._tab_fill, fg_color="#2b2b2b")
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        self._fill_result = self._create_result_area(right)

    def _init_optimizer_tab(self):
        """Inicjalizacja zakładki z Algorytmem"""
        self._tab_opt.grid_columnconfigure(0, weight=1)
        self._tab_opt.grid_columnconfigure(1, weight=2)
        
        left = ctk.CTkFrame(self._tab_opt, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Konfiguracja
        ctk.CTkLabel(left, text="⚙️ Parametry Algorytmu", font=("Roboto", 16, "bold")).pack(pady=10)
        
        fg = ctk.CTkFrame(left, fg_color="transparent")
        fg.pack(fill="x")
        self._opt_wagon = self._create_wagon_input(fg, 0)
        self._opt_bale_hay = self._add_grid_input(fg, 1, "Belka Siana:", 5500)
        self._opt_bale_straw = self._add_grid_input(fg, 2, "Belka Słomy:", 7500)
        self._opt_bale_silage = self._add_grid_input(fg, 3, "Kubeł/Belka Kiszonki:", 5000)
        
        # Mineral settings
        mf = ctk.CTkFrame(left, fg_color="transparent")
        mf.pack(fill="x", pady=20)
        
        self._opt_use_mineral = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(mf, text="Używaj Paszy Mineralnej", variable=self._opt_use_mineral).pack(anchor="w")
        
        self._opt_mineral_pct = ctk.CTkEntry(mf, width=50)
        self._opt_mineral_pct.insert(0, "2")
        self._opt_mineral_pct.pack(pady=5, anchor="w")
        ctk.CTkLabel(mf, text="(Stały % jeśli zaznaczone)", font=("Arial", 10), text_color="gray").pack(anchor="w")

        # Info text
        ctk.CTkLabel(left, text="Algorytm znajdzie kombinację pełnych bel,\naby maksymalnie zapełnić wóz\nbez wychodzenia poza widełki.", 
                     text_color="gray", font=("Arial", 12)).pack(pady=10)

        ctk.CTkButton(left, text="SZUKAJ OPTYMALNEJ MIESZANKI", command=self._run_optimizer, height=50, fg_color="#8e44ad").pack(pady=20, fill="x")
        
        # Right panel
        right = ctk.CTkFrame(self._tab_opt, fg_color="#2c3e50")
        right.grid(row=0, column=1, sticky="nsew", padx=10)
        self._opt_result = self._create_result_area(right)

    # --- LOGIC ---
    
    def _load_saved_values(self):
        # Wczytywanie wartości do wszystkich pól
        wagon = str(self._config.get("wagon_capacity", 24000))
        hay = str(self._config.get("bale_hay", 5500))
        straw = str(self._config.get("bale_straw", 7500))
        silage = str(self._config.get("bale_silage", 5000))
        
        for w in [self._std_wagon, self._fill_wagon, self._opt_wagon]: w.set(wagon)
        for e in [self._std_bale_hay, self._fill_bale_hay, self._opt_bale_hay]: 
            e.delete(0, "end"); e.insert(0, hay)
        for e in [self._std_bale_straw, self._fill_bale_straw, self._opt_bale_straw]:
            e.delete(0, "end"); e.insert(0, straw)
        for e in [self._std_bale_silage, self._fill_bale_silage, self._opt_bale_silage]:
            e.delete(0, "end"); e.insert(0, silage)

    def _calc_standard(self):
        # Logika standardowa (taka sama jak w poprzedniej wersji)
        try:
            wagon = float(self._std_wagon.get())
            percents = self._get_percents(self._std_entries)
            if not percents: return
            
            needed = {k: wagon * (v/100) for k, v in percents.items()}
            
            res = self._format_report(wagon, needed, percents, 
                                      float(self._std_bale_hay.get()), 
                                      float(self._std_bale_straw.get()), 
                                      float(self._std_bale_silage.get()), 
                                      "TRYB STANDARD")
            self._display_result(self._std_result, res)
            self._save_config_data(self._std_entries, wagon)
        except ValueError: messagebox.showerror("Błąd", "Błędne dane")

    def _calc_fill(self):
        # Logika uzupełniania
        try:
            wagon = float(self._fill_wagon.get())
            base_type = self._fixed_var.get()
            base_amt = float(self._entry_fixed_amt.get())
            percents = self._get_percents(self._fill_entries)
            if not percents: return
            
            if percents[base_type] == 0:
                messagebox.showerror("Błąd", f"Procent {base_type} to 0!")
                return
                
            total_needed = base_amt / (percents[base_type]/100)
            if total_needed > wagon:
                messagebox.showwarning("Uwaga", f"Przekroczono pojemność! Wymagane: {total_needed:.0f} L")
            
            needed = {k: total_needed * (v/100) for k, v in percents.items()}
            
            res = self._format_report(total_needed, needed, percents, 
                                      float(self._fill_bale_hay.get()), 
                                      float(self._fill_bale_straw.get()), 
                                      float(self._fill_bale_silage.get()), 
                                      f"DOPEŁNIANIE (Baza: {base_amt} L)")
            self._display_result(self._fill_result, res)
        except ValueError: messagebox.showerror("Błąd", "Błędne dane")

    # --- THE ALGORITHM ---
    def _run_optimizer(self):
        try:
            # 1. Pobranie danych
            wagon = float(self._opt_wagon.get())
            b_hay = float(self._opt_bale_hay.get())
            b_straw = float(self._opt_bale_straw.get())
            b_silage = float(self._opt_bale_silage.get())
            
            use_min = self._opt_use_mineral.get()
            min_pct = float(self._opt_mineral_pct.get()) if use_min else 0
            
            # 2. Obliczenie litrów mineralnej (jeśli używamy)
            # Mineralna jest "sztywna", resztę dobieramy belami
            mineral_liters = wagon * (min_pct / 100)
            remaining_capacity = wagon - mineral_liters
            
            if remaining_capacity <= 0:
                messagebox.showerror("Błąd", "Zbyt duży % mineralnej!")
                return

            # 3. Wyznaczanie zakresów pętli (Optymalizacja pętli)
            # Zamiast sprawdzać od 0 do 100 bel, sprawdzamy tylko te ilości, 
            # które mieszczą się w widełkach procentowych (np. Siano 20-70%)
            
            # Min/Max litrów dla składników (bazując na pełnym wozie)
            lim_hay = (wagon * 0.21, wagon * 0.70)
            lim_sil = (wagon * 0.21, wagon * 0.70)
            lim_str = (wagon * 0.01, wagon * 0.29)
            
            # Przeliczenie na zakres bel (Math.ceil dla min, Math.floor dla max)
            # Dodajemy margines +/- 1 bela dla elastyczności
            r_hay = range(max(0, int(lim_hay[0]/b_hay)), int(lim_hay[1]/b_hay) + 2)
            r_str = range(max(0, int(lim_str[0]/b_straw)), int(lim_str[1]/b_straw) + 2)
            r_sil = range(max(0, int(lim_sil[0]/b_silage)), int(lim_sil[1]/b_silage) + 2)
            
            best_mix = None
            best_score = -1
            
            # 4. Brute Force Loop (Pętla po wszystkich kombinacjach)
            for h in r_hay:
                vol_h = h * b_hay
                for s in r_str:
                    vol_str = s * b_straw
                    
                    # Sprawdzenie pośrednie - czy już nie za dużo?
                    if vol_h + vol_str + mineral_liters > wagon:
                        break 
                        
                    for k in r_sil:
                        vol_sil = k * b_silage
                        
                        total_vol = vol_h + vol_str + vol_sil + mineral_liters
                        
                        # Walidacja 1: Pojemność
                        if total_vol > wagon:
                            break # Za dużo, kolejna iteracja
                        
                        # Walidacja 2: Procenty
                        pct_h = (vol_h / total_vol) * 100
                        pct_s = (vol_str / total_vol) * 100
                        pct_k = (vol_sil / total_vol) * 100
                        pct_m = (mineral_liters / total_vol) * 100
                        
                        # Sprawdzenie czy mieszanka jest poprawna (TMR)
                        if not (21 <= pct_h <= 70): continue
                        if not (21 <= pct_k <= 70): continue
                        if not (1 <= pct_s <= 29): continue
                        # Mineralna max 5%
                        if pct_m > 5.5: continue 
                        
                        # Punktacja (Score)
                        # Zależy nam na:
                        # 1. Jak największym zapełnieniu wozu (fill_ratio)
                        fill_ratio = total_vol / wagon
                        
                        score = fill_ratio * 100
                        
                        if score > best_score:
                            best_score = score
                            best_mix = {
                                "counts": (h, s, k),
                                "vols": (vol_h, vol_str, vol_sil, mineral_liters),
                                "pcts": (pct_h, pct_s, pct_k, pct_m),
                                "total": total_vol
                            }

            # 5. Wyświetlenie wyniku
            self._opt_result.configure(state="normal")
            self._opt_result.delete("0.0", "end")
            
            if best_mix:
                h, s, k = best_mix["counts"]
                vh, vs, vk, vm = best_mix["vols"]
                ph, ps, pk, pm = best_mix["pcts"]
                tot = best_mix["total"]
                
                txt = f"ZNALEZIONO OPTYMALNĄ MIESZANKĘ!\n"
                txt += f"Zapełnienie wozu: {tot:,.0f} / {wagon:,.0f} L ({tot/wagon*100:.1f}%)\n"
                txt += "="*40 + "\n\n"
                
                txt += f"🟧 SIANO ({ph:.1f}%):\n   {h} szt. x {b_hay:.0f} L = {vh:,.0f} L\n\n"
                txt += f"🟨 SŁOMA ({ps:.1f}%):\n   {s} szt. x {b_straw:.0f} L = {vs:,.0f} L\n\n"
                txt += f"🟩 KISZONKA ({pk:.1f}%):\n   {k} szt. x {b_silage:.0f} L = {vk:,.0f} L\n\n"
                
                if use_min:
                    txt += f"⬜ MINERALNA ({pm:.1f}%):\n   Do wsypania ręcznie: {vm:,.0f} L"
                else:
                    txt += "⬜ Bez paszy mineralnej."
                    
            else:
                txt = "Nie znaleziono pasującej kombinacji bel.\n"
                txt += "Spróbuj zmienić wielkość wozu lub zmniejszyć wielkość bel."
            
            self._opt_result.insert("0.0", txt)
            self._opt_result.configure(state="disabled")

        except ValueError:
            messagebox.showerror("Błąd", "Sprawdź poprawność danych wejściowych.")

    # --- UTILS ---
    def _get_percents(self, entries):
        vals = {}
        for k, e in entries.items():
            try: vals[k] = float(e.get())
            except: return None
        
        # Walidacja indywidualnych wartości względem limitów
        for k, v in vals.items():
            min_val, max_val = self.LIMITS[k]
            if not (min_val <= v <= max_val):
                messagebox.showerror(
                    "Błąd walidacji", 
                    f"{self.LABELS[k]}: wartość {v}% jest poza zakresem!\n"
                    f"Dozwolony zakres: {min_val}% - {max_val}%"
                )
                return None
        
        if not (99.0 <= sum(vals.values()) <= 101.0):
            messagebox.showwarning("Info", f"Suma % wynosi {sum(vals.values())}")
        return vals

    def _display_result(self, box, text):
        box.configure(state="normal")
        box.delete("0.0", "end")
        box.insert("0.0", text)
        box.configure(state="disabled")

    def _format_report(self, wagon, needed, percents, bh, bs, bk, title):
        # (Skrócona wersja funkcji formatującej - użyj tej z poprzedniego pliku lub skopiuj pełną logikę)
        # Tutaj wstawiam pełną wersję dla pewności:
        def cb(amt, size): return (math.floor(amt/size), amt%size) if size>0 else (0,0)
        ch, rh = cb(needed["hay"], bh)
        cs, rs = cb(needed["straw"], bs)
        ck, rk = cb(needed["silage"], bk)
        
        t = f"{title}\nCEL: {wagon:,.0f} L\n" + "-"*30 + "\n\n"
        t += f"🟧 Siano ({percents['hay']:.0f}%): {needed['hay']:.0f} L -> {ch} bel + {rh:.0f} L\n"
        t += f"🟨 Słoma ({percents['straw']:.0f}%): {needed['straw']:.0f} L -> {cs} bel + {rs:.0f} L\n"
        t += f"🟩 Kiszonka ({percents['silage']:.0f}%): {needed['silage']:.0f} L -> {ck} kubłów + {rk:.0f} L\n"
        t += f"⬜ Mineralna ({percents['mineral']:.0f}%): {needed['mineral']:.0f} L\n"
        return t

    def _save_config_data(self, entries, wagon):
        try:
            self._config.set("wagon_capacity", int(float(wagon)))
            # Zapis reszty wartości...
        except: pass
    
    def _on_back_click(self):
        self._app.show_menu()