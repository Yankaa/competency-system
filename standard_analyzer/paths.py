from typing import Union, Callable
from os.path import exists
from ast import literal_eval


class File:
    def __init__(self, path):
        self.path = path

    def read(self) -> str:
        file = open(self.path)
        content = file.read()
        file.close()
        return content

    def read_object(self):
        return literal_eval(self.read())

    def write(self, content: str, mode='w'):
        file = open(self.path, mode)
        file.write(content)
        file.close()

    def write_object(self, obj):
        self.write(repr(obj))

    def exists(self):
        return exists(self.path)


def _gen(path: str) -> Callable[[Union[str, int]], File]:
    path = 'standarts/%s/%%s.txt' % path
    return lambda filename: File(path % str(filename))


downloaded = _gen('downloaded')
parsed = _gen('parsed')
stemmed = _gen('stemmed')
vectorized = _gen('vectorized')
