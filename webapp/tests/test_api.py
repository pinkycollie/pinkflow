#!/usr/bin/env python3
"""
Tests for PinkFlow Backend API
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))

from backend.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "PinkFlow API"
        assert "version" in data

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "services" in data


class TestToolsEndpoints:
    """Test accessibility tools endpoints"""

    def test_list_tools(self, client):
        """Test listing all tools"""
        response = client.get("/api/tools")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_list_tools_by_category(self, client):
        """Test filtering tools by category"""
        response = client.get("/api/tools?category=model_testing")
        assert response.status_code == 200
        data = response.json()
        assert all(t["category"] == "model_testing" for t in data)

    def test_get_tool(self, client):
        """Test getting a specific tool"""
        response = client.get("/api/tools/model-testing")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "model-testing"
        assert data["name"] == "Model Testing"

    def test_get_nonexistent_tool(self, client):
        """Test getting a tool that doesn't exist"""
        response = client.get("/api/tools/nonexistent")
        assert response.status_code == 404


class TestModelTestingEndpoints:
    """Test model testing endpoints"""

    def test_test_model(self, client):
        """Test model testing endpoint"""
        response = client.post("/api/test/model", json={
            "repo_url": "https://github.com/example/test-model"
        })
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "status" in data
        assert "repo_url" in data
        assert data["repo_url"] == "https://github.com/example/test-model"

    def test_batch_test(self, client):
        """Test batch testing endpoint"""
        response = client.post("/api/test/batch", json={
            "repo_urls": [
                "https://github.com/example/model1",
                "https://github.com/example/model2"
            ]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert "passed" in data
        assert "failed" in data
        assert len(data["results"]) == 2


class TestCaptionEndpoints:
    """Test caption generation endpoints"""

    def test_generate_captions(self, client):
        """Test caption generation"""
        response = client.post("/api/captions/generate", json={
            "text": "Test caption content",
            "format": "srt"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["format"] == "srt"
        assert data["captions"] is not None


class TestTranscriptionEndpoints:
    """Test transcription endpoints"""

    def test_generate_transcription(self, client):
        """Test transcription generation"""
        response = client.post("/api/transcription/generate", json={
            "language": "en",
            "include_timestamps": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["text"] is not None


class TestStatisticsEndpoints:
    """Test statistics endpoints"""

    def test_get_statistics(self, client):
        """Test getting statistics"""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_models_tested" in data
        assert "total_tools" in data
        assert "available_tools" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
