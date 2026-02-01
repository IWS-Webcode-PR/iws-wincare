"""Bug-fix modules for Windows repair operations."""

from src.modules.bugfix.dns_flush import DNSFlushModule
from src.modules.bugfix.winsock_reset import WinsockResetModule
from src.modules.bugfix.network_adapter import NetworkAdapterModule
from src.modules.bugfix.update_cache import UpdateCacheModule
from src.modules.bugfix.explorer_cache import ExplorerCacheModule
from src.modules.bugfix.temp_cleanup import TempCleanupModule
from src.modules.bugfix.env_refresh import EnvironmentRefreshModule

__all__ = [
    'DNSFlushModule',
    'WinsockResetModule',
    'NetworkAdapterModule',
    'UpdateCacheModule',
    'ExplorerCacheModule',
    'TempCleanupModule',
    'EnvironmentRefreshModule',
]
