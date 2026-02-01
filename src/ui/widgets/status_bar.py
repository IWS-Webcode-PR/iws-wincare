"""
Status indicator widget.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class StatusIndicator(QWidget):
    """Status indicator showing admin privileges and operation state."""
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Initialize layout and widgets."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(12)
        
        # Admin status badge
        self._admin_indicator = QLabel()
        self._admin_indicator.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._admin_indicator)
        
        # Separator
        separator = QFrame()
        separator.setFixedWidth(1)
        separator.setFixedHeight(16)
        separator.setStyleSheet('background-color: rgba(255, 255, 255, 0.2);')
        layout.addWidget(separator)
        
        # Operation status
        self._status_label = QLabel('Ready')
        self._status_label.setStyleSheet('''
            font-size: 12px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.8);
        ''')
        layout.addWidget(self._status_label)
        
        layout.addStretch()
    
    def set_admin_status(self, is_admin: bool) -> None:
        """Update admin privilege indicator."""
        if is_admin:
            self._admin_indicator.setText('Administrator')
            self._admin_indicator.setStyleSheet('''
                font-size: 11px;
                font-weight: 600;
                color: white;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #22c55e, stop:1 #16a34a
                );
                padding: 3px 10px;
                border-radius: 10px;
            ''')
        else:
            self._admin_indicator.setText('Standard User')
            self._admin_indicator.setStyleSheet('''
                font-size: 11px;
                font-weight: 600;
                color: white;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f59e0b, stop:1 #d97706
                );
                padding: 3px 10px;
                border-radius: 10px;
            ''')
    
    def set_status(self, status: str, is_error: bool = False) -> None:
        """Update operation status text."""
        self._status_label.setText(status)
        
        if is_error:
            self._status_label.setStyleSheet('''
                font-size: 12px;
                font-weight: 500;
                color: #ef4444;
            ''')
        else:
            self._status_label.setStyleSheet('''
                font-size: 12px;
                font-weight: 500;
                color: rgba(255, 255, 255, 0.8);
            ''')
