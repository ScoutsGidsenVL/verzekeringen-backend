import json
from django.http import QueryDict
from rest_framework import parsers


class MultipartJsonParser(parsers.MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type=media_type, parser_context=parser_context)

        data = {}

        data = json.loads(result.data["detail"])

        qdict = QueryDict("", mutable=True)
        qdict.update(data)

        return parsers.DataAndFiles(qdict, result.files)
