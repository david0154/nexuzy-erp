#!/usr/bin/env python3
"""
Nexuzy ERP - Main Entry Point
by Nexuzy Lab
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTranslator, QLocale
from PySide6.QtGui import QFontDatabase, QIcon

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nexuzy_erp.config.settings import Settings
from nexuzy_erp.ui.login_window import LoginWindow
from nexuzy_erp.database.local_db import LocalDatabase


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Nexuzy ERP")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Nexuzy Lab")

    # High DPI support
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Load global stylesheet
    qss_path = os.path.join(os.path.dirname(__file__), "nexuzy_erp", "ui", "styles", "dark_theme.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())

    # Initialize local SQLite DB
    db = LocalDatabase()
    db.initialize()

    # Show login
    login = LoginWindow()
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
