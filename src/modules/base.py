"""
Base class for all repair and reset modules.
Provides common interface and execution patterns.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List

from src.core.executor import ExecutionResult, ExecutionStatus
from src.core.validator import Validator, ValidationResult
from src.system.commands import CommandRunner
from src.utils.logger import get_logger


@dataclass
class ModuleInfo:
    """Module metadata container."""
    name: str
    description: str
    category: str
    requires_admin: bool
    requires_reboot: bool
    is_critical: bool


class BaseModule(ABC):
    """
    Abstract base class for all repair/reset modules.
    Enforces consistent interface and execution patterns.
    """
    
    def __init__(self) -> None:
        self._logger = get_logger()
        self._validator = Validator()
        self._runner = CommandRunner()
    
    @property
    @abstractmethod
    def info(self) -> ModuleInfo:
        """Return module metadata."""
        pass
    
    @abstractmethod
    def _execute(self) -> ExecutionResult:
        """
        Internal execution logic.
        Subclasses must implement this method.
        """
        pass
    
    def validate(self) -> ValidationResult:
        """
        Pre-execution validation.
        Override to add module-specific checks.
        """
        return self._validator.validate_all(
            require_admin=self.info.requires_admin
        )
    
    def execute(self) -> ExecutionResult:
        """
        Execute the module with validation.
        
        Returns:
            ExecutionResult with success/failure status
        """
        self._logger.info(f'Executing module: {self.info.name}')
        
        validation = self.validate()
        if not validation.valid:
            self._logger.warning(f'Validation failed for {self.info.name}')
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Validation failed',
                details='\n'.join(validation.messages)
            )
        
        try:
            result = self._execute()
            
            if result.success:
                self._logger.info(f'Module {self.info.name} completed successfully')
            else:
                self._logger.warning(f'Module {self.info.name} failed: {result.message}')
            
            return result
            
        except Exception as e:
            self._logger.exception(f'Module {self.info.name} raised exception')
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Execution error',
                details=str(e),
                error=e
            )
