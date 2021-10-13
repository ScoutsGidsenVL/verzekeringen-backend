from django.conf import settings
from django.core.files.storage import  FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage

from inuits.files import FileService


class S3StorageService(FileService, S3Boto3Storage):

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = settings.AWS_DEFAULT_ACL
    file_overwrite = settings.AWS_S3_FILE_OVERWRITE

    local_storage = FileSystemStorage()

    # S3Boto3Storage
    # delete(file_path)
    # exists(file_path)
    # listdir(dir_path)
    # size(file_path)
    # get_modified_time(file_path)

    # Storage
    # open(file_path)
    # save(file_path, file_contents)
    # path(file_path)
    # url(file_path)
    
    def store_file(self, file_path: str, file_contents):
        return super().save(name=file_path, content=file_contents)

    # @TODO remove s3 specific code from this model
    def get_path(self):
        storage = self.file.storage
        if storage.exists(self.file.name):
            return self.file.name
        
        return self.get_absolute_path()

    def get_absolute_path(self):
        return self.file.path

    def as_attachment(self, file_src_path: str, file_dest_path: str):
        result = self.connection.meta.client.copy_object(
            Bucket=self.bucket_name,
            CopySource=self.bucket_name + "/" + file_src_path,
            Key=file_src_path)
        
        if result["ResponseMetaData"]["HTTPStatusCode"] != 200:
            raise Exception("Unable to retrieve attachment from S3 storage")
        
        return file_src_path

    def delete(self, using=None, keep_parents=False):
        storage = self.file.storage

        if storage.exists(self.file.name):
            storage.delete(self.file.name)

        super().delete(using=using, keep_parents=keep_parents)