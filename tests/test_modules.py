"""
Unit tests for repair and reset modules.
Tests module interface compliance and basic functionality.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.modules.base import BaseModule, ModuleInfo
from src.core.executor import ExecutionResult, ExecutionStatus


class MockModule(BaseModule):
    """Mock module for testing base class behavior."""
    
    @property
    def info(self) -> ModuleInfo:
        return ModuleInfo(
            name='Test Module',
            description='A test module',
            category='Test',
            requires_admin=False,
            requires_reboot=False,
            is_critical=False
        )
    
    def _execute(self) -> ExecutionResult:
        return ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='Test completed'
        )


class TestModuleInterface(unittest.TestCase):
    """Test module interface compliance."""
    
    def test_module_has_info(self):
        """Module must provide ModuleInfo."""
        module = MockModule()
        info = module.info
        
        self.assertIsInstance(info, ModuleInfo)
        self.assertIsNotNone(info.name)
        self.assertIsNotNone(info.description)
        self.assertIsNotNone(info.category)
    
    def test_module_execute_returns_result(self):
        """Module execution must return ExecutionResult."""
        module = MockModule()
        
        with patch.object(module._validator, 'validate_all') as mock_validate:
            mock_validate.return_value = MagicMock(valid=True)
            result = module.execute()
        
        self.assertIsInstance(result, ExecutionResult)
        self.assertIn(result.status, ExecutionStatus)


class TestExecutionResult(unittest.TestCase):
    """Test ExecutionResult behavior."""
    
    def test_success_property(self):
        """Success property should match SUCCESS status."""
        success_result = ExecutionResult(
            status=ExecutionStatus.SUCCESS,
            message='OK'
        )
        failure_result = ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Error'
        )
        
        self.assertTrue(success_result.success)
        self.assertFalse(failure_result.success)
    
    def test_result_details(self):
        """Result should store details and error."""
        result = ExecutionResult(
            status=ExecutionStatus.FAILED,
            message='Failed',
            details='Additional info',
            error=ValueError('Test error')
        )
        
        self.assertEqual(result.details, 'Additional info')
        self.assertIsInstance(result.error, ValueError)


class TestModuleInfo(unittest.TestCase):
    """Test ModuleInfo dataclass."""
    
    def test_module_info_fields(self):
        """ModuleInfo must have all required fields."""
        info = ModuleInfo(
            name='Test',
            description='Desc',
            category='Cat',
            requires_admin=True,
            requires_reboot=False,
            is_critical=True
        )
        
        self.assertEqual(info.name, 'Test')
        self.assertEqual(info.description, 'Desc')
        self.assertEqual(info.category, 'Cat')
        self.assertTrue(info.requires_admin)
        self.assertFalse(info.requires_reboot)
        self.assertTrue(info.is_critical)


if __name__ == '__main__':
    unittest.main()
