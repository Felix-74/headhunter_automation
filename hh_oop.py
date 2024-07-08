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

    def get_resume_list(self):
        response = requests.get('https://api.hh.ru/resumes/mine',
                                headers=self.headers)
        resume_list = response.json().get('items', [])
        if not resume_list:
            print("Резюме не найдено")
            return []
        else:
            print("Resume List:", resume_list)
            self.resume_id = resume_list[0]['id']
            print("Using Resume ID:", self.resume_id)
            return resume_list

    def search_vacancies(self, search_row, area=113, period=3000,
                         per_page=100, experience='between1And3'):
        params = {
            'text': search_row,
            'area': area,
            'period': period,
            'per_page': per_page,
            'experience': experience
        }
        vacancy_url = 'https://api.hh.ru/vacancies'
        response = requests.get(vacancy_url, headers=self.headers,
                                params=params)
        vacancies = response.json()
        self.vacancies_ids = [x['id'] for x in vacancies['items']]
        print(len(self.vacancies_ids))
        return self.vacancies_ids

    def respond_to_vacancies(self):
        if not self.vacancies_ids:
            print("No matching vacancies found.")
            return

        k = 0
        for vacancy_id in self.vacancies_ids:
            params = {
                'vacancy_id': vacancy_id,
                'resume_id': self.resume_id,
            }
            click_url = 'https://api.hh.ru/negotiations'
            try:
                response = requests.post(
                    click_url,
                    headers=self.headers,
                    params=params
                )
                k += 1
                print("отлик +1")
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

class ParkingLot:
    def __init__(self, n):
        self.n = n
        self.park_cars = set()

    def park(self, carID):
        if len(self.parked_cars) < self.n:
            self.parked_cars.add(carID)
            return True
        else:
            return False


    def unpark(self, carID):
        if carID in self.parked_cars:
            self.parked_cars.remove(carID)