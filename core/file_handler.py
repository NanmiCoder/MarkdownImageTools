class FileHandler:
    def read_file(self, file_path: str):
        """
        Reads the content of the file.
        :param file_path:
        :return:
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def write_file(self, file_path: str, content: str):
        """
        Writes the content to the file.
        :param file_path:
        :param content:
        :return:
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
