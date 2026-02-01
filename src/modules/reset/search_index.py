"""
Windows Search Index Module.
Rebuilds the Windows Search index.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class SearchIndexModule(BaseModule):
    """Rebuild Windows Search index to fix search issues."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Search Index Rebuild',
            description='Stops search service, clears index, and rebuilds from scratch',
            category='System',
            requires_admin=True,
            requires_reboot=False,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        operations = []
        errors = []
        
        # Stop Windows Search service
        result = self._runner.run(['net', 'stop', 'WSearch'])
        if result.success or 'not started' in result.stderr.lower():
            operations.append('[OK] Windows Search service stopped')
        else:
            errors.append('Failed to stop Windows Search service')
            operations.append('[FAIL] Stop Windows Search service')
        
        # Delete index files
        ps_delete = '''
        $indexPath = "$env:ProgramData\\Microsoft\\Search\\Data\\Applications\\Windows"
        if (Test-Path $indexPath) {
            Remove-Item -Path "$indexPath\\*" -Recurse -Force -ErrorAction SilentlyContinue
            Write-Output "Index files deleted"
        } else {
            Write-Output "Index path not found"
        }
        '''
        
        delete_result = self._runner.run_powershell(ps_delete)
        if delete_result.success:
            operations.append('[OK] Search index files deleted')
        else:
            errors.append('Failed to delete index files')
            operations.append('[FAIL] Delete search index files')
        
        # Start Windows Search service
        result = self._runner.run(['net', 'start', 'WSearch'])
        if result.success:
            operations.append('[OK] Windows Search service started')
            operations.append('[INFO] Index rebuild will occur in background')
        else:
            errors.append('Failed to start Windows Search service')
            operations.append('[FAIL] Start Windows Search service')
        
        details = '\n'.join(operations)
        
        if len(errors) > 1:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Search index rebuild failed',
                details=details
            )
        
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Search index rebuild initiated',
            details=details
        )
