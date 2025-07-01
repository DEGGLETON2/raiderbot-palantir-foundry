#!/usr/bin/env python3
"""
RaiderBot Email Intelligence API Server
Containerized Flask deployment bypassing broken Foundry function registration
"""

from flask import Flask, request, jsonify
import logging
import sys
import os
from datetime import datetime

# Import our pipeline functions
sys.path.append('/app/python-functions/python/python-functions')
from raiderbot_email_pipeline import (
    raiderbot_email_monitoring_pipeline,
    raiderbot_email_sentiment_analysis, 
    raiderbot_email_response_generator
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "RaiderBot Email Intelligence API",
        "timestamp": datetime.now().isoformat(),
        "deployment": "containerized_bypass"
    })

@app.route('/api/email-monitoring', methods=['POST'])
def email_monitoring_pipeline():
    """
    Main email monitoring pipeline endpoint
    Replaces: raiderbot_email_monitoring_pipeline function
    """
    try:
        logger.info("🚀 Starting email monitoring pipeline via containerized API")
        
        # Get optional parameters from request
        data = request.get_json() if request.is_json else {}
        hours_back = data.get('hours_back', 24)
        
        # Execute the pipeline
        result = raiderbot_email_monitoring_pipeline()
        
        logger.info("✅ Email monitoring pipeline completed successfully")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Pipeline execution failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error_message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/sentiment-analysis', methods=['POST'])
def sentiment_analysis():
    """
    Email sentiment analysis endpoint
    Replaces: raiderbot_email_sentiment_analysis function
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        email_data = data.get('email_data', [])
        
        if not email_data:
            return jsonify({"error": "email_data is required"}), 400
        
        logger.info(f"🧠 Processing sentiment analysis for {len(email_data)} emails")
        
        result = raiderbot_email_sentiment_analysis(email_data)
        
        logger.info("✅ Sentiment analysis completed")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Sentiment analysis failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error_message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/response-generation', methods=['POST'])
def response_generation():
    """
    Automated response generation endpoint
    Replaces: raiderbot_email_response_generator function
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        sentiment_data = data.get('sentiment_data', [])
        
        if not sentiment_data:
            return jsonify({"error": "sentiment_data is required"}), 400
        
        logger.info(f"✍️ Generating responses for {len(sentiment_data)} analyzed emails")
        
        result = raiderbot_email_response_generator(sentiment_data)
        
        logger.info("✅ Response generation completed")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Response generation failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error_message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/full-pipeline', methods=['POST'])
def full_pipeline():
    """
    Complete end-to-end pipeline execution
    Combines all three functions into single endpoint
    """
    try:
        logger.info("🚀 Starting full end-to-end email intelligence pipeline")
        
        # Get optional parameters
        data = request.get_json() if request.is_json else {}
        hours_back = data.get('hours_back', 24)
        
        # Step 1: Email monitoring
        pipeline_result = raiderbot_email_monitoring_pipeline()
        
        if pipeline_result.get('status') != 'success':
            return jsonify(pipeline_result), 500
        
        # Step 2: Sentiment analysis (on fetched emails)
        emails = pipeline_result.get('emails', [])
        if emails:
            sentiment_result = raiderbot_email_sentiment_analysis(emails)
            pipeline_result['sentiment_analysis_api'] = sentiment_result
        
        # Step 3: Response generation (on sentiment data)
        sentiment_data = pipeline_result.get('sentiment_analysis', [])
        if sentiment_data:
            response_result = raiderbot_email_response_generator(sentiment_data)
            pipeline_result['response_generation_api'] = response_result
        
        logger.info("✅ Full pipeline execution completed successfully")
        
        return jsonify({
            "status": "success",
            "message": "Full email intelligence pipeline completed via containerized API",
            "pipeline_result": pipeline_result,
            "timestamp": datetime.now().isoformat(),
            "deployment_type": "containerized_bypass"
        })
        
    except Exception as e:
        logger.error(f"❌ Full pipeline execution failed: {str(e)}")
        return jsonify({
            "status": "error",
            "error_message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/', methods=['GET'])
def index():
    """
    API documentation endpoint
    """
    return jsonify({
        "service": "RaiderBot Email Intelligence API",
        "description": "Containerized deployment bypassing broken Foundry function registration",
        "deployment_type": "containerized_bypass",
        "endpoints": {
            "/health": "GET - Health check",
            "/api/email-monitoring": "POST - Email monitoring pipeline",
            "/api/sentiment-analysis": "POST - Email sentiment analysis", 
            "/api/response-generation": "POST - Automated response generation",
            "/api/full-pipeline": "POST - Complete end-to-end pipeline"
        },
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Starting RaiderBot Email Intelligence API on port {port}")
    logger.info("🐳 Containerized deployment - bypassing broken Foundry function registration")
    app.run(host='0.0.0.0', port=port, debug=False)
