# Farming Helper 25 by Valhalla

🌾 **Profesjonalny asystent dla Farming Simulator 25** 🌾

Modularna aplikacja desktopowa do obliczania optymalnego składu paszy TMR (Total Mixed Ration) dla bydła.

## ✨ Funkcje

- **Kalkulator TMR** - Oblicza dokładne proporcje składników paszy
  - Tryb Standard - pełne załadowanie paszowozu
  - Tryb Uzupełnianie - dopełnienie na podstawie już załadowanego składnika
- **Persystencja ustawień** - Zapamiętuje ostatnie wartości
- **Konfigurowalne rozmiary bel** - Siano, słoma, kiszonka
- **Intuicyjny interfejs** - Ciemny motyw, przyjazny dla gracza

## 📁 Struktura projektu

```
FarmingHelper25/
├── main.py                  # Punkt wejścia aplikacji
├── config.json              # Ustawienia użytkownika (auto-generowany)
├── requirements.txt         # Zależności Python
├── README.md                # Ten plik
└── src/
    ├── __init__.py
    ├── app.py               # Główna klasa aplikacji
    ├── utils/
    │   ├── __init__.py
    │   └── config_manager.py  # Zarządzanie konfiguracją JSON
    └── views/
        ├── __init__.py
        ├── menu_view.py       # Ekran menu głównego
        ├── tmr_view.py        # Kalkulator TMR
        └── settings_view.py   # Ekran ustawień
```

## 🚀 Instalacja

### Wymagania
- Python 3.8+
- customtkinter

### Kroki instalacji

1. Sklonuj repozytorium:
```bash
git clone https://github.com/your-username/FarmingHelper25.git
cd FarmingHelper25
```

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. Uruchom aplikację:
```bash
python main.py
```

## 📊 Jak używać kalkulatora TMR

### Tryb Standard
1. Ustaw pojemność paszowozu
2. Wprowadź rozmiary bel (siano, słoma, kiszonka)
3. Dostosuj proporcje składników (suma = 100%)
4. Kliknij **OBLICZ**

### Tryb Uzupełnianie
1. Wybierz co już wlałeś (kiszonka/siano/słoma)
2. Wprowadź ilość w litrach
3. Dostosuj docelowe proporcje
4. Kliknij **DOPEŁNIJ**

## ⚙️ Konfiguracja

Ustawienia są zapisywane automatycznie w pliku `config.json`:

| Parametr | Domyślna wartość | Opis |
|----------|------------------|------|
| `wagon_capacity` | 24000 | Pojemność paszowozu (L) |
| `bale_hay` | 5500 | Rozmiar belki siana (L) |
| `bale_straw` | 7500 | Rozmiar belki słomy (L) |
| `bale_silage` | 5000 | Rozmiar belki/kubła kiszonki (L) |
| `ratios.hay` | 38 | % siana w TMR |
| `ratios.silage` | 30 | % kiszonki w TMR |
| `ratios.straw` | 30 | % słomy w TMR |
| `ratios.mineral` | 2 | % paszy mineralnej w TMR |

## 🎨 Zrzuty ekranu

*Aplikacja używa ciemnego motywu z niebieskim akcentem.*

## 🤝 Wkład w projekt

Zapraszamy do współtworzenia! 

1. Zforkuj repozytorium
2. Stwórz branch dla swojej funkcji (`git checkout -b feature/AmazingFeature`)
3. Zatwierdź zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Wypchnij branch (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📝 Licencja

Rozpowszechniane na licencji MIT. Zobacz plik `LICENSE` po więcej informacji.

## 👤 Autor

**Valhalla**

---

⭐ Jeśli projekt Ci się podoba, zostaw gwiazdkę! ⭐
