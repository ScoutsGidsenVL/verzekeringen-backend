from scouts_auth.inuits.utils import SettingsHelper


class StorageSettings(SettingsHelper):

    DEFAULT_FILE_STORAGE = "DEFAULT_FILE_STORAGE"
    USE_S3_STORAGE = "USE_S3_STORAGE"

    S3_STORAGE_SERVICE = "scouts_auth.inuits.files.aws.S3StorageService"

    @staticmethod
    def get_default_storage():
        return StorageSettings.get(StorageSettings.DEFAULT_FILE_STORAGE)

    @staticmethod
    def use_s3():
        return StorageSettings.get_bool(StorageSettings.USE_S3_STORAGE, False)

    @staticmethod
    def get_s3_storage_service_name():
        return StorageSettings.S3_STORAGE_SERVICE

    @staticmethod
    def get_s3_bucket_name():
        return StorageSettings.get("AWS_STORAGE_BUCKET_NAME")

    @staticmethod
    def get_s3_default_acl():
        return StorageSettings.get("AWS_DEFAULT_ACL")

    @staticmethod
    def get_s3_file_overwrite():
        return StorageSettings.get("AWS_S3_FILE_OVERWRITE")
