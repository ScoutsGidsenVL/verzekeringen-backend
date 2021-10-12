from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorageService(S3Boto3Storage):

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = settings.AWS_DEFAULT_ACL
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE
