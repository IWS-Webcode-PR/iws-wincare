"""
Environment Variables Refresh Module.
Broadcasts environment change notification to all windows.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class EnvironmentRefreshModule(BaseModule):
    """Refresh environment variables without restart."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Environment Variables Refresh',
            description='Broadcasts WM_SETTINGCHANGE to refresh environment variables',
            category='System',
            requires_admin=False,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        # Uses Win32 API through PowerShell to broadcast setting change
        ps_script = '''
        Add-Type -TypeDefinition @"
        using System;
        using System.Runtime.InteropServices;
        public class EnvRefresh {
            [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
            private static extern IntPtr SendMessageTimeout(
                IntPtr hWnd,
                uint Msg,
                UIntPtr wParam,
                string lParam,
                uint fuFlags,
                uint uTimeout,
                out UIntPtr lpdwResult
            );
            
            public static void Refresh() {
                IntPtr HWND_BROADCAST = (IntPtr)0xffff;
                uint WM_SETTINGCHANGE = 0x001A;
                uint SMTO_ABORTIFHUNG = 0x0002;
                UIntPtr result;
                
                SendMessageTimeout(
                    HWND_BROADCAST,
                    WM_SETTINGCHANGE,
                    UIntPtr.Zero,
                    "Environment",
                    SMTO_ABORTIFHUNG,
                    5000,
                    out result
                );
            }
        }
"@
        [EnvRefresh]::Refresh()
        Write-Output "Environment variables refreshed"
        '''
        
        result = self._runner.run_powershell(ps_script, timeout=30)
        
        if result.success:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                message='Environment variables refreshed successfully',
                details='WM_SETTINGCHANGE broadcast sent to all windows'
            )
        
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Failed to refresh environment variables',
            details=result.stderr or result.stdout
        )
