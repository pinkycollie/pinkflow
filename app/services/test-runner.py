import docker
import asyncio
from datetime import datetime
from app.services.firebase import firebase_service
from app.middleware.fibronrose import log_to_fibronrose
from app.config import settings

class TestRunner:
    def __init__(self):
        self.docker_client = docker.from_env()
    
    async def start_test(self, model_id: str, options: dict) -> str:
        """Start model testing pipeline"""
        test_id = f"test_{int(datetime.utcnow().timestamp())}_{model_id[:8]}"
        
        # Create test record
        test_data = {
            "test_id": test_id,
            "model_id": model_id,
            "status": "queued",
            "dataset": options.get("dataset", "WLASL"),
            "compute_type": options.get("compute_type", "cuda"),
            "progress": 0,
            "current_stage": "setup",
            "created_at": datetime.utcnow(),
            "logs": []
        }
        
        firebase_service.create_test(test_data)
        
        # Trigger async execution
        asyncio.create_task(self._run_test(test_id, model_id, options))
        
        return test_id
    
    async def _run_test(self, test_id: str, model_id: str, options: dict):
        """Execute test in Docker container"""
        try:
            # Update status
            firebase_service.update_test(test_id, {
                "status": "running",
                "current_stage": "setup"
            })
            
            # Get model info
            model = firebase_service.get_model(model_id)
            
            # Run Docker container for testing
            container = self.docker_client.containers.run(
                "mbtq/pinkflow-tester:latest",
                environment={
                    "MODEL_REPO": model["repo"],
                    "DATASET": options["dataset"],
                    "COMPUTE_TYPE": options["compute_type"]
                },
                device_requests=[
                    docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])
                ] if settings.TEST_GPU_ENABLED else None,
                detach=True,
                remove=True
            )
            
            # Monitor progress
            for log in container.logs(stream=True):
                # Parse log and update progress
                firebase_service.update_test(test_id, {
                    "logs": firestore.ArrayUnion([{
                        "timestamp": datetime.utcnow(),
                        "message": log.decode("utf-8")
                    }])
                })
            
            # Test completed - parse results
            results = self._parse_test_results(container)
            
            # Update model with results
            firebase_service.update_model(model_id, {
                "status": "tested",
                "accuracy": results["accuracy"],
                "fps": results["fps"],
                "deaf_score": results["deaf_score"],
                "tested_at": datetime.utcnow()
            })
            
            # Update test status
            firebase_service.update_test(test_id, {
                "status": "completed",
                "progress": 100,
                "results": results
            })
            
            # Log to Fibronrose
            await log_to_fibronrose("test_completed", {
                "test_id": test_id,
                "model_id": model_id,
                "results": results
            })
        
        except Exception as e:
            firebase_service.update_test(test_id, {
                "status": "failed",
                "error": str(e)
            })
            
            firebase_service.update_model(model_id, {
                "status": "failed"
            })
    
    def _parse_test_results(self, container) -> dict:
        """Parse test results from container output"""
        # This would parse actual test output
        # For now, returning mock data
        return {
            "accuracy": 92.5,
            "fps": 45.0,
            "deaf_score": 95.0,
            "precision": 91.2,
            "recall": 93.8
        }

test_runner = TestRunner()
