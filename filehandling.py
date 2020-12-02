from os import path, makedir
class Filepro:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_file(self):
        try:
            makedir(self.file_path, mode=0o777, exist_ok=True)
        except PermissionError:
            return False
        return True
