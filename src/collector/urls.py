import os
from django.urls import path
from .views import InformerAllView, CreateInformerView, InformerDetailView, InformerUpdate, InformerDelete

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    path('', InformerAllView.as_view(), name='all'),
    path('add/', CreateInformerView.as_view(), name='add'),
    path('detail/<int:pk>/', InformerDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', InformerUpdate.as_view(), name='informer_update'),
    path('delete/<int:pk>/', InformerDelete.as_view(), name='informer_delete'),
]