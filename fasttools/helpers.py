import asyncio
import functools
import hashlib
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, Optional, Tuple, Union
import warnings
import re
import unicodedata
import secrets
import string
import math


class Vector(complex):
    """
    Simple immutable 2D vector class based on the Python complex number type
    """

    abs_tol = 1e-10

    x = complex.real
    y = complex.imag
    __add__ = lambda self, other: type(self)(complex.__add__(self, other))
    __sub__ = lambda self, other: type(self)(complex.__sub__(self, other))
    __mul__ = lambda self, other: type(self)(complex.__mul__(self, other))
    __truediv__ = lambda self, other: type(self)(complex.__truediv__(self, other))
    __len__ = lambda self: 2
    __round__ = lambda self, ndigits=None: type(self)(
        round(self.x, ndigits), round(self.y, ndigits)
    )

    def __eq__(self, other):
        return math.isclose(self.x, other.x, abs_tol=self.abs_tol) and math.isclose(
            self.y, other.y, abs_tol=self.abs_tol
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __iter__(self):
        return iter([self.x, self.y])

    def __str__(self):
        return str(tuple(self))

    def __repr__(self):
        return f"{type(self).__name__}{str(self)}"

    @classmethod
    def polar(cls, radians, magnitude):
        return cls(
            round(math.cos(radians) * magnitude, 10),
            round(math.sin(radians) * magnitude, 10),
        )

    @property
    def magnitude(self):
        return abs(self)

    @property
    def degrees(self):
        return math.degrees(self.radians)

    @property
    def radians(self):
        return math.atan2(self.y, self.x)

    def with_x(self, value):
        return type(self)(value, self.y)

    def with_y(self, value):
        return type(self)(self.x, value)

    def with_magnitude(self, value):
        return self * value / abs(self)

    def with_radians(self, value):
        magnitude = abs(self)
        return type(self).polar(value, magnitude)

    def with_degrees(self, value):
        radians = math.radians(value)
        magnitude = abs(self)
        return type(self).polar(radians, magnitude)

def random_string(length):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def slugify(value: str) -> str:
    """
    Converts to lowercase, removes non-word characters (alphanumerics and underscores)
    and converts spaces to hyphens. Also strips leading and trailing whitespace.
    """
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value).strip("-")

def deprecated(reason, version, delete_version):
    """
    A decorator function that marks a function as deprecated.

    :param reason: The reason for deprecation.
    :param version: The version from which the function was deprecated.
    :param delete_version: The version in which the function will be removed from the API.
    """

    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(
                f"Call to {func.__name__}() is deprecated in version {version} "
                f"and will be removed in version {delete_version}. {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return new_func

    return decorator


def deprecated_class(reason: str, version: str, delete_version: str):
    def decorator(cls):
        msg = f"{cls.__name__} is deprecated since version {version} and will be removed in version {delete_version}. {reason}"

        # Wrap the original __init__ method
        orig_init = cls.__init__

        @functools.wraps(orig_init)
        def new_init(self, *args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
            orig_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls

    return decorator

def is_pytest() -> bool:
    """Check if the code is running in pytest."""
    return 'pytest' in sys.modules


def is_coroutine_function(obj: Any) -> bool:
    """Check if the object is a coroutine function.

    This function is needed because functools.partial is not a coroutine function, but its func attribute is.
    Note: It will return false for coroutine objects.
    """
    while isinstance(obj, functools.partial):
        obj = obj.func
    return asyncio.iscoroutinefunction(obj)


def is_file(path: Optional[Union[str, Path]]) -> bool:
    """Check if the path is a file that exists."""
    if not path:
        return False
    if isinstance(path, str) and path.strip().startswith('data:'):
        return False  # NOTE: avoid passing data URLs to Path
    try:
        return Path(path).is_file()
    except OSError:
        return False


def hash_file_path(path: Path) -> str:
    """Hash the given path."""
    return hashlib.sha256(path.as_posix().encode()).hexdigest()[:32]


def is_port_open(host: str, port: int) -> bool:
    """Check if the port is open by checking if a TCP connection can be established."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except (ConnectionRefusedError, TimeoutError):
        return False
    except Exception:
        return False
    else:
        return True
    finally:
        sock.close()


def schedule_browser(host: str, port: int) -> Tuple[threading.Thread, threading.Event]:
    """Wait non-blockingly for the port to be open, then start a webbrowser.

    This function launches a thread in order to be non-blocking.
    This thread then uses `is_port_open` to check when the port opens.
    When connectivity is confirmed, the webbrowser is launched using `webbrowser.open`.

    The thread is created as a daemon thread, in order to not interfere with Ctrl+C.

    If you need to stop this thread, you can do this by setting the Event, that gets returned.
    The thread will stop with the next loop without opening the browser.

    :return: A tuple consisting of the actual thread object and an event for stopping the thread.
    """
    cancel = threading.Event()

    def in_thread(host: str, port: int) -> None:
        while not is_port_open(host, port):
            if cancel.is_set():
                return
            time.sleep(0.1)
        webbrowser.open(f'http://{host}:{port}/')

    host = host if host != '0.0.0.0' else '127.0.0.1'
    thread = threading.Thread(target=in_thread, args=(host, port), daemon=True)
    thread.start()
    return thread, cancel


def kebab_to_camel_case(string: str) -> str:
    """Convert a kebab-case string to camelCase."""
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('-')))







def is_asyncio():
    try:
        return asyncio.current_task() is not None or sys.platform == "emscripten"
    except RuntimeError:
        return False


def is_pyodide():
    return sys.platform == "emscripten"





LOGGING_SCHEMA = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "custom_formatter",
            "filename": "server.log",
        }
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["file_handler"],
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["file_handler"],
            "level": "INFO",
        },
    },
}