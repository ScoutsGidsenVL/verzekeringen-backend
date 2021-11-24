import logging


logger = logging.getLogger(__name__)


class TextUtils:
    @staticmethod
    def replace(path, dictionary, placeholder_start: str = "(((", placeholder_end: str = ")))"):
        try:
            with open(path, "r") as f:
                contents = f.read()
                for key in dictionary.keys():
                    contents = contents.replace(placeholder_start + key + placeholder_end, str(dictionary[key]))

                return contents
        except Exception as exc:
            logger.error("An error occurred while preparing the html template")

        return ""

    @staticmethod
    def compose_html_email(path_start, contents: str, path_end):
        start = ""
        with open(path_start, "r") as f:
            start = f.read()
        end = ""
        with open(path_end, "r") as f:
            end = f.read()

        return start + contents + end
