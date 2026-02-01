"""
Safe command execution wrapper.
Provides controlled subprocess execution without shell injection vulnerabilities.
"""

import subprocess
import shutil
from dataclasses import dataclass
from typing import List, Optional, Dict
from pathlib import Path

from src.utils.logger import get_logger


@dataclass
class CommandResult:
    """Container for command execution results."""
    success: bool
    return_code: int
    stdout: str
    stderr: str
    command: str
    
    @property
    def output(self) -> str:
        """Combined stdout and stderr output."""
        parts = []
        if self.stdout:
            parts.append(self.stdout)
        if self.stderr:
            parts.append(self.stderr)
        return '\n'.join(parts)


class CommandRunner:
    """
    Safe command execution with argument list (no shell=True).
    Prevents command injection vulnerabilities.
    """
    
    ALLOWED_COMMANDS = {
        'ipconfig': 'ipconfig.exe',
        'netsh': 'netsh.exe',
        'net': 'net.exe',
        'sc': 'sc.exe',
        'sfc': 'sfc.exe',
        'dism': 'dism.exe',
        'powercfg': 'powercfg.exe',
        'cmd': 'cmd.exe',
        'powershell': 'powershell.exe',
        'reg': 'reg.exe',
        'taskkill': 'taskkill.exe',
        'rundll32': 'rundll32.exe',
    }
    
    def __init__(self) -> None:
        self._logger = get_logger()
        self._system32 = Path(r'C:\Windows\System32')
    
    def _resolve_command(self, command: str) -> Optional[str]:
        """
        Resolve command to full system path.
        Returns None if command is not in allowed list.
        """
        cmd_lower = command.lower()
        
        if cmd_lower in self.ALLOWED_COMMANDS:
            executable = self.ALLOWED_COMMANDS[cmd_lower]
            full_path = self._system32 / executable
            
            if full_path.exists():
                return str(full_path)
            
            # Fallback to PATH resolution
            resolved = shutil.which(executable)
            if resolved:
                return resolved
        
        return None
    
    def run(
        self,
        args: List[str],
        timeout: int = 60,
        env: Optional[Dict[str, str]] = None,
        capture_output: bool = True
    ) -> CommandResult:
        """
        Execute command with argument list.
        
        Args:
            args: Command and arguments as list, e.g. ['ipconfig', '/flushdns']
            timeout: Maximum execution time in seconds
            env: Optional environment variables
            capture_output: Whether to capture stdout/stderr
        
        Returns:
            CommandResult with execution details
        """
        if not args:
            return CommandResult(
                success=False,
                return_code=-1,
                stdout='',
                stderr='No command provided',
                command=''
            )
        
        command_name = args[0]
        resolved_cmd = self._resolve_command(command_name)
        
        if resolved_cmd is None:
            self._logger.error(f'Command not allowed: {command_name}')
            return CommandResult(
                success=False,
                return_code=-1,
                stdout='',
                stderr=f'Command not allowed: {command_name}',
                command=command_name
            )
        
        full_args = [resolved_cmd] + args[1:]
        command_str = ' '.join(args)
        
        self._logger.debug(f'Executing: {command_str}')
        
        try:
            result = subprocess.run(
                full_args,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            success = result.returncode == 0
            
            if success:
                self._logger.debug(f'Command succeeded: {command_str}')
            else:
                self._logger.warning(f'Command returned {result.returncode}: {command_str}')
            
            return CommandResult(
                success=success,
                return_code=result.returncode,
                stdout=result.stdout or '',
                stderr=result.stderr or '',
                command=command_str
            )
            
        except subprocess.TimeoutExpired:
            self._logger.error(f'Command timed out: {command_str}')
            return CommandResult(
                success=False,
                return_code=-1,
                stdout='',
                stderr=f'Command timed out after {timeout} seconds',
                command=command_str
            )
        except FileNotFoundError:
            self._logger.error(f'Command not found: {resolved_cmd}')
            return CommandResult(
                success=False,
                return_code=-1,
                stdout='',
                stderr=f'Command not found: {resolved_cmd}',
                command=command_str
            )
        except Exception as e:
            self._logger.exception(f'Command execution failed: {command_str}')
            return CommandResult(
                success=False,
                return_code=-1,
                stdout='',
                stderr=str(e),
                command=command_str
            )
    
    def run_powershell(
        self,
        script: str,
        timeout: int = 120
    ) -> CommandResult:
        """
        Execute PowerShell script safely.
        
        Args:
            script: PowerShell script content
            timeout: Maximum execution time
        
        Returns:
            CommandResult with execution details
        """
        args = [
            'powershell',
            '-NoProfile',
            '-NonInteractive',
            '-ExecutionPolicy', 'Bypass',
            '-Command', script
        ]
        return self.run(args, timeout=timeout)
