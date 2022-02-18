from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkersList.as_view(), name='worker-list'),
    path('csv/', views.CsvView.as_view(), name='csv_view'),
    path('average/', views.AverageView.as_view(), name='average'),
    path('create/', views.WorkerCreateView.as_view(), name='worker-create'),
    path('<pk>/', views.WorkerDetail.as_view(), name='worker-detail'),
    path('<pk>/update/', views.WorkerUpdate.as_view(), name='worker-update'),
]

