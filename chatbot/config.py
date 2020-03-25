import json
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
            ret = {}
            for key in d:
                if key.startswith("_"):
                    ret[key[1:]] = self._load_hidden(key[1:], d[key])
                else:
                    ret[key] = d[key]
            self.update(ret)

    @staticmethod
    def _load_hidden(key, value):
        for i in value:
            env_name = f"{key.upper()}_{i.upper()}"
            value[i] = environ.get(env_name)
            if not value[i]:
                raise KeyError(f"Hidden config parameter {env_name} is needed.")
        return value
