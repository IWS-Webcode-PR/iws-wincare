"""
Start Menu and Explorer Reset Module.
Resets Start Menu and Explorer shell settings.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class StartMenuResetModule(BaseModule):
    """Reset Start Menu and Explorer to default state."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Start Menu & Explorer Reset',
            description='Resets Start Menu layout and Explorer settings to defaults',
            category='System',
            requires_admin=True,
            requires_reboot=False,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        ps_script = '''
        $operations = @()
        
        # Stop Explorer
        Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
        $operations += "[OK] Explorer stopped"
        
        # Reset Start Menu layout (Windows 10)
        $startLayoutPath = "$env:LOCALAPPDATA\\Microsoft\\Windows\\Shell\\LayoutModification.xml"
        if (Test-Path $startLayoutPath) {
            Remove-Item -Path $startLayoutPath -Force -ErrorAction SilentlyContinue
            $operations += "[OK] Start layout file removed"
        }
        
        # Clear Start Menu cache
        $startCachePaths = @(
            "$env:LOCALAPPDATA\\Packages\\Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy\\LocalState",
            "$env:LOCALAPPDATA\\Packages\\Microsoft.Windows.ShellExperienceHost_cw5n1h2txyewy\\LocalState"
        )
        
        foreach ($path in $startCachePaths) {
            if (Test-Path $path) {
                Remove-Item -Path "$path\\*" -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
        $operations += "[OK] Start Menu cache cleared"
        
        # Reset Explorer settings in registry
        $explorerRegPath = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"
        Set-ItemProperty -Path $explorerRegPath -Name "Hidden" -Value 1 -ErrorAction SilentlyContinue
        Set-ItemProperty -Path $explorerRegPath -Name "ShowSuperHidden" -Value 0 -ErrorAction SilentlyContinue
        Set-ItemProperty -Path $explorerRegPath -Name "HideFileExt" -Value 1 -ErrorAction SilentlyContinue
        $operations += "[OK] Explorer settings reset"
        
        # Re-register Start Menu apps (Windows 10/11)
        try {
            Get-AppxPackage Microsoft.Windows.StartMenuExperienceHost -ErrorAction SilentlyContinue | 
                ForEach-Object { Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\\AppXManifest.xml" -ErrorAction SilentlyContinue }
            $operations += "[OK] Start Menu re-registered"
        } catch {
            $operations += "[WARN] Start Menu re-registration skipped"
        }
        
        # Restart Explorer
        Start-Process explorer.exe
        $operations += "[OK] Explorer restarted"
        
        $operations -join "`n"
        '''
        
        result = self._runner.run_powershell(ps_script, timeout=60)
        
        if result.success:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='Start Menu and Explorer reset completed',
                details=result.stdout
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Start Menu and Explorer reset failed',
            details=result.stderr or result.stdout
        )
