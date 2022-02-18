from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('ajax/delete/',  views.DeleteWorker.as_view(), name='worker_delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)