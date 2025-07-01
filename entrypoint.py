#!/usr/bin/env python3
"""
Container Entrypoint for RaiderBot Email Pipeline
Executed inside Docker container by Foundry container transform
"""

import os
import sys
import json
import traceback
from datetime import datetime
import requests

# Add our modules to path
sys.path.append('/app/python-functions/python/python-functions')

def main():
    """
    Main entrypoint executed by Foundry container transform
    Runs the email pipeline and writes results to shared volume
    """
    print("🚀 RaiderBot Email Pipeline Container Starting...")
    print(f"⏰ Start time: {datetime.now().isoformat()}")
    
    try:
        # Import our pipeline functions
        from raiderbot_email_pipeline import (
            raiderbot_email_monitoring_pipeline,
            raiderbot_email_sentiment_analysis,
            raiderbot_email_response_generator
        )
        
        print("✅ Pipeline modules imported successfully")
        
        # Execute full pipeline
        print("📧 Starting email monitoring pipeline...")
        pipeline_result = raiderbot_email_monitoring_pipeline()
        
        if pipeline_result.get('status') != 'success':
            raise Exception(f"Email monitoring failed: {pipeline_result}")
        
        print(f"✅ Email monitoring completed: {len(pipeline_result.get('emails', []))} emails processed")
        
        # Execute sentiment analysis if emails were found
        emails = pipeline_result.get('emails', [])
        if emails:
            print("🧠 Starting sentiment analysis...")
            sentiment_result = raiderbot_email_sentiment_analysis(emails)
            pipeline_result['sentiment_analysis_container'] = sentiment_result
            print(f"✅ Sentiment analysis completed: {len(sentiment_result)} analyses")
            
            # Execute response generation if sentiment data exists
            sentiment_data = pipeline_result.get('sentiment_analysis', [])
            if sentiment_data:
                print("✍️ Starting response generation...")
                response_result = raiderbot_email_response_generator(sentiment_data)
                pipeline_result['response_generation_container'] = response_result
                print(f"✅ Response generation completed: {len(response_result)} responses")
        
        # Prepare final results
        final_result = {
            "status": "success",
            "message": "RaiderBot email pipeline executed successfully via container transform",
            "pipeline_result": pipeline_result,
            "execution_type": "foundry_container_transform",
            "timestamp": datetime.now().isoformat(),
            "container_user": os.getenv('USER', 'foundryuser'),
            "emails_processed": len(emails),
            "sentiment_analyses": len(pipeline_result.get('sentiment_analysis', [])),
            "responses_generated": len(pipeline_result.get('response_generation', []))
        }
        
        print(f"🎉 Pipeline execution completed successfully!")
        print(f"📊 Summary: {final_result['emails_processed']} emails, {final_result['sentiment_analyses']} analyses, {final_result['responses_generated']} responses")
        
    except Exception as e:
        print(f"❌ Pipeline execution failed: {str(e)}")
        print(f"📋 Full traceback:\n{traceback.format_exc()}")
        
        # Create error result
        final_result = {
            "status": "error",
            "message": f"Pipeline execution failed: {str(e)}",
            "error_details": traceback.format_exc(),
            "execution_type": "foundry_container_transform_error",
            "timestamp": datetime.now().isoformat(),
            "container_user": os.getenv('USER', 'foundryuser')
        }
    
    # Write results to shared volume for Foundry to read
    shared_path = "/shared"
    results_file = os.path.join(shared_path, "pipeline_results.json")
    
    try:
        # Ensure shared directory exists
        os.makedirs(shared_path, exist_ok=True)
        
        # Write results
        with open(results_file, 'w') as f:
            json.dump(final_result, f, indent=2, default=str)
        
        print(f"💾 Results written to: {results_file}")
        
        # Also write summary for easy debugging
        summary_file = os.path.join(shared_path, "pipeline_summary.txt")
        with open(summary_file, 'w') as f:
            f.write(f"RaiderBot Email Pipeline Container Execution Summary\n")
            f.write(f"=" * 50 + "\n")
            f.write(f"Status: {final_result['status']}\n")
            f.write(f"Timestamp: {final_result['timestamp']}\n")
            f.write(f"Execution Type: {final_result['execution_type']}\n")
            if final_result['status'] == 'success':
                f.write(f"Emails Processed: {final_result['emails_processed']}\n")
                f.write(f"Sentiment Analyses: {final_result['sentiment_analyses']}\n")
                f.write(f"Responses Generated: {final_result['responses_generated']}\n")
            else:
                f.write(f"Error: {final_result['message']}\n")
        
        print(f"📄 Summary written to: {summary_file}")
        
    except Exception as write_error:
        print(f"❌ Failed to write results to shared volume: {str(write_error)}")
        print(f"📋 Write error traceback:\n{traceback.format_exc()}")
        sys.exit(1)
    
    print(f"🏁 Container execution completed at: {datetime.now().isoformat()}")
    
    # Exit with appropriate code
    if final_result['status'] == 'success':
        print("✅ Exiting with success code")
        sys.exit(0)
    else:
        print("❌ Exiting with error code")
        sys.exit(1)


if __name__ == "__main__":
    main()
