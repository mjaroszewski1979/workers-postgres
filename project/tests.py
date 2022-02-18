# Python imports
import io
from PIL import Image

# Django imports
from django.db.models.query import QuerySet
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, resolve
from django.conf import settings
from django.shortcuts import get_object_or_404
from . import views

# App imports
from .models import Worker

def generate_photo_file():
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return 

# Testing project app
class ProjectTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.new_worker = Worker.objects.create(
        name = 'jan',
        surname = 'kowalski',
        profession = 'mechanik',
        age = 34,
        image = generate_photo_file()
        )
        self.new_worker.save()
        self.pk = self.new_worker.id

    def test_index_url_is_resolved(self):
        url = reverse('worker-list')
        self.assertEquals(resolve(url).func.view_class, views.WorkersList)

    def test_index_get(self):
        response = self.client.get(reverse('worker-list'))
        self.assertContains(response, 'Home | Workers', status_code=200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(str(response.context['page_obj']), '<Page 1 of 1>')

    def test_worker_detail_url_is_resolved(self):
        url = reverse('worker-detail', args=(self.pk,))
        self.assertEquals(resolve(url).func.view_class, views.WorkerDetail)

    def test_worker_detail_get(self):
        response = self.client.get(reverse('worker-detail', args=(self.pk,)))
        self.assertContains(response, 'Detail | Workers', status_code=200)
        self.assertTemplateUsed(response, 'worker_detail.html')
        self.assertEquals(str(response.context['object']), str(self.new_worker))

    def test_average_url_is_resolved(self):
        url = reverse('average')
        self.assertEquals(resolve(url).func.view_class, views.AverageView)

    def test_average_get(self):
        response = self.client.get(reverse('average'))
        result = Worker.objects.get_average_age()
        self.assertContains(response, 'Average | Workers', status_code=200)
        self.assertTemplateUsed(response, 'average.html')
        self.assertEquals(response.context['average'], result)

    def test_worker_create_url_is_resolved(self):
        url = reverse('worker-create')
        self.assertEquals(resolve(url).func.view_class, views.WorkerCreateView)

    def test_worker_create_get(self):
        response = self.client.get(reverse('worker-create'))
        self.assertContains(response, 'Create | Workers', status_code=200)
        self.assertTemplateUsed(response, 'worker_create.html')

    def test_worker_create_post(self):
        data={
            'name' : 'maciej',
            'surname' : 'jaroszewski',
            'profession' : 'tester',
            'age' : 18
        }
        response = self.client.post(reverse('worker-create'), data, follow=True)
        self.assertContains(response, 'Create | Workers', status_code=200)
        self.assertTemplateUsed(response, 'worker_create.html')
        self.assertEquals(Worker.objects.count(), 2)

    def test_worker_update_url_is_resolved(self):
        url = reverse('worker-update', args=(self.pk,))
        self.assertEquals(resolve(url).func.view_class, views.WorkerUpdate)

    def test_worker_update_get(self):
        response = self.client.get(reverse('worker-update',args=(self.pk,) ))
        self.assertContains(response, 'Update | Workers', status_code=200)
        self.assertTemplateUsed(response, 'worker_update.html')

    def test_worker_update_post(self):
        data={
            'name' : 'robert',
            'surname' : 'jaroszewski',
            'profession' : 'tester',
            'age' : 18
        }
        response = self.client.post(reverse('worker-update', args=(self.pk,)), data, follow=True)
        worker = get_object_or_404(Worker, id=self.pk)
        self.assertContains(response, 'Home | Workers', status_code=200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEquals(worker.name, 'robert')

    def test_get_average_age(self):
        second_worker = Worker.objects.create(
        name = 'robert',
        surname = 'lewangolski',
        profession = 'mechanik',
        age = 50,
        image = generate_photo_file()
        )
        second_worker.save()
        average_age = Worker.objects.get_average_age()
        result = [[x, y] for x, y in average_age][0][1]
        self.assertEquals(result, 42)

    def test_image_upload(self):
        self.assertFalse(self.new_worker.image is None)

    def test_csv_view_url_is_resolved(self):
        url = reverse('csv_view')
        self.assertEquals(resolve(url).func.view_class, views.CsvView)

    def test_csv_view_get(self):
        response = self.client.get(reverse('csv_view'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Profession,Average age\r\nmechanik,34\r\n' in response.content)
        self.assertEquals(response['Content-Disposition'], 'attachment; filename="average.csv"')








