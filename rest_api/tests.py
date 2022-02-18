# Python imports
import io
from PIL import Image

# Django imports
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase

# App imports
from project.models import Worker

def generate_photo_file():
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return 

# Testing rest_api app
class RestApiTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.new_worker = Worker.objects.create(
        name = 'jan',
        surname = 'kowalski',
        profession = 'mechanik',
        age = 34,
        image = generate_photo_file()
        )
        self.new_worker.save()
        self.pk = self.new_worker.id

    def test_delete(self):
        response = self.client.get('/api/ajax/delete/', {'id' : self.new_worker.id})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(b'{"deleted": true}' in response.content)
        self.assertEquals(Worker.objects.count(), 0)

