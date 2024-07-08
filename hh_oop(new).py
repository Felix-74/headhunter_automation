import os
import time
import requests
from dotenv import load_dotenv

# Загрузите переменные окружения из .env файла
load_dotenv()

class HHAPI:
    def __init__(self):
        self.access_token = os.getenv('ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("Access token not found in environment variables")
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'HH-User-Agent': 'myapp'
        }
        self.resume_id = None
        self.vacancies_ids = []
        self.responded_vacancies_file = 'responded_vacancies.txt'
        self.responded_vacancies = self.load_responded_vacancies()

    def get_resume_list(self):
        response = requests.get('https://api.hh.ru/resumes/mine', headers=self.headers)
        resume_list = response.json().get('items', [])
        if not resume_list:
            print("Резюме не найдено")
            return []
        else:
            print("Resume List:", resume_list)
            self.resume_id = resume_list[0]['id']
            print("Using Resume ID:", self.resume_id)
            return resume_list

    def search_vacancies(self, search_row, area=113, period=3000, per_page=100, experience='between1And3'):
        params = {
            'text': search_row,
            'area': area,
            'period': period,
            'per_page': per_page,
            'experience': experience
        }
        vacancy_url = 'https://api.hh.ru/vacancies'
        response = requests.get(vacancy_url, headers=self.headers, params=params)
        vacancies = response.json()
        self.vacancies_ids = [x['id'] for x in vacancies['items']]
        print(len(self.vacancies_ids))
        return self.vacancies_ids

    def load_responded_vacancies(self):
        if os.path.exists(self.responded_vacancies_file):
            with open(self.responded_vacancies_file, 'r') as file:
                responded_vacancies = file.read().splitlines()
            return set(responded_vacancies)
        return set()

    def save_responded_vacancy(self, vacancy_id):
        with open(self.responded_vacancies_file, 'a') as file:
            file.write(f'{vacancy_id}\n')

    def respond_to_vacancies(self):
        if not self.vacancies_ids:
            print("No matching vacancies found.")
            return

        k = 0

        for vacancy_id in self.vacancies_ids:
            if vacancy_id in self.responded_vacancies:
                print(f"Already responded to vacancy ID: {vacancy_id}")
                continue

            params = {
                'vacancy_id': vacancy_id,
                'resume_id': self.resume_id,
            }
            click_url = 'https://api.hh.ru/negotiations'
            try:
                response = requests.post(click_url, headers=self.headers, params=params)
                if response.status_code == 200:
                    self.save_responded_vacancy(vacancy_id)
                    self.responded_vacancies.add(vacancy_id)
                    k += 1
                    print("отлик +1")
                elif response.status_code == 403:
                    print(f"Already responded to vacancy ID: {vacancy_id} (403 Forbidden)")
                    self.save_responded_vacancy(vacancy_id)
                    self.responded_vacancies.add(vacancy_id)
                else:
                    print(f"Failed to respond to vacancy ID: {vacancy_id}")

                time.sleep(6)
                print("отликов", k)
                print(response.status_code)
                print(response.text)
            except Exception as e:
                print(f'Возникло исключение: {e}')
                print(f'отправлено {k} откликов')

if __name__ == "__main__":
    hh_api = HHAPI()

    # Получение списка резюме
    hh_api.get_resume_list()

    search_row = 'NAME:("python" OR "python программист" NOT "senior " NOT "QA")'

    # Поиск вакансий
    hh_api.search_vacancies(search_row)

    # Отклик на вакансии
    hh_api.respond_to_vacancies()
