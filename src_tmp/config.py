from os import environ, path

from src.utils import dump_json, ensure_dir, load_json

CONFIG_PATH_ENV_VAR_NAME = "REEF_CONFIG"
CONFIG_FILE_NAME = "config.json"
CONFIG_PROJECT_DIR = "projects"

class Config:

    def __init__(self, config_path, exec_path, version) -> None:
        super().__init__()

        self._config_path = path.abspath(config_path)
        self._exec_path = path.abspath(exec_path)
        self._version = version

    @property
    def config_path(self) -> str:
        return self._config_path

    @property
    def exec_path(self) -> str:
        return self._exec_path

    @property
    def version(self) -> str:
        return self._version

    @property
    def version_major(self) -> str:
        return int(self._version.split('.')[0])

    @property
    def version_minor(self) -> str:
        return int(self._version.split('.')[1])

    @property
    def version_patch(self) -> str:
        return int(self._version.split('.')[2])

    @property
    def config_file_path(self) -> str:
        return Config._filepath(self.config_path)

    @property
    def projects_path(self) -> str:
        return path.join(self.config_path, CONFIG_PROJECT_DIR)

    def __str__(self) -> str:
        result = ""

        result += "Directories:" + "\n"
        result += " - config:     " + self.config_path + '\n'
        result += " - executable: " + self.exec_path + '\n'

        return result

    @staticmethod
    def get_path() -> str:
        return environ.get(CONFIG_PATH_ENV_VAR_NAME)

    @staticmethod
    def _filepath(dirpath) -> str:
        return path.join(dirpath, CONFIG_FILE_NAME)

    @staticmethod
    def from_json(dirpath):
        data = load_json(Config._filepath(dirpath))
        return Config(data["config_path"], data["exec_path"], data["version"])

    def save_as_json(self, dirpath, verbose=False) -> None:
        filepath = Config._filepath(dirpath)
        if verbose:
            print(f"Saving current config in '{filepath}'... ", end='')

        data = {
            "config_path": self.config_path,
            "exec_path": self.exec_path,
            "version": self.version
        }

        ensure_dir(dirpath)
        dump_json(filepath, data)

        if verbose:
            print("Done.")

    @staticmethod
    def load(version=None):
        dirpath = Config.get_path()
        if not dirpath:
            return None
        res = Config.from_json(dirpath)
        if res.version != version:
            print(f"NOTE: Reef version was changed from {res.version} to {version}.")
        return res

    @staticmethod
    def save(config) -> None:
        dirpath = Config.get_path()
        if not dirpath:
            raise RuntimeError("No config path set. Run init command to initialize reef environment.")
        config.save_as_json()

    def update_shell_config(self, verbose=False):
        INTRO = "# >>> reef initialize >>>"
        COMMENT = "# !! Contents within this block are managed by 'reef init' !!"
        OUTRO = "# <<< reef initialize <<<"

        rcpath = path.abspath(path.expanduser('~/.bashrc'))

        if verbose:
            print(f"Opening and updating '{rcpath}' shell config... ", end='')

        # load shell rc file (withoud already present reef section, if any)
        is_reef = False
        new_lines = []
        with open(rcpath, encoding='utf-8') as fp:
            for line in fp:
                if line.strip().startswith(INTRO):
                    is_reef = True
                if not is_reef:
                    new_lines.append(line)
                if line.strip().startswith(OUTRO):
                    is_reef = False

        assert not is_reef, "Closing reef section marker not found. Aborting!"

        # add new reef section
        new_lines.append("\n")
        new_lines.append(INTRO + "\n")
        new_lines.append(COMMENT + "\n")

        new_lines.append(f'export {CONFIG_PATH_ENV_VAR_NAME}="{self.config_path}"\n')
        new_lines.append(f'export PATH="{self.exec_path}:$PATH"\n')

        new_lines.append(OUTRO + "\n")
        new_lines.append("\n")

        # overwriting new shell rc file
        with open(rcpath, mode='w', encoding='utf-8') as fp:
            fp.writelines(new_lines)

        if verbose:
            print("Done.")
