import os
from django.urls import path
from .views import FermaAllView, CreateFermaView, FermaDetailView, FermaUpdate, FermaDelete

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    path('', FermaAllView.as_view(), name='all'),
    path('add/', CreateFermaView.as_view(), name='add'),
    path('ferma-detail/<int:pk>/', FermaDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', FermaUpdate.as_view(), name='ferma_update'),
    path('<int:pk>/delete/', FermaDelete.as_view(), name='ferma_delete'),
]