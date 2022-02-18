from django.http import JsonResponse
from rest_framework.views import APIView

from project.models import Worker

class DeleteWorker(APIView):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Worker.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
