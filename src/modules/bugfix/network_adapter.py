"""
Network Adapter Restart Module.
Disables and re-enables all network adapters.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus
import time


class NetworkAdapterModule(BaseModule):
    """Restart network adapters to resolve connectivity issues."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Network Adapter Restart',
            description='Restarts all network adapters to resolve connectivity issues',
            category='Network',
            requires_admin=True,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        # Get list of enabled network adapters
        ps_script = '''
        $adapters = Get-NetAdapter | Where-Object {$_.Status -eq 'Up'}
        foreach ($adapter in $adapters) {
            Disable-NetAdapter -Name $adapter.Name -Confirm:$false
            Start-Sleep -Seconds 2
            Enable-NetAdapter -Name $adapter.Name -Confirm:$false
        }
        Write-Output "Restarted $($adapters.Count) network adapter(s)"
        '''
        
        result = self._runner.run_powershell(ps_script, timeout=60)
        
        if result.success:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='Network adapters restarted successfully',
                details=result.stdout
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Failed to restart network adapters',
            details=result.stderr or result.stdout
        )
