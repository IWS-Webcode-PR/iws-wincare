"""
DNS Cache Flush Module.
Clears the Windows DNS resolver cache.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class DNSFlushModule(BaseModule):
    """Flush Windows DNS resolver cache."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='DNS Cache Flush',
            description='Clears the DNS resolver cache to resolve DNS-related connectivity issues',
            category='Network',
            requires_admin=True,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        result = self._runner.run(['ipconfig', '/flushdns'])
        
        if result.success:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='DNS cache flushed successfully',
                details=result.stdout
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Failed to flush DNS cache',
            details=result.stderr or result.stdout
        )
