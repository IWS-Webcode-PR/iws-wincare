"""
Windows Update Soft-Reset Module.
Resets Windows Update components without reinstallation.
"""

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class UpdateResetModule(BaseModule):
    """Soft-reset Windows Update components."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Windows Update Soft-Reset',
            description='Resets Windows Update components, clears cache, and re-registers DLLs',
            category='System',
            requires_admin=True,
            requires_reboot=True,
            is_critical=True
        )
    
    def _execute(self) -> ExecutionResult:
        operations = []
        
        # Services to manage
        services = ['wuauserv', 'bits', 'cryptsvc', 'msiserver']
        
        # Stop services
        for service in services:
            result = self._runner.run(['net', 'stop', service])
            if result.success or 'not started' in result.stderr.lower():
                operations.append(f'[OK] Stopped {service}')
            else:
                operations.append(f'[WARN] Could not stop {service}')
        
        # Rename SoftwareDistribution folder
        ps_rename = '''
        $sdPath = "$env:SystemRoot\\SoftwareDistribution"
        $sdBackup = "$env:SystemRoot\\SoftwareDistribution.old"
        
        if (Test-Path $sdBackup) {
            Remove-Item -Path $sdBackup -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        if (Test-Path $sdPath) {
            Rename-Item -Path $sdPath -NewName "SoftwareDistribution.old" -Force -ErrorAction SilentlyContinue
        }
        
        $catroot2Path = "$env:SystemRoot\\System32\\catroot2"
        $catroot2Backup = "$env:SystemRoot\\System32\\catroot2.old"
        
        if (Test-Path $catroot2Backup) {
            Remove-Item -Path $catroot2Backup -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        if (Test-Path $catroot2Path) {
            Rename-Item -Path $catroot2Path -NewName "catroot2.old" -Force -ErrorAction SilentlyContinue
        }
        
        Write-Output "Folders renamed"
        '''
        
        rename_result = self._runner.run_powershell(ps_rename)
        if rename_result.success:
            operations.append('[OK] Update folders renamed')
        else:
            operations.append('[WARN] Could not rename all folders')
        
        # Re-register Windows Update DLLs
        dlls = [
            'atl.dll', 'urlmon.dll', 'mshtml.dll', 'shdocvw.dll',
            'browseui.dll', 'jscript.dll', 'vbscript.dll', 'scrrun.dll',
            'msxml.dll', 'msxml3.dll', 'msxml6.dll', 'actxprxy.dll',
            'softpub.dll', 'wintrust.dll', 'dssenh.dll', 'rsaenh.dll',
            'gpkcsp.dll', 'sccbase.dll', 'slbcsp.dll', 'cryptdlg.dll',
            'oleaut32.dll', 'ole32.dll', 'shell32.dll', 'initpki.dll',
            'wuapi.dll', 'wuaueng.dll', 'wuaueng1.dll', 'wucltui.dll',
            'wups.dll', 'wups2.dll', 'wuweb.dll', 'qmgr.dll', 'qmgrprxy.dll',
            'wucltux.dll', 'muweb.dll', 'wuwebv.dll'
        ]
        
        dll_success = 0
        for dll in dlls:
            result = self._runner.run(['regsvr32', '/s', dll])
            if result.success:
                dll_success += 1
        
        operations.append(f'[OK] Re-registered {dll_success}/{len(dlls)} DLLs')
        
        # Reset Winsock
        result = self._runner.run(['netsh', 'winsock', 'reset'])
        if result.success:
            operations.append('[OK] Winsock reset')
        
        # Start services
        for service in services:
            result = self._runner.run(['net', 'start', service])
            if result.success:
                operations.append(f'[OK] Started {service}')
            else:
                operations.append(f'[WARN] Could not start {service}')
        
        details = '\n'.join(operations)
        
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Windows Update soft-reset completed. Restart recommended.',
            details=details
        )
