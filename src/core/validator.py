"""
Pre-execution validation for repair and reset modules.
Ensures system state is suitable for operations.
"""

from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

from src.system.admin import is_admin
from src.system.platform_check import PlatformCheck
from src.utils.logger import get_logger


@dataclass
class ValidationResult:
    """Container for validation results."""
    valid: bool
    messages: List[str]
    warnings: List[str]
    
    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


class Validator:
    """Pre-execution validation checks."""
    
    def __init__(self) -> None:
        self._logger = get_logger()
    
    def validate_admin(self) -> ValidationResult:
        """Check if running with administrator privileges."""
        if is_admin():
            return ValidationResult(
                valid=True,
                messages=['Running with administrator privileges'],
                warnings=[]
            )
        return ValidationResult(
            valid=False,
            messages=['Administrator privileges required'],
            warnings=[]
        )
    
    def validate_platform(self) -> ValidationResult:
        """Check if running on supported Windows version."""
        info = PlatformCheck.check_system()
        
        if info.is_compatible:
            return ValidationResult(
                valid=True,
                messages=[f'Running on {info.os_name} {info.os_version}'],
                warnings=[]
            )
        return ValidationResult(
            valid=False,
            messages=[info.compatibility_message],
            warnings=[]
        )
    
    def validate_service_exists(self, service_name: str) -> ValidationResult:
        """Check if a Windows service exists."""
        from ..system.commands import CommandRunner
        
        runner = CommandRunner()
        result = runner.run(['sc', 'query', service_name])
        
        if result.success:
            return ValidationResult(
                valid=True,
                messages=[f'Service {service_name} exists'],
                warnings=[]
            )
        return ValidationResult(
            valid=False,
            messages=[f'Service {service_name} not found'],
            warnings=[]
        )
    
    def validate_path_exists(self, path: str) -> ValidationResult:
        """Check if a file or directory path exists."""
        target = Path(path)
        
        if target.exists():
            return ValidationResult(
                valid=True,
                messages=[f'Path exists: {path}'],
                warnings=[]
            )
        return ValidationResult(
            valid=False,
            messages=[f'Path not found: {path}'],
            warnings=[]
        )
    
    def validate_all(
        self,
        require_admin: bool = True,
        paths: Optional[List[str]] = None,
        services: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        Perform comprehensive validation.
        
        Args:
            require_admin: Whether admin privileges are required
            paths: List of paths that must exist
            services: List of services that must exist
        
        Returns:
            Combined validation result
        """
        all_messages: List[str] = []
        all_warnings: List[str] = []
        is_valid = True
        
        # Platform check
        platform_result = self.validate_platform()
        all_messages.extend(platform_result.messages)
        all_warnings.extend(platform_result.warnings)
        if not platform_result.valid:
            is_valid = False
        
        # Admin check
        if require_admin:
            admin_result = self.validate_admin()
            all_messages.extend(admin_result.messages)
            all_warnings.extend(admin_result.warnings)
            if not admin_result.valid:
                is_valid = False
        
        # Path checks
        if paths:
            for path in paths:
                path_result = self.validate_path_exists(path)
                if not path_result.valid:
                    all_warnings.append(path_result.messages[0])
        
        # Service checks
        if services:
            for service in services:
                service_result = self.validate_service_exists(service)
                if not service_result.valid:
                    all_warnings.append(service_result.messages[0])
        
        return ValidationResult(
            valid=is_valid,
            messages=all_messages,
            warnings=all_warnings
        )
