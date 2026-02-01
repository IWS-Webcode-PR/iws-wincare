"""
Windows Update Cache Repair Module.
Clears and repairs the Windows Update cache.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class UpdateCacheModule(BaseModule):
    """Repair Windows Update cache to fix update failures."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Windows Update Cache Repair',
            description='Stops update services, clears cache, and restarts services',
            category='System',
            requires_admin=True,
            requires_reboot=False,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        errors = []
        success_count = 0
        
        # Stop Windows Update services
        services_to_stop = ['wuauserv', 'bits', 'cryptsvc']
        for service in services_to_stop:
            result = self._runner.run(['net', 'stop', service])
            if not result.success and 'not started' not in result.stderr.lower():
                errors.append(f'Failed to stop {service}')
            else:
                success_count += 1
        
        # Clear SoftwareDistribution folder
        ps_clear = '''
        $paths = @(
            "$env:SystemRoot\\SoftwareDistribution\\Download\\*",
            "$env:SystemRoot\\SoftwareDistribution\\DataStore\\*"
        )
        foreach ($path in $paths) {
            if (Test-Path $path) {
                Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
        Write-Output "Cache cleared"
        '''
        
        clear_result = self._runner.run_powershell(ps_clear)
        if clear_result.success:
            success_count += 1
        else:
            errors.append('Failed to clear update cache')
        
        # Restart services
        for service in services_to_stop:
            result = self._runner.run(['net', 'start', service])
            if result.success:
                success_count += 1
        
        if errors:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Update cache repair completed with errors',
                details='\n'.join(errors)
            )
        
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Windows Update cache repaired successfully',
            details=f'Completed {success_count} operations'
        )
