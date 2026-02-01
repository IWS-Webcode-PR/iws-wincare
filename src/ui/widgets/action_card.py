"""
Action card widget for module display.
"""

from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor


class ActionCard(QFrame):
    """Card widget representing a repair/reset module."""
    
    execute_requested = Signal(str)
    
    CATEGORY_ICONS = {
        'Network': '&#xe89e;',
        'System': '&#xe8b8;',
        'Cleanup': '&#xe872;',
    }
    
    CATEGORY_COLORS = {
        'Network': '#3b82f6',
        'System': '#8b5cf6',
        'Cleanup': '#22c55e',
    }
    
    def __init__(
        self,
        module_id: str,
        name: str,
        description: str,
        category: str,
        is_critical: bool = False,
        requires_reboot: bool = False,
        parent=None
    ) -> None:
        super().__init__(parent)
        
        self._module_id = module_id
        self._is_critical = is_critical
        self._requires_reboot = requires_reboot
        self._category = category
        
        self.setProperty('card', True)
        self.setMinimumHeight(110)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self._setup_ui(name, description, category)
    
    def _setup_ui(self, name: str, description: str, category: str) -> None:
        """Initialize modern card layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Category indicator bar
        indicator = QFrame()
        indicator.setFixedWidth(4)
        indicator.setStyleSheet(f'''
            background: {self.CATEGORY_COLORS.get(category, '#3b82f6')};
            border-radius: 2px;
        ''')
        layout.addWidget(indicator)
        
        # Content area
        content_layout = QVBoxLayout()
        content_layout.setSpacing(8)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with title and badges
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        name_label = QLabel(name)
        name_label.setProperty('title', True)
        name_label.setStyleSheet('font-size: 15px; font-weight: 600; color: #fafafa;')
        header_layout.addWidget(name_label)
        
        # Category badge with solid background for readability
        category_badge = QLabel(category)
        category_badge.setStyleSheet(f'''
            font-size: 11px;
            font-weight: 600;
            color: #ffffff;
            background: {self.CATEGORY_COLORS.get(category, '#3b82f6')};
            padding: 4px 12px;
            border-radius: 10px;
        ''')
        header_layout.addWidget(category_badge)
        
        # Status badges
        if self._requires_reboot:
            reboot_badge = QLabel('Restart')
            reboot_badge.setStyleSheet('''
                font-size: 11px;
                font-weight: 600;
                color: #ffffff;
                background: #f59e0b;
                padding: 4px 12px;
                border-radius: 10px;
            ''')
            header_layout.addWidget(reboot_badge)
        
        if self._is_critical:
            critical_badge = QLabel('Critical')
            critical_badge.setStyleSheet('''
                font-size: 11px;
                font-weight: 600;
                color: #ffffff;
                background: #ef4444;
                padding: 4px 12px;
                border-radius: 10px;
            ''')
            header_layout.addWidget(critical_badge)
        
        header_layout.addStretch()
        content_layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setProperty('subheading', True)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet('font-size: 13px; color: #71717a; line-height: 1.4;')
        content_layout.addWidget(desc_label)
        
        layout.addLayout(content_layout, 1)
        
        # Action button
        self._execute_btn = QPushButton('Run')
        self._execute_btn.setMinimumWidth(90)
        self._execute_btn.setMinimumHeight(38)
        self._execute_btn.setCursor(Qt.PointingHandCursor)
        
        if self._is_critical:
            self._execute_btn.setProperty('critical', True)
            self._execute_btn.setStyleSheet(self._execute_btn.styleSheet())
        
        self._execute_btn.clicked.connect(self._on_execute_clicked)
        layout.addWidget(self._execute_btn, 0, Qt.AlignVCenter)
    
    def _on_execute_clicked(self) -> None:
        """Handle execute button click."""
        self.execute_requested.emit(self._module_id)
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the action button."""
        self._execute_btn.setEnabled(enabled)
    
    def set_executing(self, executing: bool) -> None:
        """Update button state during execution."""
        self._execute_btn.setEnabled(not executing)
        self._execute_btn.setText('Running...' if executing else 'Execute')
