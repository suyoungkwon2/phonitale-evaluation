import json
import requests
import time
import random
from decimal import Decimal
from datetime import datetime, timezone, timedelta

# 테스트 설정
LAMBDA_URL = "https://2ml24s4a3jfj5hqx4y644cgzbq0jbzmt.lambda-url.us-east-2.on.aws/"
USER_NAME = "권수영"
PHONE_NUMBER = "8884329342"

# 테스트 단어 목록 (12개)
WORDS = [
    {"english": "apple", "korean": "사과"},
    {"english": "bear", "korean": "곰"},
    {"english": "carrot", "korean": "당근"},
    {"english": "dog", "korean": "개"},
    {"english": "elephant", "korean": "코끼리"},
    {"english": "flower", "korean": "꽃"},
    {"english": "giraffe", "korean": "기린"},
    {"english": "house", "korean": "집"},
    {"english": "ice cream", "korean": "아이스크림"},
    {"english": "jacket", "korean": "재킷"},
    {"english": "king", "korean": "왕"},
    {"english": "lion", "korean": "사자"}
]

def get_random_duration(phase):
    """실제 상황과 유사한 소요 시간 생성"""
    if phase == "learning":
        return random.uniform(10, 20)  # 학습 시간: 10-20초
    elif phase == "recognition":
        return random.uniform(3, 8)    # 인식 시간: 3-8초
    elif phase == "generation":
        return random.uniform(5, 12)   # 생성 시간: 5-12초
    return 0

def create_test_data(round_number, page_type, words):
    """각 단계별 테스트 데이터 생성"""
    test_data = []
    
    for word in words:
        duration = get_random_duration(page_type)
        response_data = {
            "user_name": USER_NAME,
            "phone_number": PHONE_NUMBER,
            "english_word": word["english"],
            "round_number": round_number,
            "page_type": page_type,
            "duration": str(Decimal(str(duration))),
            "response": word["korean"] if page_type == "recognition" else word["english"] if page_type == "generation" else ""
        }
        test_data.append(response_data)
    
    return test_data

def create_survey_data(all_words_data):
    """설문 데이터 생성"""
    survey_data = []
    for word_data in all_words_data:
        survey_response = {
            "user_name": USER_NAME,
            "phone_number": PHONE_NUMBER,
            "english_word": word_data["english"],
            "round_number": word_data["round"],
            "page_type": "survey",
            "duration": str(Decimal('5.0')),
            "response": random.randint(3, 5)  # 3-5점 사이의 랜덤 점수
        }
        survey_data.append(survey_response)
    return survey_data

def run_test():
    all_words_data = []  # 설문을 위한 모든 단어 데이터 저장
    
    print("\n=== 실험 시작 ===")
    start_time = datetime.now()
    
    for round_num in range(1, 4):  # 3라운드
        print(f"\n=== Round {round_num} ===")
        
        # Learning phase
        print("\nLearning phase:")
        random.shuffle(WORDS)  # 단어 순서 랜덤화
        learning_data = create_test_data(round_num, "learning", WORDS)
        for data in learning_data:
            response = requests.post(LAMBDA_URL, json=data)
            print(f"Learning response for {data['english_word']}: {response.status_code}")
            time.sleep(0.5)  # API 호출 간 간격
            all_words_data.append({"english": data["english_word"], "round": round_num})
        
        # Recognition phase
        print("\nRecognition phase:")
        random.shuffle(WORDS)  # 단어 순서 다시 랜덤화
        recognition_data = create_test_data(round_num, "recognition", WORDS)
        for data in recognition_data:
            response = requests.post(LAMBDA_URL, json=data)
            print(f"Recognition response for {data['english_word']}: {response.status_code}")
            time.sleep(0.5)
        
        # Generation phase
        print("\nGeneration phase:")
        random.shuffle(WORDS)  # 단어 순서 다시 랜덤화
        generation_data = create_test_data(round_num, "generation", WORDS)
        for data in generation_data:
            response = requests.post(LAMBDA_URL, json=data)
            print(f"Generation response for {data['english_word']}: {response.status_code}")
            time.sleep(0.5)
        
        print(f"\nRound {round_num} 완료")
        time.sleep(2)  # 라운드 간 간격
    
    # Final Survey
    print("\n=== Final Survey ===")
    survey_data = create_survey_data(all_words_data)
    for data in survey_data:
        response = requests.post(LAMBDA_URL, json=data)
        print(f"Survey response for {data['english_word']} (Round {data['round_number']}): {response.status_code}")
        time.sleep(0.5)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n=== 실험 종료 ===")
    print(f"총 소요 시간: {duration}")

if __name__ == "__main__":
    run_test() 