"""
IWS-WinCare main application window.
"""

from typing import Dict, Optional, Type
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QScrollArea, QLabel, QProgressBar,
    QTextEdit, QMessageBox, QMenuBar, QMenu, QStatusBar,
    QSplitter, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QSize, QByteArray
from PySide6.QtGui import QAction, QFont, QIcon, QPixmap, QColor

from src.ui.styles import Styles
from src.ui.icon import get_icon_data
from src.ui.widgets import ActionCard, StatusIndicator
from src.core.executor import ModuleExecutor, ExecutionResult, ExecutionStatus
from src.modules.base import BaseModule
from src.modules.bugfix import (
    DNSFlushModule, WinsockResetModule, NetworkAdapterModule,
    UpdateCacheModule, ExplorerCacheModule, TempCleanupModule,
    EnvironmentRefreshModule
)
from src.modules.reset import (
    NetworkResetModule, PowerPlanResetModule, DefaultAppsResetModule,
    SearchIndexModule, StartMenuResetModule, UpdateResetModule
)
from src.system.admin import is_admin
from src.system.platform_check import PlatformCheck
from src.utils.logger import get_logger
from src.utils.config import Config


class ExecutionWorker(QThread):
    """Background worker for module execution."""
    
    finished = Signal(ExecutionResult)
    progress = Signal(str)
    
    def __init__(self, module: BaseModule, parent=None) -> None:
        super().__init__(parent)
        self._module = module
    
    def run(self) -> None:
        """Execute module in background thread."""
        self.progress.emit(f'Executing {self._module.info.name}...')
        result = self._module.execute()
        self.finished.emit(result)


class MainWindow(QMainWindow):
    """Main application window with tabbed interface."""
    
    def __init__(self) -> None:
        super().__init__()
        
        self._logger = get_logger()
        self._config = Config.load()
        self._executor = ModuleExecutor()
        self._current_worker: Optional[ExecutionWorker] = None
        self._is_dark_mode = self._config.theme == 'dark'
        
        self._modules: Dict[str, BaseModule] = {}
        self._cards: Dict[str, ActionCard] = {}
        
        self._init_modules()
        self._setup_ui()
        self._apply_theme()
        self._check_system()
    
    def _init_modules(self) -> None:
        """Initialize all available modules."""
        module_classes: list[Type[BaseModule]] = [
            DNSFlushModule,
            WinsockResetModule,
            NetworkAdapterModule,
            UpdateCacheModule,
            ExplorerCacheModule,
            TempCleanupModule,
            EnvironmentRefreshModule,
            NetworkResetModule,
            PowerPlanResetModule,
            DefaultAppsResetModule,
            SearchIndexModule,
            StartMenuResetModule,
            UpdateResetModule,
        ]
        
        for cls in module_classes:
            module = cls()
            module_id = cls.__name__
            self._modules[module_id] = module
    
    def _setup_ui(self) -> None:
        """Initialize main window UI."""
        self.setWindowTitle('IWS-WinCare')
        self.setMinimumSize(900, 650)
        self.resize(self._config.window_width, self._config.window_height)
        
        # Set window icon
        self._set_window_icon()
        
        # Center window on screen
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Content splitter
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(1)
        
        # Tab widget
        self._tabs = QTabWidget()
        self._tabs.addTab(self._create_bugfix_tab(), 'Bug Fixes')
        self._tabs.addTab(self._create_reset_tab(), 'System Reset')
        splitter.addWidget(self._tabs)
        
        # Output console
        console_frame = QFrame()
        console_layout = QVBoxLayout(console_frame)
        console_layout.setContentsMargins(12, 8, 12, 12)
        console_layout.setSpacing(4)
        
        console_header = QHBoxLayout()
        console_label = QLabel('Output')
        console_label.setStyleSheet('font-weight: 600;')
        console_header.addWidget(console_label)
        console_header.addStretch()
        console_layout.addLayout(console_header)
        
        self._console = QTextEdit()
        self._console.setReadOnly(True)
        self._console.setMinimumHeight(120)
        self._console.setMaximumHeight(200)
        console_layout.addWidget(self._console)
        
        splitter.addWidget(console_frame)
        splitter.setSizes([500, 150])
        
        main_layout.addWidget(splitter, 1)
        
        # Progress bar
        self._progress = QProgressBar()
        self._progress.setTextVisible(False)
        self._progress.setMaximum(0)
        self._progress.hide()
        main_layout.addWidget(self._progress)
        
        # Menu bar (after console is created)
        self._setup_menu()
        
        # Status bar
        self._setup_status_bar()
    
    def _setup_menu(self) -> None:
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        self._theme_action = QAction('Light Mode', self)
        self._theme_action.setCheckable(True)
        self._theme_action.setChecked(not self._is_dark_mode)
        self._theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(self._theme_action)
        
        clear_console = QAction('Clear Console', self)
        clear_console.setShortcut('Ctrl+L')
        clear_console.triggered.connect(self._console.clear)
        view_menu.addAction(clear_console)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self) -> None:
        """Create status bar."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        self._status_indicator = StatusIndicator()
        status_bar.addPermanentWidget(self._status_indicator)
        
        self._status_indicator.set_admin_status(is_admin())
        self._status_indicator.set_status('Ready')
    
    def _create_header(self) -> QWidget:
        """Create application header with logo and title."""
        header = QFrame()
        header.setObjectName('appHeader')
        header.setStyleSheet('''
            QFrame#appHeader {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(59, 130, 246, 0.15),
                    stop:0.5 rgba(139, 92, 246, 0.1),
                    stop:1 rgba(59, 130, 246, 0.15)
                );
                border-bottom: 1px solid rgba(59, 130, 246, 0.3);
            }
        ''')
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)
        
        # Logo icon
        logo_label = QLabel()
        icon_pixmap = QPixmap()
        icon_pixmap.loadFromData(QByteArray.fromBase64(get_icon_data().encode()))
        logo_label.setPixmap(icon_pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(logo_label)
        
        # Title section
        title_section = QVBoxLayout()
        title_section.setSpacing(2)
        
        title = QLabel('IWS-WinCare')
        title.setProperty('heading', True)
        title.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #3b82f6;
        ''')
        title_section.addWidget(title)
        
        subtitle = QLabel('Professional Windows 10/11 repair and maintenance toolkit')
        subtitle.setProperty('subheading', True)
        subtitle.setStyleSheet('font-size: 13px; opacity: 0.8;')
        title_section.addWidget(subtitle)
        
        layout.addLayout(title_section)
        layout.addStretch()
        
        # Version badge
        version_badge = QLabel('v1.0.0')
        version_badge.setStyleSheet('''
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #3b82f6, stop:1 #8b5cf6
            );
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        ''')
        layout.addWidget(version_badge)
        
        return header
    
    def _create_bugfix_tab(self) -> QWidget:
        """Create bug-fix modules tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        bugfix_modules = [
            'DNSFlushModule', 'WinsockResetModule', 'NetworkAdapterModule',
            'UpdateCacheModule', 'ExplorerCacheModule', 'TempCleanupModule',
            'EnvironmentRefreshModule'
        ]
        
        for module_id in bugfix_modules:
            if module_id in self._modules:
                card = self._create_module_card(module_id)
                layout.addWidget(card)
        
        layout.addStretch()
        scroll.setWidget(container)
        
        return scroll
    
    def _create_reset_tab(self) -> QWidget:
        """Create reset modules tab."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Warning notice
        warning = QLabel(
            'Warning: Reset operations may cause temporary disruption. '
            'Create a system restore point before proceeding.'
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            'background-color: rgba(240, 173, 78, 0.2); '
            'border: 1px solid #f0ad4e; '
            'border-radius: 4px; '
            'padding: 12px; '
            'color: #f0ad4e;'
        )
        layout.addWidget(warning)
        
        reset_modules = [
            'NetworkResetModule', 'PowerPlanResetModule', 'DefaultAppsResetModule',
            'SearchIndexModule', 'StartMenuResetModule', 'UpdateResetModule'
        ]
        
        for module_id in reset_modules:
            if module_id in self._modules:
                card = self._create_module_card(module_id)
                layout.addWidget(card)
        
        layout.addStretch()
        scroll.setWidget(container)
        
        return scroll
    
    def _create_module_card(self, module_id: str) -> ActionCard:
        """Create action card for a module."""
        module = self._modules[module_id]
        info = module.info
        
        card = ActionCard(
            module_id=module_id,
            name=info.name,
            description=info.description,
            category=info.category,
            is_critical=info.is_critical,
            requires_reboot=info.requires_reboot
        )
        
        card.execute_requested.connect(self._on_execute_requested)
        self._cards[module_id] = card
        
        return card
    
    def _apply_theme(self) -> None:
        """Apply current theme stylesheet."""
        stylesheet = Styles.get_theme(self._is_dark_mode)
        self.setStyleSheet(stylesheet)
    
    def _set_window_icon(self) -> None:
        """Set application window icon."""
        icon_data = get_icon_data()
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(icon_data.encode()))
        self.setWindowIcon(QIcon(pixmap))
    
    def _toggle_theme(self) -> None:
        """Toggle between dark and light theme."""
        self._is_dark_mode = not self._is_dark_mode
        self._theme_action.setChecked(not self._is_dark_mode)
        self._theme_action.setText('Light Mode' if self._is_dark_mode else 'Dark Mode')
        self._config.theme = 'dark' if self._is_dark_mode else 'light'
        self._config.save()
        self._apply_theme()
    
    def _check_system(self) -> None:
        """Check system compatibility on startup."""
        info = PlatformCheck.check_system()
        
        if not info.is_compatible:
            QMessageBox.warning(
                self,
                'Compatibility Warning',
                info.compatibility_message
            )
        
        if not is_admin():
            self._log_output(
                'Running without administrator privileges. '
                'Some functions will not be available.'
            )
    
    @Slot(str)
    def _on_execute_requested(self, module_id: str) -> None:
        """Handle module execution request."""
        if self._current_worker and self._current_worker.isRunning():
            QMessageBox.information(
                self,
                'Operation in Progress',
                'Please wait for the current operation to complete.'
            )
            return
        
        module = self._modules.get(module_id)
        if not module:
            return
        
        info = module.info
        
        # Confirmation for critical actions
        if info.is_critical:
            reply = QMessageBox.warning(
                self,
                'Confirm Critical Action',
                f'{info.name}\n\n'
                f'{info.description}\n\n'
                f'{"This operation requires a system restart." if info.requires_reboot else ""}\n\n'
                'Do you want to proceed?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
        
        # Check admin requirements
        if info.requires_admin and not is_admin():
            QMessageBox.critical(
                self,
                'Administrator Required',
                'This operation requires administrator privileges.\n'
                'Please restart the application as administrator.'
            )
            return
        
        self._execute_module(module_id)
    
    def _execute_module(self, module_id: str) -> None:
        """Execute a module in background thread."""
        module = self._modules[module_id]
        card = self._cards.get(module_id)
        
        if card:
            card.set_executing(True)
        
        self._set_all_cards_enabled(False)
        self._progress.show()
        self._status_indicator.set_status(f'Executing {module.info.name}...')
        
        self._current_worker = ExecutionWorker(module)
        self._current_worker.progress.connect(self._log_output)
        self._current_worker.finished.connect(
            lambda result: self._on_execution_finished(module_id, result)
        )
        self._current_worker.start()
        
        self._logger.info(f'Started execution of {module_id}')
    
    @Slot(str, ExecutionResult)
    def _on_execution_finished(self, module_id: str, result: ExecutionResult) -> None:
        """Handle module execution completion."""
        card = self._cards.get(module_id)
        
        if card:
            card.set_executing(False)
        
        self._set_all_cards_enabled(True)
        self._progress.hide()
        
        if result.success:
            self._status_indicator.set_status('Completed successfully')
            self._log_output(f'[SUCCESS] {result.message}')
        else:
            self._status_indicator.set_status('Operation failed', is_error=True)
            self._log_output(f'[FAILED] {result.message}')
        
        if result.details:
            self._log_output(result.details)
        
        self._logger.info(
            f'Execution of {module_id} completed: '
            f'{result.status.value} - {result.message}'
        )
        
        # Offer restart if required
        module = self._modules.get(module_id)
        if module and module.info.requires_reboot and result.success:
            self._offer_restart()
    
    def _set_all_cards_enabled(self, enabled: bool) -> None:
        """Enable or disable all action cards."""
        for card in self._cards.values():
            card.set_enabled(enabled)
    
    def _log_output(self, message: str) -> None:
        """Append message to output console."""
        self._console.append(message)
        scrollbar = self._console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _offer_restart(self) -> None:
        """Offer to restart the computer."""
        reply = QMessageBox.question(
            self,
            'Restart Required',
            'A system restart is required to complete this operation.\n'
            'Would you like to restart now?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            from ..system.commands import CommandRunner
            runner = CommandRunner()
            runner.run(['shutdown', '/r', '/t', '30', '/c', 
                       'IWS-WinCare: Restarting to complete repairs'])
            self._log_output('System will restart in 30 seconds...')
    
    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            'About IWS-WinCare',
            'IWS-WinCare\n'
            'Version 1.0.0\n\n'
            'Professional Windows 10/11 repair and\n'
            'system maintenance toolkit.\n\n'
            'Developer: IWS-Webcode.eu\n'
            'https://iws-webcode.eu\n\n'
            'https://github.com/IWS-Webcode-PR/iws-wincare\n\n'
            'Licensed under MIT License'
        )
    
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Save window size
        self._config.window_width = self.width()
        self._config.window_height = self.height()
        self._config.save()
        
        # Cancel running operations
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.terminate()
            self._current_worker.wait(1000)
        
        self._executor.shutdown()
        event.accept()
