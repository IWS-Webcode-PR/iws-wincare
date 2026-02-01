"""
Administrator privileges management.
Handles elevation checks and UAC requests.
"""

import ctypes
import sys
import os
from typing import Optional


class AdminPrivileges:
    """Manages administrator privilege checks and elevation."""
    
    @staticmethod
    def is_admin() -> bool:
        """Check if the current process has administrator privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except (AttributeError, OSError):
            return False
    
    @staticmethod
    def request_elevation(script_path: Optional[str] = None) -> bool:
        """
        Request UAC elevation for the current script.
        Returns True if elevation was requested, False on failure.
        """
        if AdminPrivileges.is_admin():
            return True
        
        if script_path is None:
            script_path = sys.argv[0]
        
        try:
            params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
            
            result = ctypes.windll.shell32.ShellExecuteW(
                None,
                'runas',
                sys.executable,
                f'"{script_path}" {params}',
                None,
                1  # SW_SHOWNORMAL
            )
            
            # ShellExecuteW returns value > 32 on success
            return result > 32
        except (AttributeError, OSError):
            return False


def is_admin() -> bool:
    """Convenience function to check admin status."""
    return AdminPrivileges.is_admin()


def request_admin(script_path: Optional[str] = None) -> bool:
    """Convenience function to request elevation."""
    return AdminPrivileges.request_elevation(script_path)
