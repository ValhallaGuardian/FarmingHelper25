"""
Constants Module
Contains translation maps and period definitions.
"""

# Tłumaczenia na Polski
TRANSLATIONS_PL = {
    "WHEAT": "Pszenica", "BARLEY": "Jęczmień", "CANOLA": "Rzepak", "OAT": "Owies",
    "MAIZE": "Kukurydza", "SUNFLOWER": "Słonecznik", "SOYBEAN": "Soja", "POTATO": "Ziemniaki",
    "SUGARBEET": "Buraki Cukrowe", "COTTON": "Bawełna", "SUGARCANE": "Trzcina Cukrowa",
    "GRAPE": "Winogrona", "OLIVE": "Oliwki", "SORGHUM": "Sorgo", "POPLAR": "Topola",
    "GRASS": "Trawa", "OILSEEDRADISH": "Rzodkiew Oleista", "MEADOW": "Łąka",
    
    "EGG": "Jajka", "MILK": "Mleko", "WOOL": "Wełna", "MANURE": "Obornik",
    "LIQUIDMANURE": "Gnojowica", "DIGESTATE": "Poferment", "HONEY": "Miód",
    
    "FLOUR": "Mąka", "BREAD": "Chleb", "CAKE": "Ciasto", "BUTTER": "Masło",
    "CHEESE": "Ser", "FABRIC": "Tkanina", "CLOTHES": "Ubrania", "SUGAR": "Cukier",
    "SUNFLOWER_OIL": "Olej Słonecznikowy", "CANOLA_OIL": "Olej Rzepakowy", 
    "OLIVE_OIL": "Oliwa z Oliwek", "GRAPEJUICE": "Sok Winogronowy", "RAISINS": "Rodzynki", 
    "CEREAL": "Płatki Zbożowe", "CHOCOLATE": "Czekolada", "STRAWBERRY": "Truskawki", 
    "LETTUCE": "Sałata", "TOMATO": "Pomidory", "BOARDS": "Deski", "FURNITURE": "Meble", 
    "WOODCHIPS": "Zrębki", "SILAGE": "Kiszonka", "HAY": "Siano", "STRAW": "Słoma", 
    "WOOD": "Drewno", "MINERAL_FEED": "Pasza Mineralna", "CHAFF": "Sieczka", 
    "PIGFOOD": "Karma dla Świń",
    
    # FS25 New Crops (Placeholder names)
    "RICE": "Ryż", "SPINACH": "Szpinak", "PEA": "Groch", "BEANS": "Fasola",
    "GREENBEAN": "Fasolka Szparagowa", "ONION": "Cebula", "GARLIC": "Czosnek",
    "CARROT": "Marchew", "PARSNIP": "Pasternak", "RED_BEET": "Burak Ćwikłowy",
    "BEETROOT": "Burak Ćwikłowy", "PUMPKIN": "Dynia", "WATERMELON": "Arbuz", 
    "MELON": "Melon", "REDLETTUCE": "Czerwona Sałata", "NAPACABBAGE": "Kapusta Pekińska", 
    "REDCABBAGE": "Czerwona Kapusta", "CHILLI": "Papryczka Chili", 
    "SPRING_ONION": "Zielona Cebulka", "ENOKI": "Grzyby Enoki", "OYSTER": "Boczniaki",
    
    "SEEDS": "Nasiona", "FERTILIZER": "Nawóz", "LIME": "Wapno", 
    "HERBICIDE": "Herbicyd", "WATER": "Woda", "DIESEL": "Paliwo",
    "PRESERVEDCARROTS": "Konserwowa Marchew", "PRESERVEDPARSNIP": "Konserwowy Pasternak",
    "PRESERVEDBEETROOT": "Konserwowy Burak", "SOUPCANSCARROTS": "Zupa Marchewkowa",
    "SOUPCANSPARSNIP": "Zupa Pasternakowa", "SOUPCANSBEETROOT": "Zupa Buraczkowa",
    "SOUPCANSPOTATO": "Zupa Ziemniaczana", "SOUPCANSMIXED": "Zupa Warzywna",
    "POTATOCHIPS": "Chipsy", "FRENCHFRIES": "Frytki", "NOODLESOUP": "Zupa z Makaronem",
    "RICEROLLS": "Roladki Ryżowe", "RICEFLOUR": "Mąka Ryżowa", "RICE_OIL": "Olej Ryżowy",
    "GOATMILK": "Mleko Kozie", "GOATCHEESE": "Ser Kozi", "BUFFALOMILK": "Mleko Bawole",
    "BUFFALOMOZZARELLA": "Mozzarella", "PAPERROLL": "Rolka Papieru", 
    "CARTONROLL": "Rolka Kartonu", "ROPE": "Lina", "CEMENT": "Cement", 
    "CEMENTBRICKS": "Cegły", "ROOFPLATES": "Dachówki", "WOODBEAM": "Belki Drewniane", 
    "PLANKS": "Deski", "PREFABWALL": "Ściana Prefabrykowana", "BATHTUB": "Wanna", 
    "BUCKET": "Wiadro", "BARREL": "Beczka", "RICESAPLINGS": "Sadzonki Ryżu"
}

# Mapa okresów z XML na nazwy miesięcy
PERIOD_MAP = {
    "EARLY_SPRING": ("Marzec", 0), "MID_SPRING": ("Kwiecień", 1), "LATE_SPRING": ("Maj", 2),
    "EARLY_SUMMER": ("Czerwiec", 3), "MID_SUMMER": ("Lipiec", 4), "LATE_SUMMER": ("Sierpień", 5),
    "EARLY_AUTUMN": ("Wrzesień", 6), "MID_AUTUMN": ("Październik", 7), "LATE_AUTUMN": ("Listopad", 8),
    "EARLY_WINTER": ("Grudzień", 9), "MID_WINTER": ("Styczeń", 10), "LATE_WINTER": ("Luty", 11)
}

INDEX_TO_MONTH = {v[1]: v[0] for k, v in PERIOD_MAP.items()}