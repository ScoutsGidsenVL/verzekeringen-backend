import logging, json
from typing import Dict, Set, cast
from django.http import QueryDict
from django.core.exceptions import ValidationError
from rest_framework import parsers


logger = logging.getLogger(__name__)


class MultipartJsonParser(parsers.MultiPartParser):
    """

    @see https://stackoverflow.com/questions/20473572/django-rest-framework-file-upload/50514022#50514022
    @see https://stackoverflow.com/questions/61161227/uploading-multiple-images-and-nested-json-using-multipart-form-data-in-django-re
    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream, media_type=media_type, parser_context=parser_context)

        data = {}

        for key, value in result.data.items():
            logger.info("KEY: %s", key)
            logger.info("VALUE: %s", value)
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

        # data = json.loads(result.data["detail"])

        # qdict = QueryDict("", mutable=True)
        # qdict.update(data)

        # return parsers.DataAndFiles(qdict, result.files)
        return parsers.dataAndFiles(data, result.files)
