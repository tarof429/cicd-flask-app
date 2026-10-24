import yaml, os
from pathlib import Path

class Prefs:
    def __init__(self, prefsConfig):
        self.prefsConfig = prefsConfig

    def load(self):

        if Path(self.prefsConfig).exists():
            with open(self.prefsConfig, 'r') as f:
                data = yaml.safe_load(f)
                return {} if data is None else data
        else:
            self._create_parent_dir()
            with open(self.prefsConfig, 'w') as f:
                return {} if yaml.dump(data, f) is None else data

    def write(self, data):
        self._create_parent_dir()
        with open(self.prefsConfig, 'w') as f:
            yaml.dump(data, f)

    def _create_parent_dir(self):
        parent = Path(self.prefsConfig).parent
        os.makedirs(parent, exist_ok =True)