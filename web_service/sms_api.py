import requests

from story_books_server.settings import SMS_API_USERNAME, SMS_API_PASSWORD


def send_sms(phone, text):
    sms_url = 'http://37.130.202.188/api/select'
    data = {
        "op": "send",
        "uname": SMS_API_USERNAME,
        "pass": SMS_API_PASSWORD,
        "message": text,
        "from": "100009",
        "to": [phone],
    }
    response = requests.post(sms_url, json=data)
    return response.json()


if __name__ == '__main__':
    print(send_sms('09134231834', 'تست پیامک'))
