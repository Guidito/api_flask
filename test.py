import unittest
import json
from app import create_app
from config import config
from app import db

class TestAPI(unittest.TestCase):
    def setUp(self):
        enviroment = config['test']
        self.app = create_app(enviroment)
        self.client = self.app.test_client()

        self.content_type = 'application/json'
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_one_equals_one(self):
        self.assertEqual(1, 1)

    def test_get_all_tasks(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_first_task(self):
        new_path = self.path + '/1'

        response = self.client.get(path = new_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        task_id = data['data']['id']

        self.assertEqual(task_id, 1)

    def test_not_found(self):
        new_path = self.path + '/100'

        response = self.client.get(path = new_path, content_type=self.content_type)

        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        data = {
            'title': 'title', 'description': 'description',
            'deadline': '2020-05-12 12:00:00'
        }

        response = self.client.post(path=self.path, data=json.dumps(data), content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        task_id = data['data']['id']

        self.assertEqual(task_id, 3)

    def test_update_task(self):
        data = {
            'title': 'Nuevo titulo'
        }
        new_path = self.path + '/1'
        response = self.client.put(path=new_path, data=json.dumps(data), content_type=self.content_type)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        title = data['data']['title']

        self.assertEqual(title, 'Nuevo titulo')

    def test_delete_task(self):
        new_path = self.path + '/1'

        response = self.client.delete(path=new_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)
        
        response = response = self.client.get(path=new_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()