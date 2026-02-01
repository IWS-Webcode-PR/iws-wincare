"""
Explorer Cache Reset Module.
Clears Windows Explorer icon and thumbnail caches.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class ExplorerCacheModule(BaseModule):
    """Reset Windows Explorer caches to fix display issues."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Explorer Cache Reset',
            description='Clears icon cache and thumbnail cache to fix display issues',
            category='System',
            requires_admin=True,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        ps_script = '''
        # Kill explorer to release file locks
        Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        
        # Clear icon cache
        $iconCachePath = "$env:LOCALAPPDATA\\IconCache.db"
        if (Test-Path $iconCachePath) {
            Remove-Item -Path $iconCachePath -Force -ErrorAction SilentlyContinue
        }
        
        # Clear all iconcache files
        $iconCacheFiles = Get-ChildItem -Path "$env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer" -Filter "iconcache*.db" -ErrorAction SilentlyContinue
        foreach ($file in $iconCacheFiles) {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        }
        
        # Clear thumbnail cache
        $thumbCacheFiles = Get-ChildItem -Path "$env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer" -Filter "thumbcache*.db" -ErrorAction SilentlyContinue
        foreach ($file in $thumbCacheFiles) {
            Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
        }
        
        # Restart explorer
        Start-Process explorer.exe
        
        Write-Output "Explorer cache cleared successfully"
        '''
        
        result = self._runner.run_powershell(ps_script, timeout=30)
        
        if result.success:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='Explorer cache reset successfully',
                details=result.stdout
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Failed to reset Explorer cache',
            details=result.stderr or result.stdout
        )
