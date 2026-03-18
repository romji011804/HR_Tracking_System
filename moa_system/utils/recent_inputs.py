"""
Recent Inputs Manager
Manages recent search history with persistence (JSON file)
Provides modern TikTok-style dropdown with delete functionality
"""
import json
import os
from typing import List

class RecentInputsManager:
    """Manages persistent recent inputs for dropdown fields"""
    
    def __init__(self, field_name: str, max_items: int = 10):
        """
        Initialize recent inputs manager
        
        Args:
            field_name: Name of the field (e.g., "school", "course")
            max_items: Maximum number of items to store (default: 10)
        """
        self.field_name = field_name
        self.max_items = max_items
        self.data_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'recent_inputs.json'
        )
        self.recent_items = self._load()
    
    def _load(self) -> dict:
        """Load recent inputs from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data
        except Exception as e:
            print(f"[DEBUG] Error loading recent inputs: {e}")
        
        return {}
    
    def _save(self):
        """Save recent inputs to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.recent_items, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[DEBUG] Error saving recent inputs: {e}")
    
    def get_recent(self) -> List[str]:
        """Get list of recent inputs for this field"""
        items = self.recent_items.get(self.field_name, [])
        return items[:self.max_items]
    
    def add_input(self, text: str):
        """
        Add a new input to recent list
        
        - Prevents duplicates
        - Most recent items first
        - Enforces max_items limit
        """
        text = text.strip()
        
        if not text:
            return
        
        # Get current items for this field
        if self.field_name not in self.recent_items:
            self.recent_items[self.field_name] = []
        
        items = self.recent_items[self.field_name]
        
        # Remove if already exists (to move to top)
        if text in items:
            items.remove(text)
        
        # Add to beginning (most recent)
        items.insert(0, text)
        
        # Enforce max items limit
        self.recent_items[self.field_name] = items[:self.max_items]
        
        # Save to file
        self._save()
        
        print(f"[DEBUG] Added '{text}' to recent {self.field_name}")
    
    def delete_input(self, text: str):
        """Remove an input from recent list"""
        text = text.strip()
        
        if self.field_name not in self.recent_items:
            return
        
        items = self.recent_items[self.field_name]
        
        if text in items:
            items.remove(text)
            self._save()
            print(f"[DEBUG] Deleted '{text}' from recent {self.field_name}")
    
    def clear_all(self):
        """Clear all recent inputs for this field"""
        if self.field_name in self.recent_items:
            del self.recent_items[self.field_name]
            self._save()
            print(f"[DEBUG] Cleared all recent {self.field_name}")
