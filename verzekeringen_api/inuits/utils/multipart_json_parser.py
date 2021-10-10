import logging, json
from typing import Dict, Set, cast
from django.http import QueryDict
from django.core.exceptions import ValidationError
from rest_framework import parsers
from formencode.compound import Any
from formencode.variabledecode import variable_decode


logger = logging.getLogger(__name__)


class MultipartJsonParser(parsers.MultiPartParser):
    """

    @see https://stackoverflow.com/questions/20473572/django-rest-framework-file-upload/50514022#50514022
    """

    # def parse(self, stream: Any, media_type: Any = None, parser_context: Any = None) -> Dict[str, Any]:
    # result = cast(
    #     parsers.DataAndFiles, super().parse(stream, media_type=media_type, parser_context=parser_context)
    # )

    # _data_keys: Set[str] = set(result.data.keys())
    # _file_keys: Set[str] = set(result.files.keys())

    # _intersect = _file_keys.intersection(_data_keys)
    # if len(_intersect) > 0:
    #     raise ValidationError("files and data had intersection on keys: " + str(_intersect))

    # # merge everything together
    # merged = QueryDict(mutable=True)

    # merged.update(result.data)
    # merged.update(result.files)  # type: ignore

    # # decode it together
    # decoded_merged = variable_decode(merged)

    # parser_context["__JSON_AS_STRING__"] = True

    # if len(result.files) > 0:
    #     # if we had at least one file put everything into files so we
    #     # later know we had at least one file by running len(request.FILES)
    #     parser_context["request"].META["REQUEST_HAD_FILES"] = True
    #     return parsers.DataAndFiles(decoded_merged, {})  # type: ignore
    # else:
    #     # just put it into data, doesnt matter really otherwise
    #     return parsers.DataAndFiles(decoded_merged, {})  # type: ignore

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
