import tempfile

from django.core.files.storage import Storage


class FileService(Storage):

    @staticmethod
    def get_temp_file(filename: str):
        return "%s/%s" % (tempfile.gettempdir(), filename)
    
    def store_file(self, file_path: str, file_contents):
        return super().save(name=file_path, content=file_contents)
    
    def copy_file(self, file_src_path: str, file_dest_path:str):
        pass

    def as_attachment(self, file_path):
        return file_path
