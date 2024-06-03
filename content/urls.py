from django.urls import path
from .views import UploadFeed, Profile, Main, Reply

urlpatterns = [
    path('upload', UploadFeed.as_view(), name='upload'),
    path('Reply', Reply.as_view(), name='reply'),
    path('profile', Profile.as_view(), name='profile'),
    path('main', Main.as_view(), name='main'),
]



