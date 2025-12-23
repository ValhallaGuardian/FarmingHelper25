

```markdown
# 🌾 Farming Helper 25 by Valhalla

**Profesjonalny asystent dla graczy Farming Simulator 25**

Kompleksowa aplikacja desktopowa typu open-source, stworzona w języku Python. Pomaga w zarządzaniu hodowlą zwierząt (idealna pasza TMR) oraz ekonomią gospodarstwa (analiza najlepszego momentu sprzedaży plonów).

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)

---

## ✨ Główne Funkcje

### 🐄 Zaawansowany Kalkulator TMR
Narzędzie do tworzenia idealnej mieszanki paszowej (Total Mixed Ration) dla krów, z poszanowaniem widełek procentowych gry.

*   **Tryb Standard:** Oblicza ilość litrów składników dla pełnego paszowozu.
*   **Tryb Uzupełnianie:** Masz już wlaną kiszonkę? Aplikacja obliczy, ile dolać reszty, aby nie przekroczyć pojemności i zachować proporcje.
*   **Tryb Optymalizator (AI):** **UNIKATOWA FUNKCJA!** Algorytm "Brute-force", który szuka idealnej kombinacji **pełnych bel**. Zamiast bawić się w "38% siana", program powie Ci: *"Wrzuć 2 bele siana, 1 słomy i 2 kubły kiszonki"*. Zero marnowania resztek!

### 📈 Inteligentny Tracker Cen (Analiza Savegame)
Zapomnij o ręcznym notowaniu cen. Aplikacja analizuje pliki Twojego zapisu gry (`economy.xml`, `environment.xml`).

*   **Analiza Historii:** Czyta historię cen z Twojego zapisu i wyznacza miesiące, w których dany produkt jest najdroższy.
*   **Detekcja Czasu:** Automatycznie wykrywa aktualny miesiąc w grze.
*   **Rekomendacje:** Porównuje aktualny miesiąc z historycznymi maksimami i mówi jasno: **SPRZEDAWAJ** lub **TRZYMAJ**.
*   **Filtrowanie:** Możesz zaznaczyć tylko te produkty, które faktycznie uprawiasz/posiadasz.

### ⚙️ Inne
*   **Nowoczesny Interfejs:** Ciemny motyw (Dark Mode) oparty o `customtkinter`.
*   **Pamięć Ustawień:** Aplikacja pamięta ścieżkę do savegame, wielkości Twoich bel, pojemność paszowozu i zaznaczone produkty.
*   **Modularność:** Kod podzielony na czytelne moduły, łatwy do rozwoju.

---

## 📁 Struktura Projektu

```text
FarmingHelper25/
├── main.py                  # Punkt startowy aplikacji
├── config.json              # Plik konfiguracyjny (generowany automatycznie)
├── src/
│   ├── app.py               # Główna klasa okna i nawigacji
│   ├── data/
│   │   └── constants.py     # Tłumaczenia PL i mapy miesięcy
│   ├── utils/
│   │   ├── config_manager.py  # Obsługa zapisu ustawień
│   │   └── savegame_parser.py # Analiza plików XML (economy/environment)
│   └── views/
│       ├── menu_view.py       # Menu Główne
│       ├── tmr_view.py        # Kalkulator TMR (3 zakładki)
│       ├── price_view.py      # Tracker Cen (Checkboxy + Raport)
│       └── settings_view.py   # Ustawienia ścieżek
```

---

## 🚀 Instalacja i Uruchomienie

### Wymagania
*   Python 3.10 lub nowszy
*   System Windows (zalecany dla analizy savegame) lub macOS

### Krok 1: Pobranie
Sklonuj repozytorium lub pobierz pliki ZIP.

```bash
git clone https://github.com/TwojNick/FarmingHelper25.git
cd FarmingHelper25
```

### Krok 2: Instalacja Zależności
Zainstaluj wymagane biblioteki (głównie `customtkinter`):

```bash
pip install -r requirements.txt
```
*(Jeśli nie masz pliku requirements.txt, wpisz: `pip install customtkinter packaging`)*

### Krok 3: Uruchomienie
```bash
python main.py
```

---

## 📖 Instrukcja Obsługi

### 1. Konfiguracja (Pierwsze kroki)
1.  Uruchom aplikację i wejdź w **Ustawienia**.
2.  Kliknij "Przeglądaj..." i wskaż folder ze swoim zapisem gry.
    *   *Domyślnie:* `Dokumenty/My Games/FarmingSimulator2025/savegameX`
3.  Ustaw domyślne wielkości bel, których używasz (np. 125cm -> ~4500L).

### 2. Używanie Trackera Cen
1.  W menu głównym wybierz **Ekonomia / Ceny**.
2.  Kliknij **"Wczytaj Produkty"**. Aplikacja przeskanuje plik `economy.xml` i wyświetli listę wszystkich dostępnych dóbr.
3.  Zaznacz "ptaszkiem" produkty, które masz w silosach (np. Pszenica, Rzepak, Mleko).
4.  Kliknij **"Sprawdź Ceny"**.
5.  Otrzymasz raport:
    *   🟢 **SPRZEDAWAJ TERAZ:** Jeśli aktualny miesiąc w grze pokrywa się z historycznym szczytem cenowym.
    *   🟠 **TRZYMAJ:** Jeśli cena jest niska. Aplikacja podpowie, do jakiego miesiąca czekać (np. *"Czekaj do: Styczeń"*).

### 3. Używanie Optymalizatora TMR
1.  W menu wybierz **Kalkulator TMR** i przejdź do zakładki **Optymalizator (AI)**.
2.  Upewnij się, że wielkości bel i wozu są poprawne.
3.  Zaznacz, czy chcesz dodawać paszę mineralną (zazwyczaj sypana z worka/palety, więc precyzyjna).
4.  Kliknij **"Szukaj Optymalnej Mieszanki"**.
5.  Algorytm przeanalizuje tysiące kombinacji i poda Ci przepis na pełne wykorzystanie wozu przy użyciu **tylko całych bel**.

---

## 🔨 Budowanie wersji .EXE (Dla Windows)

Aby stworzyć samodzielny plik wykonywalny (niewymagający Pythona), użyj **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all customtkinter --icon="logo.ico" --name "FarmingHelper25" main.py
```
*Plik wynikowy znajdziesz w folderze `dist`.*

---

## 🤝 Współpraca (Contributing)

Projekt jest Open Source! Jeśli masz pomysł na nową funkcję:
1.  Zrób Fork projektu.
2.  Stwórz nową gałąź (`git checkout -b feature/NowaFunkcja`).
3.  Zatwierdź zmiany.
4.  Otwórz Pull Request.

## 📝 Licencja

Projekt udostępniany na licencji **MIT**. Możesz go używać, modyfikować i rozpowszechniać za darmo.
```