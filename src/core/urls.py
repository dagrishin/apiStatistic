import os
from django.urls import path
from .views import IndexView

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]