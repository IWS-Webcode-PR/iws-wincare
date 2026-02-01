"""
Temporary Files Cleanup Module.
Safely removes temporary files from system directories.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class TempCleanupModule(BaseModule):
    """Remove temporary files to free disk space and resolve issues."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Temporary Files Cleanup',
            description='Removes temporary files from Windows and user temp directories',
            category='Cleanup',
            requires_admin=True,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        ps_script = '''
        $totalSize = 0
        $filesDeleted = 0
        
        $tempPaths = @(
            $env:TEMP,
            "$env:SystemRoot\\Temp",
            "$env:LOCALAPPDATA\\Temp"
        )
        
        foreach ($path in $tempPaths) {
            if (Test-Path $path) {
                $files = Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue
                foreach ($file in $files) {
                    try {
                        $totalSize += $file.Length
                        Remove-Item -Path $file.FullName -Force -Recurse -ErrorAction Stop
                        $filesDeleted++
                    } catch {
                        # File in use, skip
                    }
                }
            }
        }
        
        # Clear Windows prefetch (requires admin)
        $prefetchPath = "$env:SystemRoot\\Prefetch"
        if (Test-Path $prefetchPath) {
            $prefetchFiles = Get-ChildItem -Path $prefetchPath -ErrorAction SilentlyContinue
            foreach ($file in $prefetchFiles) {
                try {
                    $totalSize += $file.Length
                    Remove-Item -Path $file.FullName -Force -ErrorAction Stop
                    $filesDeleted++
                } catch {
                    # Access denied, skip
                }
            }
        }
        
        $sizeMB = [math]::Round($totalSize / 1MB, 2)
        Write-Output "Deleted $filesDeleted files, freed $sizeMB MB"
        '''
        
        result = self._runner.run_powershell(ps_script, timeout=120)
        
        if result.success:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='Temporary files cleaned successfully',
                details=result.stdout
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Cleanup completed with errors',
            details=result.stderr or result.stdout
        )
