from pathlib import Path


def load_embeddings(path: str) -> str:
    return ""


class TextFileReader:
    def __init__(self, file_path: str, encoding='UTF-8'):
        self.encoding = encoding
        self.path = Path(file_path)
        if not self.path.exists():
            raise ValueError()
        if not self.path.is_file():
            raise ValueError()
        self.file = None

    def read_all(self) -> str:
        return self.path.open(mode='r', encoding=self.encoding).read()
