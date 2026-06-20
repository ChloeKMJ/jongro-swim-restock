import requests
import os
import sys

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

TARGET_CLASS = '수영06시(월수금)'

API_URL = 'https://www.ijongno.co.kr/rest/lecture/list'
PAGE_URL = 'https://www.ijongno.co.kr/fmcs/3?page=1&lecture_type=R&center=JONGNO02&event=1000000000&class=1000010000'


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


lectures = check()

for lecture in lectures:
    if lecture.get('class_nm') == TARGET_CLASS:
        status = lecture.get('status')
        print(f"강좌: {TARGET_CLASS} | 상태: {status}")

        if status == 'R':
            msg = (
                f"[종로구민회관 수강신청 알림]\n"
                f"{TARGET_CLASS} 접수 시작!\n"
                f"지금 바로 신청하세요!\n\n"
                f"{PAGE_URL}"
            )
            send_telegram(msg)
            print("텔레그램 알림 발송 완료")
        else:
            print("아직 접수종료 상태입니다.")
        sys.exit(0)

print(f"강좌 '{TARGET_CLASS}' 정보를 찾지 못했습니다.")
