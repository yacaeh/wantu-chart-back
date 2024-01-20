import os
import datetime

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status


def _get_key_file(f, path, given_file_name=None):

    filename, file_extension = os.path.splitext(f.name)
    print(filename)
    key_name = "{filename}-{date}-{microsecond}{extension}".format(
        filename=filename,
        date=str(datetime.datetime.now().date()),
        microsecond=datetime.datetime.now().microsecond,
        extension=file_extension
    )

    full_key_name = os.path.join(path, key_name).replace(os.sep, "/", -1)

    conn = boto.s3.connect_to_region(
        settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        calling_format=boto.s3.connection.OrdinaryCallingFormat(),
    )
    bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    k = Key(bucket)

    k.key = full_key_name
    k.set_contents_from_string(f.read())
    k.set_acl('public-read')

    return full_key_name


@csrf_exempt
def s3_upload(request):
    f = request.FILES.get('file')
    file_name = request.POST.get('file_name', None)
    type = request.POST.get('type', None)
    
    full_key_name = _get_key_file(f, type, request.FILES.get('file').name)

    return JsonResponse({"url": settings.S3_URL + full_key_name}, status=status.HTTP_200_OK)
