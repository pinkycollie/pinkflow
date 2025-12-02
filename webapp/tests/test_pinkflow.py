#!/usr/bin/env python3
"""
Tests for PinkFlow model testing functionality
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from backend.pinkflow import (
    PinkFlowTester,
    ModelTestResult,
    ModelTestStatus,
    ModelDetector
)
from backend.pinkflow_mcp import (
    MCPGitHubTester,
    run_test_on_repo,
    batch_test_repos
)


class TestModelTestStatus:
    """Test ModelTestStatus enum"""

    def test_status_values(self):
        """Test that all status values are correct"""
        assert ModelTestStatus.GREEN.value == "GREEN"
        assert ModelTestStatus.YELLOW.value == "YELLOW"
        assert ModelTestStatus.RED.value == "RED"
        assert ModelTestStatus.ERROR.value == "ERROR"


class TestModelTestResult:
    """Test ModelTestResult dataclass"""

    def test_result_creation(self):
        """Test creating a test result"""
        result = ModelTestResult(
            status=ModelTestStatus.GREEN,
            accuracy=0.95,
            precision=0.93,
            recall=0.97,
            f1_score=0.95,
            processing_time=2.5,
            errors=[],
            metadata={"model_type": "asl_recognition"}
        )
        assert result.status == ModelTestStatus.GREEN
        assert result.accuracy == 0.95

    def test_result_to_dict(self):
        """Test converting result to dictionary"""
        result = ModelTestResult(
            status=ModelTestStatus.GREEN,
            accuracy=0.95,
            precision=0.93,
            recall=0.97,
            f1_score=0.95,
            processing_time=2.5,
            errors=[],
            metadata={}
        )
        data = result.to_dict()
        assert data["status"] == "GREEN"
        assert data["accuracy"] == 0.95


class TestModelDetector:
    """Test ModelDetector class"""

    def test_detect_unknown_model(self, tmp_path):
        """Test detecting unknown model type"""
        result = ModelDetector.detect_model_type(tmp_path)
        assert result is None

    def test_detect_pytorch_model(self, tmp_path):
        """Test detecting PyTorch model"""
        (tmp_path / 'model.pt').write_text('')
        (tmp_path / 'README.md').write_text('ASL recognition model')
        result = ModelDetector.detect_model_type(tmp_path)
        assert result == 'asl_recognition'

    def test_detect_fingerspelling_model(self, tmp_path):
        """Test detecting fingerspelling model"""
        (tmp_path / 'model.pt').write_text('')
        (tmp_path / 'README.md').write_text('ASL fingerspelling model')
        result = ModelDetector.detect_model_type(tmp_path)
        assert result == 'asl_fingerspelling'


class TestPinkFlowTester:
    """Test PinkFlowTester class"""

    def test_tester_initialization(self):
        """Test tester initialization"""
        tester = PinkFlowTester()
        assert tester.results == []

    def test_test_nonexistent_path(self):
        """Test testing non-existent path"""
        tester = PinkFlowTester()
        result = tester.test_local_model(Path('/nonexistent/path'))
        assert result.status == ModelTestStatus.ERROR
        assert len(result.errors) > 0


class TestMCPGitHubTester:
    """Test MCPGitHubTester class"""

    def test_mcp_tester_initialization(self):
        """Test MCP tester initialization"""
        tester = MCPGitHubTester()
        assert tester.test_results == []

    def test_get_repo_info(self):
        """Test getting repo info"""
        tester = MCPGitHubTester()
        info = tester._get_repo_info('https://github.com/user/repo')
        assert info['owner'] == 'user'
        assert info['repo'] == 'repo'
        assert info['accessible'] == True

    def test_get_repo_info_invalid(self):
        """Test getting repo info for invalid URL"""
        tester = MCPGitHubTester()
        info = tester._get_repo_info('invalid-url')
        assert 'error' in info

    def test_test_repo_with_mcp(self):
        """Test testing repo with MCP"""
        tester = MCPGitHubTester()
        result = tester.test_repo_with_mcp('https://github.com/user/asl-model')
        assert 'repo' in result
        assert 'repo_info' in result
        assert 'model_type' in result
        assert 'test_results' in result
        assert 'passed' in result


class TestPublicAPI:
    """Test public API functions"""

    def test_run_test_on_repo(self, tmp_path):
        """Test run_test_on_repo function"""
        result = run_test_on_repo('https://github.com/user/model')
        assert 'repo' in result
        assert 'passed' in result

    def test_run_test_on_repo_with_output(self, tmp_path):
        """Test run_test_on_repo with output file"""
        output_file = str(tmp_path / 'result.json')
        result = run_test_on_repo('https://github.com/user/model', output_file)
        assert Path(output_file).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
