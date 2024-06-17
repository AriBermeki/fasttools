"""General utility functions."""

import os
from typing import Literal, Optional
import psutil
import multiprocessing
import sys
from pathlib import Path
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import os
from pathlib import Path
import platform
import contextlib
import os
import shutil
import time

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from typing import TypeVar, Type, Any, Callable, Generic


T = TypeVar("T")



class Ref(Generic[T]):
    def __init__(self):
        self._current: T = None

    @property
    def current(self) -> T:
        return self._current

    @current.setter
    def current(self, value: T):
        self._current = value

class classproperty:
    def __init__(self, func: Callable[[Type[T]], Any]) -> None:
        self.fget = func

    def __get__(self, instance: T, owner: Type[T]) -> Any:
        return self.fget(owner)

PWD = Path(".").resolve()


def _walk_files(path):
    """Walk all files in a path.
    This can be replaced with Path.walk() in python3.12.

    Args:
        path: The path to walk.

    Yields:
        The next file in the path.
    """
    for p in Path(path).iterdir():
        if p.is_dir():
            yield from _walk_files(p)
            continue
        yield p.resolve()



def _relative_to_pwd(path: Path) -> Path:
    """Get the relative path of a path to the current working directory.

    Args:
        path: The path to get the relative path for.

    Returns:
        The relative path.
    """
    if path.is_absolute():
        return path.relative_to(PWD)
    return path







def get_cpu_count() -> int:
    """Get the number of CPUs.

    Returns:
        The number of CPUs.
    """
    return multiprocessing.cpu_count()


def get_memory() -> int:
    """Get the total memory in MB.

    Returns:
        The total memory in MB.
    """
    try:
        return psutil.virtual_memory().total >> 20
    except ValueError:  # needed to pass ubuntu test
        return 0
    

def remove_logging(lgging_folder: str, log_file: str):
    try:
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
            log_file_path = os.path.join(application_path, lgging_folder, log_file)
        if os.path.exists(log_file_path):
            with open(log_file_path, "w"):
                pass
        else:
            return "Die Serverlog-Datei wurde nicht gefunden."
    except Exception as e:
        return e


def get_logging(lgging_folder: str, log_file: str):
    try:
        if getattr(sys, "frozen", False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(__file__)
            log_file_path = os.path.join(
                application_path, str(lgging_folder), str(log_file)
            )
        if os.path.exists(log_file_path):
            with open(log_file_path, "rb") as log:
                log_read = log.read()
                return log_read
        else:
            return FileNotFoundError()
    except Exception as e:
        return e
    


def transfer(source_path: Path, dist_path: Path):
    if not source_path.is_dir():
        raise ValueError(f"The source path {source_path} is not a valid directory.")

    if not dist_path.exists():
        dist_path.mkdir(parents=True, exist_ok=True)

    for item in source_path.iterdir():
        dest_item = dist_path / item.name
        if item.is_dir():
            shutil.copytree(item, dest_item, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest_item)





def transfer_frontend_protocoll(source_path, dist_path, frame):
    # Ensure paths are Path objects
    source_path = Path(source_path)
    dist_path = Path(dist_path)
    
    # Define build folder names based on the framework type
    build_folders = {
        "react": "build",
        "vite": "dist",
        "next": "out"
    }
    
    if frame not in build_folders:
        raise ValueError(f"Unknown frame type: {frame}. Expected one of {', '.join(build_folders.keys())}.")

    # Adjust source path to point to the framework's build folder
    source_path_ = source_path / build_folders[frame]

    # Ensure the source path is valid and exists
    if not source_path_.is_dir():
        raise ValueError(f"The source path {source_path_} is not a valid directory.")

    # Ensure the destination directory exists or create it
    if not dist_path.exists():
        dist_path.mkdir(parents=True, exist_ok=True)
    
    if frame == "react":
        build_sub_folder = source_path_ / "static"
        for item in build_sub_folder.iterdir():
            dest_item = dist_path / item.name
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
                
            else:
                shutil.copy2(item, dest_item)
        
        for item in source_path_.iterdir():
            dest_item = dist_path / item.name
            if item.is_dir():
                if item == source_path_ / "static":
                    continue
                
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_item)
                
        
    else:
        for item in source_path_.iterdir():
            dest_item = dist_path / item.name
            if item.is_dir():
                shutil.copytree(item, dest_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest_item)



async def shutdown():
    import os
    import signal
    os.kill(os.getpid(), signal.SIGINT)




async def productions(app: FastAPI, static_directory: Path):
    static_directory_path = static_directory.resolve()
    directory_ = static_directory_path
    
    index_html_path = directory_ / "index.html"

    @app.get("/")
    async def get_index():
        if not index_html_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(index_html_path, media_type='text/html')

    @app.get("/{asset_path:path}")
    async def get_assets(asset_path: str):
        asset_file_path = directory_ / asset_path
        if not asset_file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(asset_file_path)





async def development(app: FastAPI, vite_port: int, frame: str):

    # Determine the frontend port based on the given frame
    frontend_ports = {
        "react": 3000,
        "vite": vite_port if vite_port else 5173,  # Corrected the conditional expression
        "next": 3000
    }
    
    # Check if the given frame is valid
    if frame not in frontend_ports:
        raise ValueError(f"Unknown frame port type: {frame}. Expected one of {', '.join(frontend_ports.keys())}.")

    # Generate the HTML redirection script
    html = f"<script>window.location.replace('http://localhost:{frontend_ports[frame]}')</script>"

    # Define the root endpoint
    @app.get("/")
    async def get_index():
        return HTMLResponse(content=html, media_type='text/html')







async def frontend(
        status:Optional[Literal["prod","dev"]], 
        app:FastAPI, 
        static_directory:str, 
        vite_port:int=None,
        *,
        frame:Optional[Literal["react","vite","next"]]
    ):
    if status == "dev":
        await development(app=app, vite_port=vite_port, frame=frame)
    elif status=="prod":
        await productions(app=app, static_directory=static_directory)
    


def get_os() -> str:
    """Get the operating system.

    Returns:
        The operating system.
    """
    return platform.system()


def get_detailed_platform_str() -> str:
    """Get the detailed os/platform string.

    Returns:
        The platform string
    """
    return platform.platform()


def get_python_version() -> str:
    """Get the Python version.

    Returns:
        The Python version.
    """
    return platform.python_version()






class AssetFolderWatch:
    """Asset folder watch class."""

    def __init__(self, root):
        """Initialize the Watch Class.

        Args:
            root: root path of the public.
        """
        self.path = str(root)
        self.event_handler = AssetFolderHandler(root)

    def start(self):
        """Start watching asset folder."""
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()


class AssetFolderHandler(FileSystemEventHandler):
    """Asset folder event handler."""

    def __init__(self, root):
        """Initialize the AssetFolderHandler Class.

        Args:
            root: root path of the public.
        """
        super().__init__()
        self.root = root

    def on_modified(self, event: FileSystemEvent):
        """Event handler when a file or folder was modified.

        This is called every time after a file is created, modified and deleted.

        Args:
            event: Event information.
        """
        dest_path = self.get_dest_path(event.src_path)

        # wait 1 sec for fully saved
        time.sleep(1)

        if os.path.isfile(event.src_path):
            with contextlib.suppress(PermissionError):
                shutil.copyfile(event.src_path, dest_path)
        if os.path.isdir(event.src_path):
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            with contextlib.suppress(PermissionError):
                shutil.copytree(event.src_path, dest_path)

    def on_deleted(self, event: FileSystemEvent):
        """Event hander when a file or folder was deleted.

        Args:
            event: Event infomation.
        """
        dest_path = self.get_dest_path(event.src_path)

        if os.path.isfile(dest_path):
            # when event is about a file, pass
            # this will be deleted at on_modified function
            return

        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)

    def get_dest_path(self, src_path: str, app_assets:str, web_assets) -> str:
        """Get public file path.

        Args:
            src_path: The asset file path.

        Returns:
            The public file path.
        """
        return src_path.replace(
            str(self.root / app_assets), str(self.root / web_assets)
        )