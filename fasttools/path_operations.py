"""Path operations."""

from __future__ import annotations
from .node_operations import constants
import json
import os
import re
import shutil
from pathlib import Path
import psutil
import hashlib
from .console_ import console




def detect_package_change(json_file_path: str) -> str:
    with open(json_file_path, "r") as file:
        json_data = json.load(file)
    json_string = json.dumps(json_data, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode())
    return hash_object.hexdigest()

def manipulate_config_file(config_path, entries, index):
    if entries is None:
        entries = []
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config_content = file.readlines()
    else:
        config_content = []
    insert_index = -1
    for i, line in enumerate(config_content):
        if f'{index} = ' in line:
            insert_index = i + 1
            break
    if insert_index != -1:
        for entry in entries:
            js_entry = f"  {entry},\n"
            if js_entry not in config_content:
                config_content.insert(insert_index, js_entry)
                insert_index += 1
        with open(config_path, 'w') as file:
            file.writelines(config_content)
        print("Die Einträge wurden erfolgreich hinzugefügt.")
    else:
        print("Die Datei enthält keine nextConfig Definition.")




join = os.linesep.join


def rm(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def cp(src: str, dest: str, overwrite: bool = True) -> bool:
    if src == dest:
        return False
    if not overwrite and os.path.exists(dest):
        return False
    if os.path.isdir(src):
        rm(dest)
        shutil.copytree(src, dest)
    else:
        shutil.copyfile(src, dest)
    return True


def mv(src: str, dest: str, overwrite: bool = True) -> bool:
    if src == dest:
        return False
    if not overwrite and os.path.exists(dest):
        return False
    rm(dest)
    shutil.move(src, dest)
    return True


def mkdir(path: str):
    os.makedirs(path, exist_ok=True)


def ln(src: str, dest: str, overwrite: bool = False) -> bool:
    if src == dest:
        return False
    if not overwrite and (os.path.exists(dest) or os.path.islink(dest)):
        return False
    if os.path.isdir(src):
        rm(dest)
        os.symlink(src, dest, target_is_directory=True)
    else:
        os.symlink(src, dest)
    return True


def psutil_kill(proc_pid: int):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def update_json_file(file_path: str, update_dict: dict[str, int | str]):
    fp = Path(file_path)
    fp.touch(exist_ok=True)
    fp.write_text("{}") if fp.stat().st_size == 0 else None
    json_object = {}
    if fp.stat().st_size == 0:
        with open(fp) as f:
            json_object = json.load(f)
    json_object.update(update_dict)
    with open(fp, "w") as f:
        json.dump(json_object, f, ensure_ascii=False)


def find_replace(directory: str, find: str, replace: str):
    for root, _dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            text = re.sub(find, replace, text)
            with open(filepath, "w") as f:
                f.write(text)




def output_system_info():
    """Show system information if the loglevel is in DEBUG."""
    if console._LOG_LEVEL > constants.LogLevel.DEBUG:
        return


    console.rule(f"System Info")
    