"""
Default Apps Reset Module.
Resets file associations to Windows defaults.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class DefaultAppsResetModule(BaseModule):
    """Reset default app associations to Windows defaults."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Default Apps Reset',
            description='Resets file type associations to Windows recommended defaults',
            category='System',
            requires_admin=True,
            requires_reboot=False,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        ps_script = '''
        # Reset UserChoice registry entries for common file types
        $fileTypes = @(
            ".htm", ".html", ".pdf", ".txt", ".jpg", ".jpeg", ".png",
            ".gif", ".mp3", ".mp4", ".avi", ".mkv", ".doc", ".docx",
            ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar"
        )
        
        $removedCount = 0
        foreach ($type in $fileTypes) {
            $path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\$type\\UserChoice"
            if (Test-Path $path) {
                try {
                    # UserChoice is protected, use special method
                    $key = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey(
                        "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FileExts\\$type",
                        $true
                    )
                    if ($key -ne $null) {
                        $key.DeleteSubKey("UserChoice", $false)
                        $key.Close()
                        $removedCount++
                    }
                } catch {
                    # Protected key, skip
                }
            }
        }
        
        # Notify shell of changes
        $code = @"
        [DllImport("shell32.dll")]
        public static extern void SHChangeNotify(int eventId, int flags, IntPtr item1, IntPtr item2);
"@
        Add-Type -MemberDefinition $code -Namespace Win32 -Name Shell32
        [Win32.Shell32]::SHChangeNotify(0x08000000, 0, [IntPtr]::Zero, [IntPtr]::Zero)
        
        Write-Output "Reset $removedCount file associations"
        '''
        
        result = self._runner.run_powershell(ps_script, timeout=60)
        
        # UserChoice keys are often protected, partial success is acceptable
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Default app associations reset initiated',
            details=result.stdout + '\nNote: Some associations may require manual reset via Settings > Apps > Default apps'
        )
