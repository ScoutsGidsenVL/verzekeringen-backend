import logging


logger = logging.getLogger(__name__)


class TextUtils:
    @staticmethod
    def replace(path, dictionary):
        try:
            with open(path, "r") as f:
                contents = f.read()
                for key in dictionary.keys():
                    contents = contents.replace("(((" + key + ")))", str(dictionary[key]))

                return contents
        except Exception as exc:
            logger.error("An error occurred while preparing the html template")

        return ""
