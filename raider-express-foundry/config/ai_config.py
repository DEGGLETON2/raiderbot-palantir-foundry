"""
AI Configuration for Raider Express
Configuration for AI services, chat bot, and ML models
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class AIConfig:
    """AI and ML configuration"""
    
    # OpenAI/LLM settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2000
    
    # Azure OpenAI settings (alternative)
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_key: str = os.getenv("AZURE_OPENAI_KEY", "")
    azure_deployment_name: str = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")
    
    # Embedding settings
    embedding_model: str = "text-embedding-ada-002"
    embedding_dimension: int = 1536
    
    # Vector database settings
    vector_db_type: str = os.getenv("VECTOR_DB_TYPE", "pinecone")  # pinecone, weaviate, etc.
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
    pinecone_index_name: str = "raider-express-knowledge"
    
    # Chat configuration
    chat_system_prompt: str = """
    You are RaiderBot, an AI assistant for Raider Express Transportation.
    You help with fleet management, logistics, safety analysis, and operational insights.
    You have access to real-time fleet data, driver performance metrics, and route analytics.
    Always provide accurate, actionable information to help improve operations and safety.
    """
    
    chat_max_history: int = 10
    chat_timeout: int = 30
    
    # Document processing
    document_chunk_size: int = 1000
    document_chunk_overlap: int = 200
    supported_file_types: List[str] = [".pdf", ".docx", ".txt", ".csv", ".xlsx"]
    max_file_size_mb: int = 50
    
    # ML model settings
    model_registry_path: str = "/raider-express/ml-models"
    model_serving_timeout: int = 30
    batch_prediction_size: int = 1000
    
    # Safety scoring model
    safety_model_name: str = "driver-safety-scoring-v1"
    safety_model_threshold: float = 0.7
    
    # Route optimization model
    route_optimization_model: str = "route-optimizer-v2"
    route_optimization_timeout: int = 60
    
    # Maintenance prediction model
    maintenance_model_name: str = "predictive-maintenance-v1"
    maintenance_prediction_horizon_days: int = 30

@dataclass
class RaiderBotConfig:
    """RaiderBot-specific configuration"""
    
    # Bot identity
    bot_name: str = "RaiderBot"
    bot_version: str = "1.0.0"
    
    # Capabilities
    can_analyze_documents: bool = True
    can_process_images: bool = True
    can_analyze_video: bool = True
    can_generate_reports: bool = True
    
    # Response settings
    max_response_length: int = 2000
    include_data_sources: bool = True
    include_confidence_scores: bool = True
    
    # Knowledge base
    knowledge_base_paths: List[str] = [
        "/raider-express/documents/policies",
        "/raider-express/documents/procedures", 
        "/raider-express/documents/training",
        "/raider-express/documents/compliance"
    ]
    
    # Quick actions
    quick_actions: List[Dict[str, str]] = [
        {"name": "Fleet Status", "query": "What's the current status of our fleet?"},
        {"name": "Safety Summary", "query": "Show me today's safety metrics and incidents"},
        {"name": "Route Performance", "query": "How are our routes performing this week?"},
        {"name": "Driver Leaderboard", "query": "Show me the top performing drivers this month"},
        {"name": "Maintenance Alerts", "query": "What vehicles need maintenance soon?"}
    ]

@dataclass
class MLModelConfig:
    """Machine learning model configuration"""
    
    # Model training settings
    training_data_window_days: int = 365
    model_retrain_frequency_days: int = 30
    validation_split: float = 0.2
    test_split: float = 0.1
    
    # Feature engineering
    feature_selection_method: str = "recursive_feature_elimination"
    max_features: int = 100
    feature_importance_threshold: float = 0.01
    
    # Model types for different use cases
    safety_scoring_algorithm: str = "xgboost"
    route_optimization_algorithm: str = "genetic_algorithm"
    maintenance_prediction_algorithm: str = "random_forest"
    demand_forecasting_algorithm: str = "prophet"
    
    # Hyperparameter tuning
    hyperparameter_tuning_method: str = "bayesian_optimization"
    max_tuning_iterations: int = 100
    tuning_timeout_hours: int = 6
    
    # Model evaluation
    primary_metric: str = "f1_score"  # for classification tasks
    regression_metric: str = "rmse"   # for regression tasks
    acceptable_performance_threshold: float = 0.85

def get_ai_config() -> AIConfig:
    """Get AI configuration"""
    return AIConfig()

def get_raiderbot_config() -> RaiderBotConfig:
    """Get RaiderBot configuration"""
    return RaiderBotConfig()

def get_ml_model_config() -> MLModelConfig:
    """Get ML model configuration"""
    return MLModelConfig()

def get_prompt_templates() -> Dict[str, str]:
    """Get prompt templates for different AI tasks"""
    return {
        "safety_analysis": """
        Analyze the following safety data for Raider Express:
        {data}
        
        Please provide:
        1. Key safety concerns and trends
        2. Recommended actions
        3. Risk assessment
        4. Priority level (High/Medium/Low)
        """,
        
        "route_optimization": """
        Given the following route and traffic data:
        {route_data}
        
        Suggest optimizations for:
        1. Delivery sequence
        2. Time windows
        3. Fuel efficiency
        4. Driver workload balance
        """,
        
        "maintenance_prediction": """
        Based on the vehicle data:
        {vehicle_data}
        
        Predict:
        1. Likelihood of maintenance needs in next 30 days
        2. Specific components at risk
        3. Recommended maintenance schedule
        4. Cost estimates
        """,
        
        "driver_coaching": """
        Review driver performance data:
        {performance_data}
        
        Provide coaching recommendations for:
        1. Safety improvements
        2. Efficiency gains
        3. Training opportunities
        4. Recognition areas
        """
    }

# Global configuration instances
AI_CONFIG = get_ai_config()
RAIDERBOT_CONFIG = get_raiderbot_config()
ML_MODEL_CONFIG = get_ml_model_config()
PROMPT_TEMPLATES = get_prompt_templates()