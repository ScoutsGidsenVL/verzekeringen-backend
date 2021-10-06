class TextUtils:
    @staticmethod
    def replace(self, path, dictionary):
        data = ""
        with open(path, "r") as file:
            for key in dictionary.keys():
                data = file.read().replace(key, dictionary[key])

        return data
