"""
Nexuzy ERP — Global Settings
"""

import os
import json


class Settings:
    # ─── API Configuration ───────────────────────────────────
    API_BASE_URL = "https://yourdomain.com/api"  # Change to your cPanel URL
    API_KEY = "YOUR_API_KEY_HERE"
    API_TIMEOUT = 15  # seconds

    # ─── Sarvaam AI ──────────────────────────────────────────
    SARVAAM_AI_API_KEY = "YOUR_SARVAAM_AI_KEY"
    SARVAAM_AI_URL = "https://api.sarvaam.ai/v1/chat"

    # ─── Local Database ──────────────────────────────────────
    LOCAL_DB_PATH = os.path.join(os.path.expanduser("~"), ".nexuzy_erp", "local.db")

    # ─── Sync Settings ───────────────────────────────────────
    AUTO_SYNC_INTERVAL = 5 * 60  # 5 minutes in seconds
    SYNC_ON_STARTUP = True

    # ─── App ─────────────────────────────────────────────────
    APP_NAME = "Nexuzy ERP"
    APP_VERSION = "1.0.0"
    COMPANY_NAME = "Nexuzy Lab"
    DEFAULT_LANGUAGE = "en"  # en | hi | bn

    # ─── Security ────────────────────────────────────────────
    TOKEN_EXPIRY_HOURS = 24
    SESSION_FILE = os.path.join(os.path.expanduser("~"), ".nexuzy_erp", "session.json")

    @classmethod
    def load_from_file(cls):
        config_path = os.path.join(os.path.expanduser("~"), ".nexuzy_erp", "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                data = json.load(f)
                for key, val in data.items():
                    setattr(cls, key, val)

    @classmethod
    def save_to_file(cls, updates: dict):
        config_dir = os.path.join(os.path.expanduser("~"), ".nexuzy_erp")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.json")
        existing = {}
        if os.path.exists(config_path):
            with open(config_path) as f:
                existing = json.load(f)
        existing.update(updates)
        with open(config_path, "w") as f:
            json.dump(existing, f, indent=2)
