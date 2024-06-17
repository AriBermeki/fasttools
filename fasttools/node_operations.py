from __future__ import absolute_import, print_function
import platform
import os
from pathlib import Path
import shutil
import subprocess
import json
from functools import partial
from os.path import basename, dirname, join


class Constants:
    class Node:
        if platform.system() == "Windows":
            BIN_PATH = r"C:\Program Files\nodejs"
            PATH = r"C:\Program Files\nodejs\node.exe"
            NPM_PATH = r"C:\Program Files\nodejs\npm.cmd"
        elif platform.system() == "Darwin":  # macOS
            BIN_PATH = "/usr/local/bin"
            PATH = "/usr/local/bin/node"
            NPM_PATH = "/usr/local/bin/npm"
        else:  # Annahme: Linux
            BIN_PATH = "/usr/bin"
            PATH = "/usr/bin/node"
            NPM_PATH = "/usr/bin/npm"

constants = Constants()

def which(program: str) -> str | None:
    return shutil.which(program)

def get_node_bin_path() -> str | None:
    if not os.path.exists(constants.Node.BIN_PATH):
        str_path = which("node")
        return str(Path(str_path).parent.resolve()) if str_path else str_path
    return str(Path(constants.Node.BIN_PATH).resolve())

def get_node_path() -> str | None:
    if not os.path.exists(constants.Node.PATH):
        return which("node")
    return constants.Node.PATH

def get_npm_path() -> str | None:
    if not os.path.exists(constants.Node.NPM_PATH):
        return which("npm")
    return constants.Node.NPM_PATH

def run_npm(pkgdir, cmd, args=None, npm_bin="npm", wait=True, shell=False):
    """Run NPM."""
    
    node_bin = get_node_bin_path()
    node_path = get_node_path()
    npm_bin = get_npm_path() or npm_bin
    
    if not node_bin:
        raise ValueError("node executable not found. Make sure node is installed.")
    if not node_path:
        raise ValueError("node_path dose not found. Make sure node is installed.")
    if not npm_bin:
        raise ValueError("npm executable not found. Make sure npm is installed.")

    command = [npm_bin, cmd] + list(args or [])
    
    if wait:
        return subprocess.call(
            command,
            cwd=pkgdir,
            shell=shell,
        )
    else:
        return subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=pkgdir,
            shell=shell,
        )



class NPMPackage(object):
    """API to an NPM ``package.json``.

    :param filepath: Path to ``package.json`` or directory containing the file.
    :param npm_bin: Path to NPM binary. Defaults to ``npm``.
    :param commands: List of allowed NPM commands to invoke.
    :param shell: Run NPM in a shell. Defaults to ``False``.
    """

    def __init__(self, filepath, npm_bin="npm", commands=None, shell=False):
        """Initialize package."""
        self._commands = commands or [
            "build",
            "init",
            "install",
            "link",
            "run-script",
            "start",
            "stop",
            "test",
        ]
        self._package_json_path = filepath
        self._package_json_contents = None
        self._npm_bin = npm_bin
        self._shell = shell

    @property
    def package_json_path(self):
        """Get ``package.json`` file path."""
        if basename(self._package_json_path) != "package.json":
            return join(self._package_json_path, "package.json")
        return self._package_json_path

    @property
    def package_json(self):
        """Read ``package.json`` contents."""
        if self._package_json_contents is None:
            with open(self.package_json_path, "r") as fp:
                self._package_json_contents = json.load(fp)
        return self._package_json_contents

    def _run_npm(self, command, *args, **kwargs):
        """Run an NPM command.

        By default the call is blocking until NPM is finished and output
        is directed to stdout. If ``wait=False`` is passed to the method,
        you get a handle to the process (return value of ``subprocess.Popen``).

        :param command: NPM command to run.
        :param args: List of arguments.
        :param wait: Wait for NPM command to finish. By defaul
        """
        return run_npm(
            dirname(self.package_json_path),
            command,
            npm_bin=self._npm_bin,
            args=args,
            shell=self._shell,
            **kwargs
        )

    def __getattr__(self, name):
        """Run partial function for an NPM command."""
        name = name.replace("_", "-")
        if name in self._commands:
            return partial(self._run_npm, name)
        raise AttributeError("Invalid NPM command.")


class YarnPackage(NPMPackage):
    """Yarn package."""

    def __init__(self, filepath, yarn_bin="yarn", commands=None, shell=False):
        """Initialize package."""
        super(YarnPackage, self).__init__(
            filepath, npm_bin=yarn_bin, commands=commands or ["install"], shell=shell
        )
