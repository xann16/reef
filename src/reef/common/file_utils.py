"""Provides some basic utility functions and wrappers for handling file system and file I/O."""

import json
import os


def load_json(filepath):
    """Returns object representing JSON data from file at given filepath."""
    with open(filepath, encoding="utf-8") as fp:
        return json.load(fp)


def dump_json(filepath, data):
    """Writes JSON data to file at given filepath."""
    with open(filepath, mode="w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)


def ensure_dir(dirpath):
    """Checks if directory exists at dirpath and if it does not, creates an empty directory there."""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
