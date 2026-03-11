"""
FastAPI service for Regression Manager Agent.
Provides REST API endpoints for regression optimization.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import logging
import tempfile
from pathlib import Path

from .regression_manager_agent import RegressionManagerAgent
from .config import config, RegressionConfig, ScoringWeights

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Regression Manager Agent API",
    description="Production-grade regression test optimization service",
    version="1.0.0"
)


class OptimizeRequest(BaseModel):
    """Request model for regression optimization."""
    csv_path: str = Field(..., description="Path to CSV testcase data")
    log_path: Optional[str] = Field(None, description="Optional path to simulation log")
    coverage_report_path: Optional[str] = Field(None, description="Optional path to coverage report")
    enable_load_optimizer: bool = Field(True, description="Enable resource load optimization")
    enable_llm_copilot: bool = Field(False, description="Enable LLM-powered insights")
    llm_api_key: Optional[str] = Field(None, description="API key for LLM provider")
    
    class Config:
        schema_extra = {
            "example": {
                "csv_path": "rag_training_data.csv",
                "log_path": "sim.log",
                "coverage_report_path": "coverage.rpt",
                "enable_load_optimizer": True,
                "enable_llm_copilot": False
            }
        }


class ConfigUpdateRequest(BaseModel):
    """Request model for configuration updates."""
    coverage_weight: Optional[float] = Field(None, ge=0, le=1)
    efficiency_weight: Optional[float] = Field(None, ge=0, le=1)
    stability_weight: Optional[float] = Field(None, ge=0, le=1)
    pass_rate_threshold: Optional[float] = Field(None, ge=0, le=1)
    coverage_gain_threshold: Optional[float] = Field(None, ge=0)
    critical_modules: Optional[List[str]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "coverage_weight": 0.4,
                "efficiency_weight": 0.3,
                "stability_weight": 0.3,
                "pass_rate_threshold": 0.95,
                "coverage_gain_threshold": 1.0,
                "critical_modules": ["cpu_core", "memory_controller"]
            }
        }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Regression Manager Agent API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/optimize-regression")
async def optimize_regression(request: OptimizeRequest) -> Dict:
    """
    Optimize regression test suite.
    
    Args:
        request: Optimization request with file paths
        
    Returns:
        Optimization results with ranked and excluded tests
    """
    try:
        logger.info(f"Received optimization request: {request.csv_path}")
        
        # Validate file paths
        csv_path = Path(request.csv_path)
        if not csv_path.exists():
            raise HTTPException(status_code=404, detail=f"CSV file not found: {request.csv_path}")
        
        if request.log_path:
            log_path = Path(request.log_path)
            if not log_path.exists():
                logger.warning(f"Log file not found: {request.log_path}, proceeding without log data")
                request.log_path = None
        
        # Run optimization
        agent = RegressionManagerAgent(
            csv_path=str(csv_path),
            log_path=request.log_path,
            coverage_report_path=request.coverage_report_path,
            enable_load_optimizer=request.enable_load_optimizer,
            enable_llm_copilot=request.enable_llm_copilot,
            llm_api_key=request.llm_api_key
        )
        
        result = agent.run()
        
        logger.info(f"Optimization complete: {result['summary']}")
        
        return result
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Optimization failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


@app.post("/upload-and-optimize")
async def upload_and_optimize(
    csv_file: UploadFile = File(...),
    log_file: Optional[UploadFile] = File(None)
) -> Dict:
    """
    Upload files and optimize regression.
    
    Args:
        csv_file: CSV file upload
        log_file: Optional log file upload
        
    Returns:
        Optimization results
    """
    try:
        # Save uploaded files to temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / csv_file.filename
            with open(csv_path, 'wb') as f:
                content = await csv_file.read()
                f.write(content)
            
            log_path = None
            if log_file:
                log_path = Path(tmpdir) / log_file.filename
                with open(log_path, 'wb') as f:
                    content = await log_file.read()
                    f.write(content)
            
            # Run optimization
            agent = RegressionManagerAgent(
                csv_path=str(csv_path),
                log_path=str(log_path) if log_path else None
            )
            
            result = agent.run()
            
            return result
            
    except Exception as e:
        logger.error(f"Upload and optimize failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config() -> Dict:
    """
    Get current configuration.
    
    Returns:
        Current configuration settings
    """
    return {
        "scoring_weights": {
            "coverage": config.scoring_weights.coverage,
            "efficiency": config.scoring_weights.efficiency,
            "stability": config.scoring_weights.stability
        },
        "redundancy_thresholds": {
            "pass_rate_threshold": config.redundancy_thresholds.pass_rate_threshold,
            "coverage_gain_threshold": config.redundancy_thresholds.coverage_gain_threshold,
            "no_failure_window": config.redundancy_thresholds.no_failure_window
        },
        "critical_modules": {
            "modules": config.critical_modules.modules,
            "critical_weight_multiplier": config.critical_modules.critical_weight_multiplier
        }
    }


@app.put("/config")
async def update_config(request: ConfigUpdateRequest) -> Dict:
    """
    Update configuration.
    
    Args:
        request: Configuration update request
        
    Returns:
        Updated configuration
    """
    try:
        # Update scoring weights
        if request.coverage_weight is not None:
            config.scoring_weights.coverage = request.coverage_weight
        if request.efficiency_weight is not None:
            config.scoring_weights.efficiency = request.efficiency_weight
        if request.stability_weight is not None:
            config.scoring_weights.stability = request.stability_weight
        
        # Validate weights sum
        total_weight = (
            config.scoring_weights.coverage +
            config.scoring_weights.efficiency +
            config.scoring_weights.stability
        )
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Scoring weights must sum to 1.0, got {total_weight}")
        
        # Update redundancy thresholds
        if request.pass_rate_threshold is not None:
            config.redundancy_thresholds.pass_rate_threshold = request.pass_rate_threshold
        if request.coverage_gain_threshold is not None:
            config.redundancy_thresholds.coverage_gain_threshold = request.coverage_gain_threshold
        
        # Update critical modules
        if request.critical_modules is not None:
            config.critical_modules.modules = request.critical_modules
        
        logger.info("Configuration updated successfully")
        
        return await get_config()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


class ChatRequest(BaseModel):
    """Request model for copilot chat."""
    message: str = Field(..., description="User message")
    context: Optional[Dict] = Field(None, description="Optional context")
    llm_api_key: Optional[str] = Field(None, description="API key for LLM")


class ResourceConfigRequest(BaseModel):
    """Request model for resource configuration."""
    cpu_units: int = Field(16, description="Number of CPU cores")
    gpu_units: int = Field(4, description="Number of GPUs")
    cloud_units: int = Field(100, description="Number of cloud instances")


@app.post("/copilot/chat")
async def copilot_chat(request: ChatRequest) -> Dict:
    """
    Chat with the regression testing copilot.
    
    Args:
        request: Chat request with message and context
        
    Returns:
        Copilot response
    """
    try:
        from .llm_copilot import RegressionCopilot
        
        copilot = RegressionCopilot(api_key=request.llm_api_key)
        response = copilot.chat(request.message, request.context)
        
        return {
            "response": response,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Copilot chat failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/copilot/explain-test")
async def explain_test(test_data: Dict, llm_api_key: Optional[str] = None) -> Dict:
    """
    Get explanation for a test's score.
    
    Args:
        test_data: Test information
        llm_api_key: Optional API key
        
    Returns:
        Explanation of test score
    """
    try:
        from .llm_copilot import RegressionCopilot
        
        copilot = RegressionCopilot(api_key=llm_api_key)
        explanation = copilot.explain_test_score(test_data)
        
        return {
            "explanation": explanation,
            "test_id": test_data.get('testcase_id', 'unknown')
        }
        
    except Exception as e:
        logger.error(f"Test explanation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resources/configure")
async def configure_resources(request: ResourceConfigRequest) -> Dict:
    """
    Configure available resources for load optimization.
    
    Args:
        request: Resource configuration
        
    Returns:
        Configuration confirmation
    """
    try:
        from .load_optimizer import LoadOptimizer
        
        optimizer = LoadOptimizer()
        optimizer.configure_resources(
            cpu_units=request.cpu_units,
            gpu_units=request.gpu_units,
            cloud_units=request.cloud_units
        )
        
        return {
            "status": "configured",
            "resources": {
                "cpu": request.cpu_units,
                "gpu": request.gpu_units,
                "cloud": request.cloud_units
            }
        }
        
    except Exception as e:
        logger.error(f"Resource configuration failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resources/usage")
async def get_resource_usage() -> Dict:
    """
    Get current resource usage statistics.
    
    Returns:
        Resource usage report
    """
    try:
        # This would typically query a database or monitoring system
        # For now, return example data
        return {
            "servers": [
                {
                    "server_id": "cpu_server_1",
                    "resource_type": "cpu",
                    "utilization": 75.5,
                    "tests_running": 8,
                    "status": "active"
                },
                {
                    "server_id": "gpu_server_1",
                    "resource_type": "gpu",
                    "utilization": 92.3,
                    "tests_running": 3,
                    "status": "active"
                }
            ],
            "summary": {
                "total_servers": 6,
                "active_servers": 5,
                "average_utilization": 68.4
            }
        }
        
    except Exception as e:
        logger.error(f"Resource usage query failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/coverage/parse")
async def parse_coverage(
    coverage_file: UploadFile = File(...),
    report_type: str = "auto"
) -> Dict:
    """
    Parse coverage report file.
    
    Args:
        coverage_file: Coverage report file
        report_type: Type of report (vcs, questa, xcelium, auto)
        
    Returns:
        Parsed coverage data
    """
    try:
        from .coverage_parser import CoverageParser
        
        # Save uploaded file
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / coverage_file.filename
            with open(file_path, 'wb') as f:
                content = await coverage_file.read()
                f.write(content)
            
            # Parse coverage
            parser = CoverageParser(str(file_path), report_type=report_type)
            coverage_data = parser.parse()
            
            return {
                "coverage": coverage_data,
                "report_type": parser.report_type,
                "filename": coverage_file.filename
            }
            
    except Exception as e:
        logger.error(f"Coverage parsing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
