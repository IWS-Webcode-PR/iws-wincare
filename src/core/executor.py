"""
Module execution engine.
Handles async execution of repair and reset modules with proper error handling.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, Any
from concurrent.futures import ThreadPoolExecutor, Future
import threading

from ..utils.logger import get_logger


class ExecutionStatus(Enum):
    """Status codes for module execution."""
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


@dataclass
class ExecutionResult:
    """Container for module execution results."""
    status: ExecutionStatus
    message: str
    details: Optional[str] = None
    error: Optional[Exception] = None
    
    @property
    def success(self) -> bool:
        return self.status == ExecutionStatus.SUCCESS


class ModuleExecutor:
    """
    Thread-safe executor for running repair/reset modules.
    Supports progress callbacks and cancellation.
    """
    
    def __init__(self, max_workers: int = 1) -> None:
        self._logger = get_logger()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._current_task: Optional[Future] = None
        self._cancel_flag = threading.Event()
    
    def execute(
        self,
        module_func: Callable[[], ExecutionResult],
        on_complete: Optional[Callable[[ExecutionResult], None]] = None,
        on_progress: Optional[Callable[[str], None]] = None
    ) -> Future:
        """
        Execute a module function asynchronously.
        
        Args:
            module_func: The module function to execute
            on_complete: Callback when execution completes
            on_progress: Callback for progress updates
        
        Returns:
            Future representing the execution
        """
        self._cancel_flag.clear()
        
        def wrapper() -> ExecutionResult:
            try:
                if self._cancel_flag.is_set():
                    return ExecutionResult(
                        status=ExecutionStatus.CANCELLED,
                        message='Execution cancelled'
                    )
                
                if on_progress:
                    on_progress('Starting execution...')
                
                result = module_func()
                
                if self._cancel_flag.is_set():
                    return ExecutionResult(
                        status=ExecutionStatus.CANCELLED,
                        message='Execution cancelled'
                    )
                
                return result
                
            except Exception as e:
                self._logger.exception('Module execution failed')
                return ExecutionResult(
                    status=ExecutionStatus.FAILED,
                    message='Execution failed',
                    details=str(e),
                    error=e
                )
        
        def done_callback(future: Future) -> None:
            if on_complete:
                try:
                    result = future.result()
                    on_complete(result)
                except Exception as e:
                    on_complete(ExecutionResult(
                        status=ExecutionStatus.FAILED,
                        message='Callback error',
                        error=e
                    ))
        
        self._current_task = self._executor.submit(wrapper)
        self._current_task.add_done_callback(done_callback)
        
        return self._current_task
    
    def execute_sync(self, module_func: Callable[[], ExecutionResult]) -> ExecutionResult:
        """Execute a module function synchronously."""
        try:
            return module_func()
        except Exception as e:
            self._logger.exception('Sync module execution failed')
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                message='Execution failed',
                details=str(e),
                error=e
            )
    
    def cancel(self) -> bool:
        """Request cancellation of current execution."""
        self._cancel_flag.set()
        if self._current_task and not self._current_task.done():
            return self._current_task.cancel()
        return True
    
    def is_running(self) -> bool:
        """Check if an execution is currently in progress."""
        return self._current_task is not None and not self._current_task.done()
    
    def shutdown(self) -> None:
        """Shutdown the executor and release resources."""
        self._executor.shutdown(wait=False)
