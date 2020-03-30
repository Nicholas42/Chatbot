import json
from typing import Tuple

import dotenv
from os import environ
from pathlib import Path


class Config(dict):
    def __init__(self, path: Path = Path(__file__).parent / ".." / "data" / "configuration",
                 env_file: Path = Path(__file__).parent / ".." / ".env"):
        super().__init__()
        self.path = path
        dotenv.load_dotenv(str(env_file.absolute()))
        for i in path.glob("*.json"):
            with open(str(i.absolute())) as f:
                d: dict = json.load(f)
                if not isinstance(d, dict):
                    raise ValueError(f"Config file {self.path} does not provide a dictionary.")
            self.update(self._load_dict(d))

    def _load_dict(self, inp, prefix=""):
        out = dict()
        for key, value in inp.items():
            if isinstance(value, dict):
                out[key] = self._load_dict(value, f"{prefix}{key.upper()}_")
            elif key.startswith("_") and value is None:
                out[key[1:]] = self._load_hidden(key[1:], prefix)
            else:
                out[key] = value
        return out

    @staticmethod
    def _load_hidden(key, prefix):
        env_name = f"{prefix}{key.upper()}"
        ret = environ.get(env_name)
        if ret is None:
            raise KeyError(f"Hidden config parameter {env_name} is needed.")
        return ret


def adapt_config(dic: dict, matches) -> dict:
    """ If the .env names cannot match the needed names. """
    ret = dic.copy()
    for i in matches:
        ret[i[1]] = ret.pop(i[0])

    return ret
