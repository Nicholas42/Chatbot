import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any

from chatbot.bots.abc import BotABC


class Loader:
    bots: Dict[str, Any]
    bot_srcs = Path(__file__).parent / "bot_srcs"

    def __init__(self):
        self.bots = dict()

    def create_bot(self, bot_name: str, *args, **kwargs) -> BotABC:
        if bot_name not in self.bots:
            self.load_bot(bot_name)

        return self.bots[bot_name].create_bot(*args, **kwargs)

    def load_bot(self, bot_name, src_folder: Path = bot_srcs):
        if bot_name in self.bots:
            raise KeyError(f"Bot {bot_name} was already loaded, consider reloading it instead.")
        spec = importlib.util.spec_from_file_location(bot_name, f"{src_folder / bot_name}.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[bot_name] = module
        spec.loader.exec_module(module)
        self.bots[bot_name] = module

    def reload_bot(self, bot_name):
        self.bots[bot_name] = importlib.reload(self.bots[bot_name])
