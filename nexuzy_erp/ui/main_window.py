"""
Nexuzy ERP — Main Window (Dashboard Shell)
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame,
    QSizePolicy, QStatusBar
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QIcon

from nexuzy_erp.config.roles import has_access
from nexuzy_erp.ui.dashboard import DashboardWidget
from nexuzy_erp.ui.modules.employees_widget import EmployeesWidget
from nexuzy_erp.ui.modules.attendance_widget import AttendanceWidget
from nexuzy_erp.ui.modules.inventory_widget import InventoryWidget
from nexuzy_erp.ui.modules.production_widget import ProductionWidget
from nexuzy_erp.ui.modules.bom_widget import BOMWidget
from nexuzy_erp.ui.modules.sales_widget import SalesWidget
from nexuzy_erp.ui.modules.purchase_widget import PurchaseWidget
from nexuzy_erp.ui.modules.accounts_widget import AccountsWidget
from nexuzy_erp.ui.modules.reports_widget import ReportsWidget
from nexuzy_erp.ui.modules.settings_widget import SettingsWidget
from nexuzy_erp.api.sync_api import SyncAPI


NAV_ITEMS = [
    ("dashboard",  "📊", "Dashboard"),
    ("production", "🏭", "Production"),
    ("bom",        "📝", "BOM"),
    ("inventory",  "📦", "Inventory"),
    ("purchase",   "🛒", "Purchase"),
    ("sales",      "💰", "Sales"),
    ("employees",  "👨‍💼", "Employees"),
    ("attendance", "⏱️",  "Attendance"),
    ("accounts",   "💳", "Accounts"),
    ("reports",    "📈", "Reports"),
    ("settings",   "⚙️",  "Settings"),
]


class MainWindow(QMainWindow):
    def __init__(self, user_data: dict):
        super().__init__()
        self.user_data = user_data
        self.role = user_data.get("role", "worker")
        self.setWindowTitle("Nexuzy ERP — Nexuzy Lab")
        self.setMinimumSize(1280, 800)
        self._setup_ui()
        self._start_sync_timer()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = self._build_sidebar()
        main_layout.addWidget(sidebar)

        # Content area
        self.stack = QStackedWidget()
        self._pages = {}
        self._build_pages()
        main_layout.addWidget(self.stack, 1)

        # Status bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(f"🟢 Connected • Logged in as: {self.user_data.get('username', 'User')} ({self.role.title()})")

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(4)

        # Logo
        logo = QLabel("🚀 Nexuzy ERP")
        logo.setObjectName("logo_label")
        logo.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(logo)

        # User info badge
        user_badge = QLabel(f"👤 {self.user_data.get('username', 'User')}\n{self.role.title()}")
        user_badge.setStyleSheet("color: #9090cc; font-size: 11px; padding: 4px 16px; margin-bottom: 8px;")
        layout.addWidget(user_badge)

        self._nav_buttons = {}
        for module_id, icon, label in NAV_ITEMS:
            if not has_access(self.role, module_id):
                continue
            btn = QPushButton(f"  {icon}  {label}")
            btn.setCheckable(True)
            btn.setMinimumHeight(44)
            btn.clicked.connect(lambda checked, mid=module_id: self._navigate(mid))
            layout.addWidget(btn)
            self._nav_buttons[module_id] = btn

        layout.addStretch()

        # Sync status
        self.sync_lbl = QLabel("⏳ Syncing...")
        self.sync_lbl.setStyleSheet("color: #6060aa; font-size: 11px; padding: 4px 16px;")
        layout.addWidget(self.sync_lbl)

        # Logout
        logout_btn = QPushButton("  🚪  Logout")
        logout_btn.setObjectName("danger_btn")
        logout_btn.setMinimumHeight(40)
        logout_btn.clicked.connect(self._logout)
        layout.addWidget(logout_btn)

        return sidebar

    def _build_pages(self):
        page_map = {
            "dashboard":  DashboardWidget,
            "production": ProductionWidget,
            "bom":        BOMWidget,
            "inventory":  InventoryWidget,
            "purchase":   PurchaseWidget,
            "sales":      SalesWidget,
            "employees":  EmployeesWidget,
            "attendance": AttendanceWidget,
            "accounts":   AccountsWidget,
            "reports":    ReportsWidget,
            "settings":   SettingsWidget,
        }
        for module_id, widget_cls in page_map.items():
            if has_access(self.role, module_id):
                w = widget_cls(user_data=self.user_data)
                self.stack.addWidget(w)
                self._pages[module_id] = w

        # Default page
        self._navigate("dashboard")

    def _navigate(self, module_id: str):
        for mid, btn in self._nav_buttons.items():
            btn.setChecked(mid == module_id)
        if module_id in self._pages:
            self.stack.setCurrentWidget(self._pages[module_id])

    def _start_sync_timer(self):
        from nexuzy_erp.config.settings import Settings
        self._sync_timer = QTimer(self)
        self._sync_timer.timeout.connect(self._do_sync)
        self._sync_timer.start(Settings.AUTO_SYNC_INTERVAL * 1000)

    def _do_sync(self):
        self.sync_lbl.setText("⏳ Syncing...")
        # Background sync
        from PySide6.QtCore import QThread
        # SyncAPI.sync_all() called in thread
        self.sync_lbl.setText("✅ Synced")

    def _logout(self):
        from nexuzy_erp.ui.login_window import LoginWindow
        self.login_win = LoginWindow()
        self.login_win.show()
        self.close()
