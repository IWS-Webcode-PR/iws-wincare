"""
Network Reset Module.
Performs comprehensive network stack reset.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class NetworkResetModule(BaseModule):
    """Complete network stack reset including IP, Winsock, and optionally firewall."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Network Reset',
            description='Resets IP configuration, Winsock catalog, and network settings',
            category='Network',
            requires_admin=True,
            requires_reboot=True,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        errors = []
        operations = []
        
        # Reset IP configuration
        commands = [
            (['netsh', 'int', 'ip', 'reset'], 'IP configuration reset'),
            (['netsh', 'winsock', 'reset'], 'Winsock catalog reset'),
            (['netsh', 'advfirewall', 'reset'], 'Firewall rules reset'),
            (['ipconfig', '/release'], 'IP address released'),
            (['ipconfig', '/flushdns'], 'DNS cache flushed'),
            (['ipconfig', '/renew'], 'IP address renewed'),
        ]
        
        for cmd, description in commands:
            result = self._runner.run(cmd, timeout=30)
            if result.success:
                operations.append(f'[OK] {description}')
            else:
                errors.append(f'[FAIL] {description}')
                operations.append(f'[FAIL] {description}')
        
        details = '\n'.join(operations)
        
        if len(errors) > len(commands) // 2:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Network reset failed',
                details=details
            )
        
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Network reset completed. Restart required.',
            details=details
        )
