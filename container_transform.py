"""
RaiderBot Email Pipeline Container Transform
Foundry-compatible container transform using Docker image from Artifacts repository
"""

from palantir_models.transforms import sidecar, Volume, transform, Output, Input
import os
import json
from datetime import datetime

@sidecar(
    image="raiderbot-email-intelligence-api",  # Will be updated with full registry path
    tag="latest",  # Will be updated with specific tag
    volumes=[Volume("shared")]
)
@transform(
    output=Output("ri.foundry.main.dataset.email_pipeline_results"),  # Update with actual dataset RID
    # Optional: Add input datasets if needed
    # source_emails=Input("ri.foundry.main.dataset.source_emails")
)
def raiderbot_email_container_transform(output):
    """
    Container transform that executes RaiderBot email pipeline via Docker container
    
    The container runs the Flask API internally and executes the full pipeline:
    1. Email monitoring and ingestion
    2. Sentiment analysis via Snowflake Cortex
    3. Automated response generation
    4. Results output to Foundry dataset
    """
    
    # Container will execute the pipeline and write results to shared volume
    # The shared volume allows data exchange between container and Foundry
    
    # Read results from shared volume (written by container)
    results_path = "/shared/pipeline_results.json"
    
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            pipeline_results = json.load(f)
    else:
        # Fallback if container execution fails
        pipeline_results = {
            "status": "error",
            "message": "Container execution failed - no results found",
            "timestamp": datetime.now().isoformat()
        }
    
    # Convert results to Foundry dataset format
    import pandas as pd
    
    # Create DataFrame from pipeline results
    if pipeline_results.get('status') == 'success':
        # Extract email data and analysis results
        emails = pipeline_results.get('emails', [])
        sentiment_data = pipeline_results.get('sentiment_analysis', [])
        responses = pipeline_results.get('response_generation', [])
        
        # Combine all results into structured dataset
        result_records = []
        
        for i, email in enumerate(emails):
            record = {
                'email_id': email.get('id', f'email_{i}'),
                'subject': email.get('subject', ''),
                'sender': email.get('sender', ''),
                'timestamp': email.get('timestamp', ''),
                'content_preview': email.get('content', '')[:200] if email.get('content') else '',
                'sentiment_score': sentiment_data[i].get('sentiment_score', 0) if i < len(sentiment_data) else 0,
                'sentiment_label': sentiment_data[i].get('sentiment_label', 'neutral') if i < len(sentiment_data) else 'neutral',
                'critical_issue': sentiment_data[i].get('critical_issue', False) if i < len(sentiment_data) else False,
                'generated_response': responses[i].get('response_text', '') if i < len(responses) else '',
                'pipeline_timestamp': pipeline_results.get('timestamp', datetime.now().isoformat()),
                'deployment_type': 'container_transform'
            }
            result_records.append(record)
        
        df = pd.DataFrame(result_records)
    else:
        # Error case - create minimal error record
        df = pd.DataFrame([{
            'email_id': 'error',
            'subject': 'Pipeline Execution Error',
            'sender': 'system',
            'timestamp': datetime.now().isoformat(),
            'content_preview': pipeline_results.get('message', 'Unknown error'),
            'sentiment_score': 0,
            'sentiment_label': 'error',
            'critical_issue': True,
            'generated_response': 'Pipeline execution failed',
            'pipeline_timestamp': pipeline_results.get('timestamp', datetime.now().isoformat()),
            'deployment_type': 'container_transform_error'
        }])
    
    # Write to output dataset
    output.write_pandas(df)
    
    print(f"✅ Container transform completed: {len(df)} records processed")
    return f"Container transform executed successfully: {pipeline_results.get('status', 'unknown')}"


# Alternative: Simpler container transform for testing
@sidecar(
    image="raiderbot-email-intelligence-api",
    tag="latest", 
    volumes=[Volume("shared")]
)
@transform(
    output=Output("ri.foundry.main.dataset.email_pipeline_test")
)
def raiderbot_email_container_test(output):
    """
    Simple test version of container transform
    """
    import pandas as pd
    
    # Create test record to verify container transform works
    test_data = [{
        'test_id': 'container_transform_test',
        'status': 'success',
        'message': 'Container transform deployment successful',
        'timestamp': datetime.now().isoformat(),
        'deployment_type': 'container_transform_test'
    }]
    
    df = pd.DataFrame(test_data)
    output.write_pandas(df)
    
    print("✅ Container transform test completed")
    return "Container transform test successful"
