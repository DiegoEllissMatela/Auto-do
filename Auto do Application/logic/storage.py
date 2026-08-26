"""
Macro Storage & Profile Manager for Auto Do Application
Handles saving and loading automation routines to JSON files.
"""

import json
import os
import datetime

class MacroStorage:
    @staticmethod
    def save_to_file(filepath, actions, metadata=None):
        if not filepath:
            return False, "Invalid filepath"

        if not filepath.endswith(".json"):
            filepath += ".json"

        data = {
            "app": "DENM Auto-Do",
            "version": "2.4.0",
            "created_at": datetime.datetime.now().isoformat(),
            "action_count": len(actions),
            "metadata": metadata or {},
            "actions": actions
        }

        try:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True, f"Saved {len(actions)} actions successfully."
        except Exception as e:
            return False, f"Failed to save: {str(e)}"

    @staticmethod
    def load_from_file(filepath):
        if not filepath or not os.path.exists(filepath):
            return None, "File does not exist"

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            actions = data.get("actions", [])
            return actions, f"Loaded {len(actions)} actions."
        except Exception as e:
            return None, f"Failed to load: {str(e)}"
