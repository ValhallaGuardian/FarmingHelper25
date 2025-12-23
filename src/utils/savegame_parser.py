"""
Savegame Parser Module
Handles reading XML files from Farming Simulator savegames.
"""

import os
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Tuple
from src.data.constants import PERIOD_MAP, TRANSLATIONS_PL

class SavegameParser:
    def __init__(self, save_path: str):
        self.save_path = save_path

    def get_available_products(self) -> List[str]:
        """
        Scans economy.xml to find all products that have price history.
        Returns a sorted list of product names (fillTypes).
        """
        products = set()
        if not self.save_path or not os.path.exists(self.save_path):
            return []

        try:
            eco_file = os.path.join(self.save_path, "economy.xml")
            if not os.path.exists(eco_file):
                return []

            tree = ET.parse(eco_file)
            root = tree.getroot()
            
            for filltype_node in root.findall(".//fillType"):
                ft_name = filltype_node.get("fillType")
                history = filltype_node.find("history")
                # Filtrujemy UNKNOWN i tylko te co mają historię
                if ft_name and ft_name != "UNKNOWN" and history is not None:
                    products.add(ft_name)
                    
            # Sortujemy alfabetycznie wg polskiej nazwy dla wygody
            return sorted(list(products), key=lambda x: self._translate(x))
            
        except Exception as e:
            print(f"XML Parse Error: {e}")
            return []

    def get_current_month_index(self) -> Optional[int]:
        """
        Reads environment.xml to calculate current in-game month index (0-11).
        0 = March, 1 = April, etc. (FS logic).
        """
        try:
            env_path = os.path.join(self.save_path, "environment.xml")
            if os.path.exists(env_path):
                tree = ET.parse(env_path)
                root = tree.getroot()
                
                # Logic based on FS22/FS25 structure
                current_day = int(root.find("currentDay").text)
                days_per_period = int(root.find("daysPerPeriod").text)
                
                # Calculate month index
                month_abs_index = (current_day - 1) // days_per_period
                return month_abs_index % 12
        except Exception:
            return None
        return None

    def analyze_economy_history(self) -> Dict[str, List[int]]:
        """
        Analyzes economy.xml to find best selling months for each product.
        Returns: { 'WHEAT': [9, 10], ... } where list contains best month indices.
        """
        seasonality = {}
        try:
            eco_path = os.path.join(self.save_path, "economy.xml")
            if os.path.exists(eco_path):
                tree = ET.parse(eco_path)
                root = tree.getroot()
                
                for filltype_node in root.findall(".//fillType"):
                    ft_name = filltype_node.get("fillType")
                    history = filltype_node.find("history")
                    
                    if ft_name and history is not None:
                        prices = []
                        for period_node in history.findall("period"):
                            p_name = period_node.get("period")
                            p_val = float(period_node.text)
                            
                            if p_name in PERIOD_MAP:
                                idx = PERIOD_MAP[p_name][1]
                                prices.append((idx, p_val))
                        
                        if prices:
                            # Find max price
                            max_price = max(p[1] for p in prices)
                            # Consider any month with price >= 98% of max as "Best"
                            best_months = [p[0] for p in prices if p[1] >= max_price * 0.98]
                            seasonality[ft_name] = sorted(best_months)
        except Exception:
            pass
        return seasonality

    def _translate(self, key: str) -> str:
        return TRANSLATIONS_PL.get(key, key.replace("_", " ").title())