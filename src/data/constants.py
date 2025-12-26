"""
Constants Module
Contains translation maps, period definitions, and CATEGORIES.
"""

# Tłumaczenia na Polski (Twoja baza + nowe)
TRANSLATIONS_PL = {
    # UPRAWY
    "WHEAT": "Pszenica", "BARLEY": "Jęczmień", "CANOLA": "Rzepak", "OAT": "Owies",
    "MAIZE": "Kukurydza", "SUNFLOWER": "Słonecznik", "SOYBEAN": "Soja", "SORGHUM": "Sorgo",
    "POPLAR": "Topola", "GRASS": "Trawa", "OILSEEDRADISH": "Rzodkiew Oleista", "MEADOW": "Łąka",
    "SUGARCANE": "Trzcina Cukrowa", "POTATO": "Ziemniaki", "SUGARBEET": "Buraki Cukrowe",
    "COTTON": "Bawełna",
    
    # WARZYWA / SZKLARNIA / NOWE
    "GRAPE": "Winogrona", "OLIVE": "Oliwki", "TOMATO": "Pomidory", "LETTUCE": "Sałata",
    "STRAWBERRY": "Truskawki", "RICE": "Ryż", "SPINACH": "Szpinak", "PEA": "Groch",
    "BEANS": "Fasola", "GREENBEAN": "Fasolka Szparagowa", "ONION": "Cebula", "GARLIC": "Czosnek",
    "CARROT": "Marchew", "PARSNIP": "Pasternak", "RED_BEET": "Burak Ćwikłowy",
    "BEETROOT": "Burak Ćwikłowy", "PUMPKIN": "Dynia", "WATERMELON": "Arbuz", "MELON": "Melon",
    
    # PRODUKTY ZWIERZĘCE
    "EGG": "Jajka", "MILK": "Mleko", "WOOL": "Wełna", "MANURE": "Obornik",
    "LIQUIDMANURE": "Gnojowica", "DIGESTATE": "Poferment", "HONEY": "Miód",
    "GOATMILK": "Mleko Kozie", "BUFFALOMILK": "Mleko Bawole",

    # PRZETWÓRSTWO / INNE
    "FLOUR": "Mąka", "BREAD": "Chleb", "CAKE": "Ciasto", "BUTTER": "Masło",
    "CHEESE": "Ser", "FABRIC": "Tkanina", "CLOTHES": "Ubrania", "SUGAR": "Cukier",
    "SUNFLOWER_OIL": "Olej Słonecznikowy", "CANOLA_OIL": "Olej Rzepakowy", 
    "OLIVE_OIL": "Oliwa z Oliwek", "GRAPEJUICE": "Sok Winogronowy", "RAISINS": "Rodzynki", 
    "CEREAL": "Płatki Zbożowe", "CHOCOLATE": "Czekolada", "BOARDS": "Deski", 
    "FURNITURE": "Meble", "WOODCHIPS": "Zrębki", "SILAGE": "Kiszonka", "HAY": "Siano", 
    "STRAW": "Słoma", "WOOD": "Drewno", "MINERAL_FEED": "Pasza Mineralna", "CHAFF": "Sieczka", 
    "PIGFOOD": "Karma dla Świń", "SEEDS": "Nasiona", "FERTILIZER": "Nawóz", "LIME": "Wapno", 
    "HERBICIDE": "Herbicyd", "WATER": "Woda", "DIESEL": "Paliwo"
}

# Definicje Kategorii (Klucz wewnętrzny -> Lista FillTypes)
CATEGORY_DEFINITIONS = {
    "crops": [
        "WHEAT", "BARLEY", "CANOLA", "OAT", "MAIZE", "SUNFLOWER", "SOYBEAN", "SORGHUM", 
        "COTTON", "SUGARCANE", "POTATO", "SUGARBEET", "POPLAR", "GRASS", "MEADOW"
    ],
    "veggies": [
        "TOMATO", "LETTUCE", "STRAWBERRY", "GRAPE", "OLIVE", "RICE", "SPINACH", "PEA", 
        "BEANS", "GREENBEAN", "ONION", "GARLIC", "CARROT", "PARSNIP", "RED_BEET", 
        "BEETROOT", "PUMPKIN", "WATERMELON", "MELON", "REDLETTUCE", "NAPACABBAGE", 
        "REDCABBAGE", "CHILLI", "SPRING_ONION", "ENOKI", "OYSTER", "RICESAPLINGS"
    ],
    "animals": [
        "MILK", "EGG", "WOOL", "HONEY", "MANURE", "LIQUIDMANURE", "DIGESTATE", 
        "GOATMILK", "BUFFALOMILK"
    ],
    "production": [
        "FLOUR", "BREAD", "CAKE", "BUTTER", "CHEESE", "FABRIC", "CLOTHES", "SUGAR", 
        "SUNFLOWER_OIL", "CANOLA_OIL", "OLIVE_OIL", "GRAPEJUICE", "RAISINS", "CEREAL", 
        "CHOCOLATE", "BOARDS", "FURNITURE", "PRESERVEDCARROTS", "PRESERVEDPARSNIP", 
        "PRESERVEDBEETROOT", "SOUPCANSCARROTS", "SOUPCANSPARSNIP", "SOUPCANSBEETROOT", 
        "SOUPCANSPOTATO", "SOUPCANSMIXED", "POTATOCHIPS", "FRENCHFRIES", "NOODLESOUP", 
        "RICEROLLS", "RICEFLOUR", "RICE_OIL", "GOATCHEESE", "BUFFALOMOZZARELLA", 
        "PAPERROLL", "CARTONROLL", "ROPE", "CEMENT", "CEMENTBRICKS", "ROOFPLATES", 
        "WOODBEAM", "PLANKS", "PREFABWALL", "BATHTUB", "BUCKET", "BARREL"
    ],
    "forage": [
        "SILAGE", "HAY", "STRAW", "CHAFF", "GRASS_WINDROW", "DRYGRASS_WINDROW", 
        "WOOD", "WOODCHIPS", "PIGFOOD", "MINERAL_FEED"
    ]
}

# Nazwy wyświetlane zakładek
CATEGORY_LABELS_PL = {
    "crops": "🌾 Uprawy",
    "veggies": "🍅 Warzywa / Szklarnia",
    "animals": "🐄 Zwierzęce",
    "production": "🏭 Przetwórstwo",
    "forage": "🚜 Pasze i Drewno",
    "mods": "📦 Inne / Mody"
}

# Mapa okresów
PERIOD_MAP = {
    "EARLY_SPRING": ("Marzec", 0), "MID_SPRING": ("Kwiecień", 1), "LATE_SPRING": ("Maj", 2),
    "EARLY_SUMMER": ("Czerwiec", 3), "MID_SUMMER": ("Lipiec", 4), "LATE_SUMMER": ("Sierpień", 5),
    "EARLY_AUTUMN": ("Wrzesień", 6), "MID_AUTUMN": ("Październik", 7), "LATE_AUTUMN": ("Listopad", 8),
    "EARLY_WINTER": ("Grudzień", 9), "MID_WINTER": ("Styczeń", 10), "LATE_WINTER": ("Luty", 11)
}

INDEX_TO_MONTH = {v[1]: v[0] for k, v in PERIOD_MAP.items()}