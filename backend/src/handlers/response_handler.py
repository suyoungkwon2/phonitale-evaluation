import json
import boto3
from datetime import datetime
from typing import Dict, Any

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserResponses')

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Parse the event data
        user_name = event['user_name']
        phone_number = event['phone_number']
        english_word = event['english_word']
        round_number = event['round_number']
        page_type = event['page_type']
        duration = event['duration']
        response = event.get('response', 'N/A')
        
        # Create keys
        partition_key = f"{user_name}#{phone_number}"
        sort_key = english_word
        
        # Get current timestamp
        current_timestamp = datetime.now().isoformat()
        
        # Prepare update expression and attribute values
        update_expression = []
        expression_attribute_values = {}
        
        # Add timestamp for the specific page type
        timestamp_key = f"timestamp-{page_type}"
        update_expression.append(f"{timestamp_key} = :{timestamp_key}")
        expression_attribute_values[f":{timestamp_key}"] = current_timestamp
        
        # Add duration for the specific page type
        duration_key = f"duration-{page_type}"
        update_expression.append(f"{duration_key} = :{duration_key}")
        expression_attribute_values[f":{duration_key}"] = duration
        
        # Add response if it's recognition or generation
        if page_type in ['recognition', 'generation']:
            response_key = f"response-{page_type}"
            update_expression.append(f"{response_key} = :{response_key}")
            expression_attribute_values[f":{response_key}"] = response
        
        # Add survey response if it's survey
        if page_type == 'survey':
            update_expression.append("survey = :survey")
            expression_attribute_values[":survey"] = response
        
        # Update or create item in DynamoDB
        table.update_item(
            Key={
                'PK': partition_key,
                'SK': sort_key
            },
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_attribute_values
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Response recorded successfully',
                'user_name': user_name,
                'phone_number': phone_number,
                'english_word': english_word,
                'round_number': round_number,
                'page_type': page_type,
                'timestamp': current_timestamp,
                'duration': duration,
                'response': response
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 