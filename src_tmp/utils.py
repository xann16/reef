import json
from os import makedirs, path


def load_json(filepath):
    with open(filepath, encoding="utf-8") as fp:
        return json.load(fp)


def dump_json(filepath, data):
    with open(filepath, mode="w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)


def ensure_dir(dirpath):
    if not path.exists(dirpath):
        makedirs(dirpath)
