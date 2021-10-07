class TextUtils:
    @staticmethod
    def replace(path, dictionary):
        data = ""
        with open(path, "r") as file:
            for key in dictionary.keys():
                data = file.read().replace(key, str(dictionary[key]))

        return data
