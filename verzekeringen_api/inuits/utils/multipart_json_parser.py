import json
from django.http import QueryDict
from rest_framework import parsers


class MultipartJsonParser(parsers.MultiPartParser):
    """

    @https://stackoverflow.com/questions/20473572/django-rest-framework-file-upload/50514022#50514022
    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type=media_type, parser_context=parser_context)

        data = {}

        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if "{" in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value

        data = json.loads(result.data["detail"])

        qdict = QueryDict("", mutable=True)
        qdict.update(data)

        return parsers.DataAndFiles(qdict, result.files)
