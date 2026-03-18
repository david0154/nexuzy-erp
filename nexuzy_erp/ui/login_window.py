"""
Nexuzy ERP — Login Window
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox,
    QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QFont, QColor

from nexuzy_erp.api.auth_api import AuthAPI
from nexuzy_erp.config.settings import Settings


class LoginWorker(QThread):
    success = Signal(dict)
    failed = Signal(str)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        try:
            result = AuthAPI.login(self.username, self.password)
            if result.get("success"):
                self.success.emit(result)
            else:
                self.failed.emit(result.get("message", "Login failed"))
        except Exception as e:
            self.failed.emit(str(e))


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nexuzy ERP — Login")
        self.setFixedSize(420, 520)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_pos = None
        self._setup_ui()

    def _setup_ui(self):
        # Main card
        card = QFrame(self)
        card.setFixedSize(400, 500)
        card.move(10, 10)
        card.setObjectName("login_card")
        card.setStyleSheet("""
            #login_card {
                background: rgba(18, 12, 40, 0.97);
                border: 1px solid rgba(108, 63, 255, 0.5);
                border-radius: 20px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)

        # Logo / Title
        title = QLabel("🚀 Nexuzy ERP")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: #ffffff; margin-bottom: 4px;")
        layout.addWidget(title)

        sub = QLabel("Enterprise Resource Planning")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #7070cc; font-size: 12px; margin-bottom: 20px;")
        layout.addWidget(sub)

        # Username
        lbl_user = QLabel("Username")
        lbl_user.setStyleSheet("color: #b0b0dd; font-weight: bold;")
        layout.addWidget(lbl_user)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setMinimumHeight(42)
        layout.addWidget(self.username_input)

        # Password
        lbl_pass = QLabel("Password")
        lbl_pass.setStyleSheet("color: #b0b0dd; font-weight: bold;")
        layout.addWidget(lbl_pass)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(42)
        layout.addWidget(self.password_input)

        # Remember me
        self.remember_cb = QCheckBox("Remember me")
        self.remember_cb.setStyleSheet("color: #9090cc;")
        layout.addWidget(self.remember_cb)

        layout.addSpacing(8)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("primary_btn")
        self.login_btn.setMinimumHeight(44)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.clicked.connect(self._do_login)
        layout.addWidget(self.login_btn)

        # Status label
        self.status_lbl = QLabel("")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet("color: #ff6060; font-size: 12px;")
        layout.addWidget(self.status_lbl)

        layout.addStretch()

        # Footer
        footer = QLabel("\u00a9 2026 Nexuzy Lab")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #444466; font-size: 11px;")
        layout.addWidget(footer)

        # Close button
        close_btn = QPushButton("×", self)
        close_btn.setFixedSize(30, 30)
        close_btn.move(378, 8)
        close_btn.setStyleSheet("""
            QPushButton { background: rgba(255,60,60,0.7); border: none;
                          border-radius: 15px; color: white; font-size: 16px; }
            QPushButton:hover { background: rgba(255,60,60,1); }
        """)
        close_btn.clicked.connect(self.close)

    def _do_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            self.status_lbl.setText("Please enter username and password")
            return

        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
        self.status_lbl.setText("")

        self.worker = LoginWorker(username, password)
        self.worker.success.connect(self._on_login_success)
        self.worker.failed.connect(self._on_login_failed)
        self.worker.start()

    def _on_login_success(self, data: dict):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Login")
        from nexuzy_erp.ui.main_window import MainWindow
        self.main_win = MainWindow(user_data=data)
        self.main_win.show()
        self.close()

    def _on_login_failed(self, msg: str):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Login")
        self.status_lbl.setText(f"⚠️ {msg}")

    # Draggable frameless window
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            diff = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + diff)
            self._drag_pos = event.globalPosition().toPoint()
