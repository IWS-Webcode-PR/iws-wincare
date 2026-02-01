"""
Power Plan Reset Module.
Restores Windows default power plans.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class PowerPlanResetModule(BaseModule):
    """Reset power plans to Windows defaults."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Power Plan Reset',
            description='Restores all power plans to Windows default settings',
            category='System',
            requires_admin=True,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        # Default power plan GUIDs
        default_plans = {
            '381b4222-f694-41f0-9685-ff5bb260df2e': 'Balanced',
            '8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c': 'High Performance',
            'a1841308-3541-4fab-bc81-f71556f20b4a': 'Power Saver',
        }
        
        errors = []
        operations = []
        
        # Restore default power schemes
        result = self._runner.run(['powercfg', '-restoredefaultschemes'])
        if result.success:
            operations.append('[OK] Default power schemes restored')
        else:
            errors.append('Failed to restore default schemes')
            operations.append('[FAIL] Default power schemes restoration')
        
        # Set Balanced as active plan
        balanced_guid = '381b4222-f694-41f0-9685-ff5bb260df2e'
        result = self._runner.run(['powercfg', '-setactive', balanced_guid])
        if result.success:
            operations.append('[OK] Balanced plan activated')
        else:
            errors.append('Failed to activate Balanced plan')
            operations.append('[FAIL] Balanced plan activation')
        
        details = '\n'.join(operations)
        
        if errors:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Power plan reset completed with errors',
                details=details
            )
        
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Power plans reset to Windows defaults',
            details=details
        )
