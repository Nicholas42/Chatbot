import json
from collections import UserDict
from os import environ
from pathlib import Path

import dotenv


class Config(UserDict):
    def __init__(self, path: Path = Path(__file__).parent / ".." / "data" / "configuration",
                 env_file: Path = Path(__file__).parent / ".." / ".env"):
        super().__init__()
        self.path = path
        self.env_file = env_file
        self.environ = None
        self.load()

    def load(self, path=None, env_file=None):
        self.path = path or self.path
        self.env_file = env_file or self.env_file
        self.environ = dotenv.dotenv_values(str(self.env_file.absolute()))
        for i in self.path.glob("*.json"):
            with open(str(i.absolute())) as f:
                self.data[i.stem] = json.load(f)

        self._sub_variables(self.data)

    def _sub_variables(self, iterable):
        try:
            items = iterable.items() if isinstance(iterable, dict) else enumerate(iterable)
        except TypeError:
            return
        for k, v in items:
            if isinstance(v, str):
                if v.startswith("$"):
                    v = v[1:]
                    iterable[k] = environ.get(v, self.environ[v])
            else:
                self._sub_variables(v)


def adapt_config(dic: dict, matches) -> dict:
    """ If the .env names cannot match the needed names. """
    ret = dic.copy()
    for i in matches:
        ret[i[1]] = ret.pop(i[0])

    return ret


config = Config()
