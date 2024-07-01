import time

import requests

# Указать свой access_token
access_token = '****'
headers = {
    'Authorization': f'Bearer {access_token}',
    'HH-User-Agent': 'myapp'
}

# Получение списка резюме
resume_list_response = requests.get('https://api.hh.ru/resumes/mine', headers=headers)
resume_list = resume_list_response.json().get('items', [])

if not resume_list:
    print("Резюме не найдено.Не правильно указан номер.")
else:
    # Печать списка резюме
    print("Resume List:", resume_list)

    # Использование первого резюме из списка
    resume_id = resume_list[0]['id']
    print("Using Resume ID:", resume_id)




search_row = 'python'
search_row = f'NAME:("python" OR "python программист" NOT "senior ")'
params = {
    'text': search_row,  # поисковый запрос
    'area': 113,  # регион поиска - Россия
    'period': 3000,  # период в днях, за который появились вакансии
    'per_page': 100,  # количество вакансий на странице
    'experience': 'between1And3'
}

# URL для поиска вакансий
vacancy_url = 'https://api.hh.ru/vacancies'


response = requests.get(vacancy_url, headers=headers, params=params)
vacancies = response.json()

vacancies_ids = [x['id'] for x in vacancies['items']]

if len(vacancies_ids) > 0:
    k = 0
    for id in vacancies_ids:
        params = {
            'vacancy_id': id,  # id вакансии
            'resume_id': resume_id,
        }

        click_url = 'https://api.hh.ru/negotiations'
        try:
            response = requests.post(click_url, headers=headers, params=params)
            k += 1
            print("отлик +1")
            time.sleep(3)
        except Exception as e:
            print(f'Возникло исключение: {e}')
            print(f'отправлено {k} откликов')
            break
else:
    print("No matching vacancies found.")
