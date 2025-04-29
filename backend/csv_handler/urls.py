from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_csv_files, name="upload_csv_files"),
    path(
        "download/<uuid:file_id>/",
        views.download_processed_file,
        name="csv_download_processed",
    ),
]
