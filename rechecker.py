import requests, time


url = 'http://localhost:8000/admin/ParsKCPT'

while True:
    # Отправка POST-запроса
    requests.post(url)
    time.sleep(86400)