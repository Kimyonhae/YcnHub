from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import handler404

from . import views

urlpatterns = [
    path("", views.Main.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("<str:folderName>/", views.FolderView.as_view(), name="folder_page"),
    path("<str:folderName>/createFile/", views.FolderView.as_view(), name="file_upload"),
    path("<str:folderName>/updateFolder/", views.FolderView.as_view(), name="folder_update"),
    path("<str:folderName>/deleteFolder/", views.FolderView.as_view(), name="folder_delete"),
    path("<str:folderName>/<str:fileName>/", views.FileView.as_view()),
    path("<str:folderName>/<str:fileName>/delete_file/", views.FileView.as_view(), name="delete_file"),
    path("<str:folderName>/<str:fileName>/download_file/", views.FileView.as_view(), name="download_file"),
    path("favicon.ico", RedirectView.as_view(url="static/assets/favicon.ico")),
]

handler404 = views.custom_404_fn