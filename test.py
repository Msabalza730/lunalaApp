import unittest
import requests

from app import app, db

class TestApp(unittest.TestCase):
    base_url = 'http://127.0.0.1:5000'

    def test_index(self):
        response = requests.get(f'{self.base_url}/')
        self.assertEqual(response.status_code, 200)

    def test_medicines_get(self):
        response = requests.get(f'{self.base_url}/all_medicines')
        self.assertEqual(response.status_code, 200)

    def test_medicines_post(self):
        data = {
            'name': 'Test Medicine',
            'stock': 10,
            'due_date': '2024-01-31'
        }
        response = requests.post(f'{self.base_url}/update_medicines', data=data)
        self.assertEqual(response.status_code, 302) 

    def test_animals_get(self):
        response = requests.get(f'{self.base_url}/all_animals')
        self.assertEqual(response.status_code, 200)

    def test_animals_post(self):
        data = {
            'name': 'Test Animal'
        }
        response = requests.post(f'{self.base_url}/update_animals', data=data)
        self.assertEqual(response.status_code, 302) 

    def test_foods_get(self):
        response = requests.get(f'{self.base_url}/all_foods')
        self.assertEqual(response.status_code, 200)

    def test_foods_post(self):
        data = {
            'brand': 'Test Brand',
            'stock': '20', 
            'due_date': '2024-01-31',
            'animal_id': 1 
        }
        response = requests.post(f'{self.base_url}/update_foods', data=data)
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()

