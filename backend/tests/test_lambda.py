import json
import requests
import unittest
from datetime import datetime

class TestLambdaFunction(unittest.TestCase):
    LAMBDA_URL = "https://2ml24s4a3jfj5hqx4y644cgzbq0jbzmt.lambda-url.us-east-2.on.aws/"
    
    def test_successful_response(self):
        # 테스트 데이터 준비
        test_data = {
            "user_name": "권수영2",
            "phone_number": "84394892", # Use a valid phone number for success test
            "english_word": "test",
            "round_number": 1,
            "page_type": "recognition",
            "duration": 10,
            "response": "테스트"
        }
        
        # API 요청 보내기
        response = requests.post(
            self.LAMBDA_URL,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 응답 확인 (HTTP 상태 코드)
        self.assertEqual(response.status_code, 200)
        
        # 응답 데이터 확인 (Lambda 함수의 body 내용을 직접 확인)
        try:
            response_data = response.json()
            # Assuming response_data is the parsed content of the Lambda's body
            self.assertEqual(response_data["message"], 'Response recorded successfully')
            self.assertEqual(response_data["user_name"], test_data["user_name"])
            self.assertEqual(response_data["phone_number"], test_data["phone_number"])
            self.assertEqual(response_data["english_word"], test_data["english_word"])
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")
        except KeyError as e:
             self.fail(f"Expected key not found in response body: {e}")

    def test_missing_required_fields(self):
        # 필수 필드가 누락된 테스트 데이터
        test_data = {
            "user_name": "테스트사용자",
            "phone_number": "01012345678"
            # 'english_word', 'round_number', etc. are missing
        }
        
        # API 요청 보내기
        response = requests.post(
            self.LAMBDA_URL,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        # 에러 응답 확인 (Lambda 함수 내부 오류 시 500 반환 예상)
        self.assertEqual(response.status_code, 500)
        try:
            response_data = response.json()
            # Check if the error message is in the response body
            self.assertIn("error", response_data)
        except json.JSONDecodeError:
            self.fail("Error response is not valid JSON")

    def test_multiple_rounds(self):
        # Round 1
        for page_type in ['learning', 'recognition', 'generation']:
            for i in range(3):
                test_data = {
                    "user_name": "권수영2",
                    "phone_number": "test1212",
                    "english_word": f"word_{i+1}",
                    "round_number": 1,
                    "page_type": page_type,
                    "duration": 10,
                    "response": "테스트" if page_type != 'learning' else 'N/A' # Provide response only when relevant
                }
                response = requests.post(
                    self.LAMBDA_URL,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                self.assertEqual(response.status_code, 200)
                # Optional: Add checks for response body content if needed

        # Round 2
        for page_type in ['learning', 'recognition', 'generation']:
            for i in range(3): # Using the same words for simplicity, adjust if needed
                test_data = {
                    "user_name": "권수영2",
                    "phone_number": "test1212",
                    "english_word": f"word_{i+1}",
                    "round_number": 2,
                    "page_type": page_type,
                    "duration": 10,
                    "response": "테스트" if page_type != 'learning' else 'N/A'
                }
                response = requests.post(
                    self.LAMBDA_URL,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                self.assertEqual(response.status_code, 200)

        # Round 3
        for page_type in ['learning', 'recognition', 'generation']:
            for i in range(3):
                test_data = {
                    "user_name": "권수영2",
                    "phone_number": "test1212",
                    "english_word": f"word_{i+1}",
                    "round_number": 3,
                    "page_type": page_type,
                    "duration": 10,
                    "response": "테스트" if page_type != 'learning' else 'N/A'
                }
                response = requests.post(
                    self.LAMBDA_URL,
                    json=test_data,
                    headers={"Content-Type": "application/json"}
                )
                self.assertEqual(response.status_code, 200)

        # Survey
        # Assuming words 1-3 were used across rounds. Surveying 3 words.
        # The original test surveyed 9 words (range(9)), which seems inconsistent
        # with learning 3 words per round. Adjusting to survey words 1-3.
        for i in range(3):
            test_data = {
                "user_name": "권수영2",
                "phone_number": "test1212",
                "english_word": f"word_{i+1}",
                "round_number": 3, # Survey might happen after round 3
                "page_type": "survey",
                "duration": 10,
                "response": 5 # Survey response is likely a rating (e.g., 1-5)
            }
            response = requests.post(
                self.LAMBDA_URL,
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 