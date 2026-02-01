"""
Winsock Reset Module.
Resets Windows Sockets catalog to default state.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class WinsockResetModule(BaseModule):
    """Reset Winsock catalog to fix network connectivity issues."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Winsock Reset',
            description='Resets Windows Sockets catalog to resolve network stack corruption',
            category='Network',
            requires_admin=True,
            requires_reboot=True,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        result = self._runner.run(['netsh', 'winsock', 'reset'])
        
        if result.success or 'successfully' in result.stdout.lower():
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='Winsock catalog reset successfully. Restart required.',
                details=result.stdout
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Failed to reset Winsock catalog',
            details=result.stderr or result.stdout
        )
