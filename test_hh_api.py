import unittest
from unittest.mock import patch, MagicMock
from hh_oop import HHAPI  # Предположим, что ваш файл называется hh_api.py

class TestHHAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_resume_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': [{'id': '123'}]}
        mock_get.return_value = mock_response

        hh_api = HHAPI()
        resume_list = hh_api.get_resume_list()

        self.assertEqual(len(resume_list), 1)
        self.assertEqual(hh_api.resume_id, '123')

    @patch('requests.get')
    def test_search_vacancies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': [{'id': '456'}, {'id': '789'}]}
        mock_get.return_value = mock_response

        hh_api = HHAPI()
        hh_api.get_resume_list()
        vacancies_ids = hh_api.search_vacancies('python')

        self.assertEqual(len(vacancies_ids), 2)
        self.assertIn('456', vacancies_ids)
        self.assertIn('789', vacancies_ids)

    @patch('requests.post')
    def test_respond_to_vacancies(self, mock_post):
        mock_response = MagicMock()
        mock_post.return_value = mock_response

        hh_api = HHAPI()
        hh_api.get_resume_list()
        hh_api.search_vacancies('python')
        hh_api.resume_id = '123'
        hh_api.vacancies_ids = ['456']

        hh_api.respond_to_vacancies()

        mock_post.assert_called_once_with(
            'https://api.hh.ru/negotiations',
            headers=hh_api.headers,
            params={'vacancy_id': '456', 'resume_id': '123'}
        )

if __name__ == "__main__":
    unittest.main()
