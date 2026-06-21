import requests
import os
import time
from datetime import datetime

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

TARGET_CLASS = '수영06시(월수금)'

API_URL = 'https://www.ijongno.co.kr/rest/lecture/list'
PAGE_URL = 'https://www.ijongno.co.kr/fmcs/3?page=1&lecture_type=R&center=JONGNO02&event=1000000000&class=1000010000'

TOTAL_CHECKS = 55
CHECK_INTERVAL = 60

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': message}, timeout=10)


def check():
    response = requests.post(
        API_URL,
        data={
            'company_code': 'JONGNO02',
            'mem_no': '',
            'search_type': '%',
            'category_cd': '1000010000',
            'category_level': 2,
            'class_nm': '',
            'train_day': '',
            'adult_gubn': '',
            'lecturer_nm': '',
            'page': 1,
            'page_size': 50,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

send_telegram("워크플로우 시작")

for i in range(1, TOTAL_CHECKS + 1):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] 조회 {i}/{TOTAL_CHECKS}")

    try:
        lectures = check()
        found = False
        for lecture in lectures:
            if lecture.get('class_nm') == TARGET_CLASS:
                found = True
                status = lecture.get('status')
                print(f"[{now}] {TARGET_CLASS} | 상태: {status}")

                if status == 'R':
                    msg = (
                        f"[종로구민회관 수강신청 알림]\n"
                        f"{TARGET_CLASS} 접수 시작!\n"
                        f"지금 바로 신청하세요!\n\n"
                        f"{PAGE_URL}"
                    )
                    send_telegram(msg)
                    print(f"[{now}] 텔레그램 알림 발송 완료")
                break

        if not found:
            print(f"[{now}] 강좌 '{TARGET_CLASS}' 정보를 찾지 못했습니다.")

    except Exception as e:
        print(f"[{now}] 오류 발생: {e}")

    if i < TOTAL_CHECKS:
        time.sleep(CHECK_INTERVAL)

print("55회 조회 완료. 종료합니다.")
