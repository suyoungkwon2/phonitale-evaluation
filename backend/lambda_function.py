import json
import boto3
import time
from datetime import datetime, timezone

def lambda_handler(event, context):
    # DynamoDB 클라이언트 초기화
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('phonitale-responses')
    
    # 현재 시간을 ISO 형식으로 변환
    current_time = datetime.now(timezone.utc).isoformat()
    
    # 요청 데이터 파싱
    try:
        body = json.loads(event['body'])
        user = body.get('user', '')
        words = body.get('words', [])
        page_type = body.get('page_type', '')
        round_number = body.get('round_number', 1)
        
        # 응답 데이터 구조 생성
        response_data = {
            "user": user,
            "words": []
        }
        
        # 각 단어에 대한 응답 처리
        for word_data in words:
            english_word = word_data.get('english_word', '')
            duration = word_data.get('duration', 0)
            response = word_data.get('response', {})
            
            # 단어별 응답 데이터 생성
            word_response = {
                "english_word": english_word,
                "Attributes": {
                    "round_number": round_number,
                    "timestamp-start": current_time,
                    "timestamp-learning": current_time if page_type == "learning" else "",
                    "timestamp-recognition": current_time if page_type == "recognition" else "",
                    "timestamp-generation": current_time if page_type == "generation" else "",
                    "timestamp-survey": current_time if page_type == "survey" else "",
                    "timestamp-end": current_time if page_type == "survey" else "",
                    "duration-learning": duration if page_type == "learning" else 0,
                    "duration-recognition": duration if page_type == "recognition" else 0,
                    "duration-generation": duration if page_type == "generation" else 0,
                    "duration-all": duration * 3 if page_type == "survey" else 0,
                    "response-recognition": response.get('recognition', ''),
                    "response-generation": response.get('generation', ''),
                    "survey": response.get('survey', 0)
                }
            }
            
            response_data["words"].append(word_response)
            
            # DynamoDB에 데이터 저장
            table.put_item(
                Item={
                    'user': user,
                    'timestamp': current_time,
                    'word': english_word,
                    'round_number': round_number,
                    'page_type': page_type,
                    'duration': duration,
                    'response_recognition': response.get('recognition', ''),
                    'response_generation': response.get('generation', ''),
                    'survey': response.get('survey', 0)
                }
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_data, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        } 