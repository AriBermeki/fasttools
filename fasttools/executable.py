import importlib
import os
import pathlib
import sys
from typing import Literal, Optional, List
import shutil
from loguru import logger
from .utils import transfer
from pathlib import Path



class Executable:
    def __init__(
            self, 
            executable_name: str, 
            app_path: str, 
            console: bool, 
            exe_sys:Optional[Literal["onedir","onefile"]] = "onefile"
            ):
        self.app_path = pathlib.Path(app_path).resolve()
        self.app_name = self.app_path.stem
        self.exe_sys = exe_sys
        self.workdir = pathlib.Path("out").resolve()
        self.workdir.mkdir(exist_ok=True)
        self.pyinstallercommands: List[str] = []
        self.uvicorn_packages = [
            "uvicorn.lifespan.off",
            "uvicorn.lifespan.on",
            "uvicorn.lifespan",
            "uvicorn.protocols.websockets.auto",
            "uvicorn.protocols.websockets.wsproto_impl",
            "uvicorn.protocols.websockets.websockets_impl",
            "uvicorn.protocols.http.auto",
            "uvicorn.protocols.http.h11_impl",
            "uvicorn.protocols.http.httptools_impl",
            "uvicorn.protocols.websockets",
            "uvicorn.protocols.http",
            "uvicorn.protocols",
            "uvicorn.loops.auto",
            "uvicorn.loops.asyncio",
            "uvicorn.loops.uvloop",
            "uvicorn.loops",
            "uvicorn.logging",
            "aap.server.log",
        ]
        self.executable = executable_name
        self.console = console

        if self.console:
            self.pyinstallercommands.append("--console")
        else:
            logger.warning("Please configure uvicorn to set log_config=None to block command line access when console is set to False.")

    def add_hiddenimports(self, package: str):
        if package not in self.pyinstallercommands:
            self.pyinstallercommands.append(f"--hidden-import={package}")

    def log_level(self, log_level: str):
        self.pyinstallercommands.append(f"--log-level={log_level}")

    def add_data(self, folder_name: str):
        app_dir = self.workdir / folder_name
        self.pyinstallercommands.append(f"--add-data={app_dir.parent.parent}/{folder_name};{folder_name}")

    def add_binary(self, folder_name: str):
        app_dir = self.workdir / folder_name
        self.pyinstallercommands.append(f"--add-binary={app_dir.parent.parent}/{folder_name};{folder_name}")

    def set_icon(self, icon_name: str):
        icon_dir = self.workdir / icon_name
        self.pyinstallercommands.append(f"--icon={icon_dir.parent.parent}/{icon_name}")

    def _prepare_args(self):
        args = [
            str(self.app_path),
            "--distpath", str(self.workdir / "dist"),
            f"--name={self.executable}",
            f"--{self.exe_sys}",
            "--windowed",
        ]
        return args


    def _move_output(self):
        output_dir = self.workdir / "dist"
        if output_dir.exists():
            shutil.move(str(output_dir), "./")

    def _clean_up(self):
        spec = f"{self.executable}.spec"
        if os.path.exists(spec):
            os.remove(spec)
        if self.exe_sys == "onedir":
            transfer(source_path=Path("dist"), dist_path=Path("out"))
            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("dist", ignore_errors=True)
        elif self.exe_sys == "onefile":
            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("out", ignore_errors=True)
            os.rename(src="dist", dst="out")

        if os.path.isdir("__pycache__"):
            shutil.rmtree("__pycache__")

    def run_build(self, backend_framework: Optional[Literal["fastapi", "starlette", "flask", "robyn"]]):
        import PyInstaller.__main__ 
        if backend_framework in {"fastapi", "starlette"}:
            for package in self.uvicorn_packages:
                self.add_hiddenimports(package)

        args = self._prepare_args()
        
        sys.path.insert(0, str(self.workdir))
        module_path = ".".join(
            list(reversed([x.stem for x in self.app_path.parents if x.stem]))
            + [self.app_path.stem]
        )
        try:
            importlib.import_module(module_path)
        except ImportError as e:
            logger.error(f"No module found with this name: {e}")
            pass
        
        PyInstaller.__main__.run(args + self.pyinstallercommands)
        self._move_output()
        self._clean_up()
