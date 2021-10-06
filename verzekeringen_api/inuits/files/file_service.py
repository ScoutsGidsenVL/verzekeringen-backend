import tempfile


class FileService:
    def get_temp_file(self, filename: str):
        return "%s/%s" % (tempfile.gettempdir(), filename)
