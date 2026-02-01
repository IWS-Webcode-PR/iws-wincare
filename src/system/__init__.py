"""System-level operations package."""

from src.system.admin import AdminPrivileges, is_admin, request_admin
from src.system.platform_check import PlatformCheck
from src.system.commands import CommandRunner, CommandResult

__all__ = [
    'AdminPrivileges', 'is_admin', 'request_admin',
    'PlatformCheck', 'CommandRunner', 'CommandResult'
]
