"""
IWS-WinCare - Application entry point.
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.ui.main_window import MainWindow
from src.system.platform_check import PlatformCheck
from src.utils.logger import get_logger


def main() -> int:
    """Application entry point."""
    logger = get_logger()
    logger.info('IWS-WinCare starting')
    
    system_info = PlatformCheck.check_system()
    logger.info(
        f'System: {system_info.os_name} {system_info.os_version} '
        f'({system_info.architecture})'
    )
    
    if not system_info.is_compatible:
        logger.error(f'Compatibility check failed: {system_info.compatibility_message}')
        print(f'Error: {system_info.compatibility_message}')
        return 1
    
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName('IWS-WinCare')
    app.setApplicationVersion('1.0.0')
    app.setOrganizationName('IWS-Webcode')
    
    font = QFont('Segoe UI', 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    logger.info('Application window displayed')
    
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
