"""
Nexuzy ERP — Dashboard Widget
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QSizePolicy, QPushButton, QScrollArea
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QColor

from nexuzy_erp.api.dashboard_api import DashboardAPI
from nexuzy_erp.api.ai_api import SarvaamAI


class StatCard(QFrame):
    def __init__(self, icon: str, title: str, value: str, color: str = "#6c3fff"):
        super().__init__()
        self.setObjectName("stat_card")
        self.setMinimumSize(200, 110)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        top = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setFont(QFont("Segoe UI Emoji", 24))
        top.addWidget(icon_lbl)
        top.addStretch()
        layout.addLayout(top)

        val_lbl = QLabel(value)
        val_lbl.setFont(QFont("Segoe UI", 22, QFont.Bold))
        val_lbl.setStyleSheet(f"color: {color};")
        layout.addWidget(val_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("color: #9090bb; font-size: 12px;")
        layout.addWidget(title_lbl)
        self.val_lbl = val_lbl

    def update_value(self, val: str):
        self.val_lbl.setText(val)


class DashboardDataWorker(QThread):
    data_ready = Signal(dict)

    def run(self):
        try:
            data = DashboardAPI.get_summary()
            self.data_ready.emit(data)
        except Exception:
            self.data_ready.emit({})


class DashboardWidget(QWidget):
    def __init__(self, user_data: dict = None):
        super().__init__()
        self.user_data = user_data or {}
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        self.main_layout = QVBoxLayout(content)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(20)

        # Header
        header = QHBoxLayout()
        title = QLabel("📊 Dashboard")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        header.addWidget(title)
        header.addStretch()
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("primary_btn")
        refresh_btn.clicked.connect(self._load_data)
        header.addWidget(refresh_btn)
        self.main_layout.addLayout(header)

        # Stat cards grid
        cards_grid = QGridLayout()
        cards_grid.setSpacing(16)

        self.cards = {
            "production": StatCard("🏭", "Production Today", "0", "#6c3fff"),
            "inventory":  StatCard("📦", "Inventory Alerts", "0", "#ff6b35"),
            "workers":    StatCard("👨‍💼", "Active Workers", "0", "#00d2a0"),
            "sales":      StatCard("💰", "Today Sales", "₹0", "#f7c94b"),
            "pending":    StatCard("⏳", "Pending Orders", "0", "#ff4f87"),
            "revenue":    StatCard("📈", "Monthly Revenue", "₹0", "#4fc3f7"),
        }
        positions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2)]
        for (r,c), (_, card) in zip(positions, self.cards.items()):
            cards_grid.addWidget(card, r, c)
        self.main_layout.addLayout(cards_grid)

        # AI Insights panel
        ai_frame = QFrame()
        ai_frame.setObjectName("stat_card")
        ai_layout = QVBoxLayout(ai_frame)
        ai_header = QHBoxLayout()
        ai_title = QLabel("🤖 AI Insights (Sarvaam AI)")
        ai_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        ai_title.setStyleSheet("color: #a78bfa;")
        ai_header.addWidget(ai_title)
        ai_header.addStretch()
        ai_refresh = QPushButton("✨ Get Insights")
        ai_refresh.setObjectName("primary_btn")
        ai_refresh.clicked.connect(self._load_ai_insights)
        ai_header.addWidget(ai_refresh)
        ai_layout.addLayout(ai_header)

        self.ai_label = QLabel("Click 'Get Insights' to load AI-powered business analysis...")
        self.ai_label.setWordWrap(True)
        self.ai_label.setStyleSheet("color: #c0c0ee; font-size: 13px; padding: 8px;")
        ai_layout.addWidget(self.ai_label)
        self.main_layout.addWidget(ai_frame)

        self.main_layout.addStretch()
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0,0,0,0)
        outer.addWidget(scroll)

    def _load_data(self):
        self.worker = DashboardDataWorker()
        self.worker.data_ready.connect(self._update_cards)
        self.worker.start()

    def _update_cards(self, data: dict):
        self.cards["production"].update_value(str(data.get("production_today", 0)))
        self.cards["inventory"].update_value(str(data.get("inventory_alerts", 0)))
        self.cards["workers"].update_value(str(data.get("active_workers", 0)))
        self.cards["sales"].update_value(f"₹{data.get('today_sales', 0):,.0f}")
        self.cards["pending"].update_value(str(data.get("pending_orders", 0)))
        self.cards["revenue"].update_value(f"₹{data.get('monthly_revenue', 0):,.0f}")

    def _load_ai_insights(self):
        self.ai_label.setText("⏳ Loading AI insights...")
        try:
            insight = SarvaamAI.get_business_insights({
                "context": "ERP dashboard summary",
                "data": "Analyze production, sales and inventory trends"
            })
            self.ai_label.setText(insight)
        except Exception as e:
            self.ai_label.setText(f"⚠️ AI unavailable: {e}")
