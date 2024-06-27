from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.Main.as_view(), name="index"),
    path("<int:folderId>/", views.FolderView.as_view(), name="folder_view"),
    path("<int:folderId>/edit/", views.FolderView.as_view(), name="edit_folder"),
    path(
        "<int:folderId>/delete_folder/",
        views.FolderView.as_view(),
        name="delete_folder",
    ),
    path("<int:folderId>/createFile/", views.FileView.as_view(), name="file_post"),
    path("<int:folderId>/<int:fileId>/", views.FileView.as_view(), name="file_view"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password_reset/", views.forgotPassword, name="password_reset"),
    path(
        "<int:folderId>/<int:fileId>/download_file/",
        views.FileBox.as_view(),
        name="file_download",
    ),
    path(
        "<int:folderId>/<int:fileId>/delete_file/",
        views.FileBox.as_view(),
        name="file_delete",
    ),
    path("favicon.ico", RedirectView.as_view(url="static/assets/favicon.ico")),
]
