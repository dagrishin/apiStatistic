import os

from django.urls import path

from . import views
app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    # path('', views.index_miner, name='statistic'),
    path('', views.FermaAllView.as_view(), name='all'),
    path('add/', views.CreateFermaView.as_view(), name='add'),
    path('ferma-detail/<int:pk>/', views.FermaDetailView.as_view(), name='detail'),
]