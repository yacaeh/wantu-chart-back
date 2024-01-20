from django.urls import path

from s3.views import s3_upload

# postman headers {"enctype" : "multipart/form-data"}, body form-data     key: file   value: 파일선택

urlpatterns = [
    path('upload', s3_upload, name='s3_upload'),
]
