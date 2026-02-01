"""
Platform compatibility checks.
Validates Windows version and system requirements.
"""

import platform
import sys
from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class SystemInfo:
    """Container for system information."""
    os_name: str
    os_version: str
    os_build: str
    architecture: str
    python_version: str
    is_compatible: bool
    compatibility_message: str


class PlatformCheck:
    """Validates system compatibility requirements."""
    
    SUPPORTED_VERSIONS = {
        '10': (10, 0, 19041),  # Windows 10 2004+
        '11': (10, 0, 22000),  # Windows 11
    }
    
    @staticmethod
    def get_windows_version() -> Tuple[int, int, int]:
        """
        Get Windows version as tuple (major, minor, build).
        Returns (0, 0, 0) if detection fails.
        """
        try:
            version = platform.version()
            build = int(version.split('.')[2]) if '.' in version else 0
            win_ver = sys.getwindowsversion()
            return (win_ver.major, win_ver.minor, build)
        except (AttributeError, ValueError, IndexError):
            return (0, 0, 0)
    
    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows."""
        return platform.system() == 'Windows'
    
    @staticmethod
    def is_windows_10_or_11() -> bool:
        """Check if running on Windows 10 or 11."""
        if not PlatformCheck.is_windows():
            return False
        
        major, minor, build = PlatformCheck.get_windows_version()
        
        # Windows 10: build < 22000, Windows 11: build >= 22000
        return major == 10 and minor == 0 and build >= 19041
    
    @staticmethod
    def get_windows_edition() -> str:
        """Get Windows edition string."""
        try:
            return platform.win32_edition()
        except AttributeError:
            return 'Unknown'
    
    @staticmethod
    def check_system() -> SystemInfo:
        """Perform full system compatibility check."""
        os_name = platform.system()
        os_version = platform.release()
        
        try:
            os_build = platform.version()
        except Exception:
            os_build = 'Unknown'
        
        architecture = platform.machine()
        python_version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
        
        is_compatible = True
        message = 'System is compatible'
        
        if not PlatformCheck.is_windows():
            is_compatible = False
            message = 'This tool requires Windows operating system'
        elif not PlatformCheck.is_windows_10_or_11():
            is_compatible = False
            message = 'This tool requires Windows 10 (2004+) or Windows 11'
        elif sys.version_info < (3, 10):
            is_compatible = False
            message = 'This tool requires Python 3.10 or higher'
        
        return SystemInfo(
            os_name=os_name,
            os_version=os_version,
            os_build=os_build,
            architecture=architecture,
            python_version=python_version,
            is_compatible=is_compatible,
            compatibility_message=message
        )
