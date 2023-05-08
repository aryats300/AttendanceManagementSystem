from django.urls import path
from .views import upload_csv, success

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('success/', success, name='success'),
    # path('my-view/', my_view, name='my_view'),
]