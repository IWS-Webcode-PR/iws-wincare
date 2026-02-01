"""
Application styles and themes.
"""


class Styles:
    """Application stylesheet provider."""
    
    DARK_THEME = """
        * {
            font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
        }
        
        QMainWindow {
            background-color: #0f0f0f;
        }
        
        QWidget {
            background-color: transparent;
            color: #e4e4e7;
            font-size: 13px;
        }
        
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #1a1a1a;
            width: 10px;
            border-radius: 5px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3f3f46;
            border-radius: 5px;
            min-height: 40px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #52525b;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3b82f6, stop:1 #2563eb);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #60a5fa, stop:1 #3b82f6);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563eb, stop:1 #1d4ed8);
        }
        
        QPushButton:disabled {
            background: #27272a;
            color: #52525b;
        }
        
        QPushButton[critical="true"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ef4444, stop:1 #dc2626);
        }
        
        QPushButton[critical="true"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f87171, stop:1 #ef4444);
        }
        
        QPushButton[secondary="true"] {
            background: transparent;
            border: 1px solid #3f3f46;
            color: #a1a1aa;
        }
        
        QPushButton[secondary="true"]:hover {
            background: #27272a;
            border-color: #52525b;
            color: #e4e4e7;
        }
        
        QLabel {
            color: #e4e4e7;
            background: transparent;
        }
        
        QLabel[heading="true"] {
            font-size: 26px;
            font-weight: 700;
            color: #ffffff;
        }
        
        QLabel[subheading="true"] {
            font-size: 13px;
            color: #71717a;
        }
        
        QLabel[title="true"] {
            font-size: 15px;
            font-weight: 600;
            color: #fafafa;
        }
        
        QFrame[card="true"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1c1c1e, stop:1 #18181b);
            border: 1px solid #27272a;
            border-radius: 12px;
        }
        
        QFrame[card="true"]:hover {
            border-color: #3b82f6;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #1f1f23, stop:1 #1a1a1e);
        }
        
        QTabWidget::pane {
            border: none;
            background-color: transparent;
            margin-top: -1px;
        }
        
        QTabBar {
            background: transparent;
        }
        
        QTabBar::tab {
            background: transparent;
            color: #71717a;
            padding: 12px 24px;
            margin-right: 4px;
            border: none;
            border-bottom: 3px solid transparent;
            font-weight: 500;
            font-size: 14px;
        }
        
        QTabBar::tab:selected {
            color: #3b82f6;
            border-bottom: 3px solid #3b82f6;
        }
        
        QTabBar::tab:hover:!selected {
            color: #a1a1aa;
            border-bottom: 3px solid #3f3f46;
        }
        
        QProgressBar {
            background-color: #27272a;
            border: none;
            border-radius: 4px;
            height: 4px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3b82f6, stop:1 #8b5cf6);
            border-radius: 4px;
        }
        
        QTextEdit {
            background-color: #0a0a0a;
            border: 1px solid #27272a;
            border-radius: 8px;
            color: #a1a1aa;
            font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
            font-size: 12px;
            padding: 12px;
            selection-background-color: #3b82f6;
        }
        
        QMessageBox {
            background-color: #18181b;
        }
        
        QMessageBox QLabel {
            color: #e4e4e7;
            font-size: 13px;
        }
        
        QMessageBox QPushButton {
            min-width: 90px;
            min-height: 32px;
        }
        
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1e1b4b, stop:0.5 #312e81, stop:1 #1e1b4b);
            color: #c7d2fe;
            border-top: 1px solid #3730a3;
            padding: 4px 12px;
            font-size: 12px;
        }
        
        QStatusBar::item {
            border: none;
        }
        
        QMenuBar {
            background-color: #0f0f0f;
            color: #a1a1aa;
            border-bottom: 1px solid #27272a;
            padding: 4px 8px;
        }
        
        QMenuBar::item {
            padding: 6px 12px;
            border-radius: 6px;
        }
        
        QMenuBar::item:selected {
            background-color: #27272a;
            color: #ffffff;
        }
        
        QMenu {
            background-color: #18181b;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 6px;
        }
        
        QMenu::item {
            padding: 8px 32px 8px 16px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #3b82f6;
            color: #ffffff;
        }
        
        QMenu::separator {
            height: 1px;
            background: #27272a;
            margin: 6px 8px;
        }
        
        QToolTip {
            background-color: #27272a;
            color: #e4e4e7;
            border: 1px solid #3f3f46;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 12px;
        }
        
        QSplitter::handle {
            background: #27272a;
        }
        
        QSplitter::handle:vertical {
            height: 2px;
        }
    """
    
    LIGHT_THEME = """
        * {
            font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
        }
        
        QMainWindow {
            background-color: #fafafa;
        }
        
        QWidget {
            background-color: transparent;
            color: #18181b;
            font-size: 13px;
        }
        
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #f4f4f5;
            width: 10px;
            border-radius: 5px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #d4d4d8;
            border-radius: 5px;
            min-height: 40px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #a1a1aa;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3b82f6, stop:1 #2563eb);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #60a5fa, stop:1 #3b82f6);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563eb, stop:1 #1d4ed8);
        }
        
        QPushButton:disabled {
            background: #e4e4e7;
            color: #a1a1aa;
        }
        
        QPushButton[critical="true"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ef4444, stop:1 #dc2626);
        }
        
        QPushButton[critical="true"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f87171, stop:1 #ef4444);
        }
        
        QPushButton[secondary="true"] {
            background: transparent;
            border: 1px solid #d4d4d8;
            color: #52525b;
        }
        
        QPushButton[secondary="true"]:hover {
            background: #f4f4f5;
            border-color: #a1a1aa;
            color: #18181b;
        }
        
        QLabel {
            color: #18181b;
            background: transparent;
        }
        
        QLabel[heading="true"] {
            font-size: 26px;
            font-weight: 700;
            color: #09090b;
        }
        
        QLabel[subheading="true"] {
            font-size: 13px;
            color: #71717a;
        }
        
        QLabel[title="true"] {
            font-size: 15px;
            font-weight: 600;
            color: #18181b;
        }
        
        QFrame[card="true"] {
            background: #ffffff;
            border: 1px solid #e4e4e7;
            border-radius: 12px;
        }
        
        QFrame[card="true"]:hover {
            border-color: #3b82f6;
            background: #fafafa;
        }
        
        QTabWidget::pane {
            border: none;
            background-color: transparent;
            margin-top: -1px;
        }
        
        QTabBar {
            background: transparent;
        }
        
        QTabBar::tab {
            background: transparent;
            color: #71717a;
            padding: 12px 24px;
            margin-right: 4px;
            border: none;
            border-bottom: 3px solid transparent;
            font-weight: 500;
            font-size: 14px;
        }
        
        QTabBar::tab:selected {
            color: #3b82f6;
            border-bottom: 3px solid #3b82f6;
        }
        
        QTabBar::tab:hover:!selected {
            color: #52525b;
            border-bottom: 3px solid #d4d4d8;
        }
        
        QProgressBar {
            background-color: #e4e4e7;
            border: none;
            border-radius: 4px;
            height: 4px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3b82f6, stop:1 #8b5cf6);
            border-radius: 4px;
        }
        
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #e4e4e7;
            border-radius: 8px;
            color: #3f3f46;
            font-family: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
            font-size: 12px;
            padding: 12px;
            selection-background-color: #3b82f6;
        }
        
        QMessageBox {
            background-color: #ffffff;
        }
        
        QMessageBox QLabel {
            color: #18181b;
            font-size: 13px;
        }
        
        QMessageBox QPushButton {
            min-width: 90px;
            min-height: 32px;
        }
        
        QStatusBar {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3b82f6, stop:0.5 #6366f1, stop:1 #3b82f6);
            color: #ffffff;
            border-top: 1px solid #2563eb;
            padding: 4px 12px;
            font-size: 12px;
        }
        
        QStatusBar::item {
            border: none;
        }
        
        QMenuBar {
            background-color: #fafafa;
            color: #52525b;
            border-bottom: 1px solid #e4e4e7;
            padding: 4px 8px;
        }
        
        QMenuBar::item {
            padding: 6px 12px;
            border-radius: 6px;
        }
        
        QMenuBar::item:selected {
            background-color: #f4f4f5;
            color: #18181b;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e4e4e7;
            border-radius: 8px;
            padding: 6px;
        }
        
        QMenu::item {
            padding: 8px 32px 8px 16px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #3b82f6;
            color: #ffffff;
        }
        
        QMenu::separator {
            height: 1px;
            background: #e4e4e7;
            margin: 6px 8px;
        }
        
        QToolTip {
            background-color: #18181b;
            color: #fafafa;
            border: none;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 12px;
        }
        
        QSplitter::handle {
            background: #e4e4e7;
        }
        
        QSplitter::handle:vertical {
            height: 2px;
        }
    """
    
    @classmethod
    def get_theme(cls, dark_mode: bool = True) -> str:
        """Return stylesheet for specified theme."""
        return cls.DARK_THEME if dark_mode else cls.LIGHT_THEME
