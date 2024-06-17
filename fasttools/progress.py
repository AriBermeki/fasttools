"""Process operations."""

from __future__ import annotations

import collections
import contextlib
import os
import signal
import subprocess
from concurrent import futures
from pathlib import Path
from typing import Callable, Generator, List, Optional, Tuple, Union
from .console_ import warn,info,debug, error,log
from .node_operations import get_node_bin_path,get_node_path,get_npm_path
import psutil
import typer
import httpx


def check_pypi_latest_package_version(package_name: str, last_version_check: str) -> bool:
    """
    example: 

    # Beispielaufruf
    if __name__ == "__main__":
        package_name = "requests"
        last_version_check = "2.25.0"
        is_newer_version = check_pypi_latest_package_version(package_name, last_version_check)
        print(f"Ist eine neuere Version verfügbar? {is_newer_version}")
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        response = httpx.get(url)
        response.raise_for_status()
        
        package_info = response.json()
        latest_version = package_info["info"]["version"]
        
        return latest_version > last_version_check
    except httpx.RequestError as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return False





def kill(pid):
    """Kill a process.

    Args:
        pid: The process ID.
    """
    os.kill(pid, signal.SIGTERM)


def get_num_workers() -> int:
    """Get the number of backend worker processes.

    Raises:
        Exit: If unable to connect to Redis.

    Returns:
        The number of backend worker processes.
    """
    return (os.cpu_count() or 1) * 2 + 1


def get_process_on_port(port) -> Optional[psutil.Process]:
    """Get the process on the given port.

    Args:
        port: The port.

    Returns:
        The process on the given port.
    """
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            for conns in proc.connections(kind="inet"):
                if conns.laddr.port == int(port):
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None


def is_process_on_port(port) -> bool:
    """Check if a process is running on the given port.

    Args:
        port: The port.

    Returns:
        Whether a process is running on the given port.
    """
    return get_process_on_port(port) is not None


def kill_process_on_port(port):
    """Kill the process on the given port.

    Args:
        port: The port.
    """
    if get_process_on_port(port) is not None:
        with contextlib.suppress(psutil.AccessDenied):
            get_process_on_port(port).kill()  # type: ignore


def change_port(port: str, _type: str) -> str:
    """Change the port.

    Args:
        port: The port.
        _type: The type of the port.

    Returns:
        The new port.

    """
    new_port = str(int(port) + 1)
    if is_process_on_port(new_port):
        return change_port(new_port, _type)
    info(
        f"The {_type} will run on port [bold underline]{new_port}[/bold underline]."
    )
    return new_port


def handle_port(service_name: str, port: str, default_port: str) -> str:
    """Change port if the specified port is in use and is not explicitly specified as a CLI arg or config arg.
    otherwise tell the user the port is in use and exit the app.

    We make an assumption that when port is the default port,then it hasnt been explicitly set since its not straightforward
    to know whether a port was explicitly provided by the user unless its any other than the default.

    Args:
        service_name: The frontend or backend.
        port: The provided port.
        default_port: The default port number associated with the specified service.

    Returns:
        The port to run the service on.

    Raises:
        Exit:when the port is in use.
    """
    if is_process_on_port(port):
        if int(port) == int(default_port):
            return change_port(port, service_name)
        else:
            error(f"{service_name.capitalize()} port: {port} is already in use")
            raise typer.Exit()
    return port


def new_process(args, run: bool = False, show_logs: bool = False, **kwargs):
    """Wrapper over subprocess.Popen to unify the launch of child processes.

    Args:
        args: A string, or a sequence of program arguments.
        run: Whether to run the process to completion.
        show_logs: Whether to show the logs of the process.
        **kwargs: Kwargs to override default wrap values to pass to subprocess.Popen as arguments.

    Returns:
        Execute a child program in a new process.

    Raises:
        Exit: When attempting to run a command with a None value.
    """
    node_bin_path = get_node_bin_path()
    if not node_bin_path:
        warn(
            "The path to the Node binary could not be found. Please ensure that Node is properly "
            "installed and added to your system's PATH environment variable or try running "
            "`reflex init` again."
        )
    if None in args:
        error(f"Invalid command: {args}")
        raise typer.Exit(1)
    # Add the node bin path to the PATH environment variable.
    env = {
        **os.environ,
        "PATH": os.pathsep.join(
            [node_bin_path if node_bin_path else "", os.environ["PATH"]]
        ),  # type: ignore
        **kwargs.pop("env", {}),
    }
    kwargs = {
        "env": env,
        "stderr": None if show_logs else subprocess.STDOUT,
        "stdout": None if show_logs else subprocess.PIPE,
        "universal_newlines": True,
        "encoding": "UTF-8",
        "errors": "replace",  # Avoid UnicodeDecodeError in unknown command output
        **kwargs,
    }
    debug(f"Running command: {args}")
    fn = subprocess.run if run else subprocess.Popen
    return fn(args, **kwargs)


@contextlib.contextmanager
def run_concurrently_context(
    *fns: Union[Callable, Tuple]
) -> Generator[list[futures.Future], None, None]:
    """Run functions concurrently in a thread pool.

    Args:
        *fns: The functions to run.

    Yields:
        The futures for the functions.
    """
    # If no functions are provided, yield an empty list and return.
    if not fns:
        yield []
        return

    # Convert the functions to tuples.
    fns = [fn if isinstance(fn, tuple) else (fn,) for fn in fns]  # type: ignore

    # Run the functions concurrently.
    executor = None
    try:
        executor = futures.ThreadPoolExecutor(max_workers=len(fns))
        # Submit the tasks.
        tasks = [executor.submit(*fn) for fn in fns]  # type: ignore

        # Yield control back to the main thread while tasks are running.
        yield tasks

        # Get the results in the order completed to check any exceptions.
        for task in futures.as_completed(tasks):
            # if task throws something, we let it bubble up immediately
            task.result()
    finally:
        # Shutdown the executor
        if executor:
            executor.shutdown(wait=False)


def run_concurrently(*fns: Union[Callable, Tuple]) -> None:
    """Run functions concurrently in a thread pool.

    Args:
        *fns: The functions to run.
    """
    with run_concurrently_context(*fns):
        pass



def atexit_handler():
    """Display a custom message with the current time when exiting an app."""
    log("Reflex app stopped.")


def get_command_with_loglevel(command: list[str]) -> list[str]:
    """Add the right loglevel flag to the designated command.
     npm uses --loglevel <level>, Bun doesnt use the --loglevel flag and
     runs in debug mode by default.

    Args:
        command:The command to add loglevel flag.

    Returns:
        The updated command list
    """
    npm_path = get_npm_path()
    npm_path = str(Path(npm_path).resolve()) if npm_path else npm_path

    if command[0] == npm_path:
        return command + ["--loglevel", "silly"]
    return command


def execute_command_and_return_output(command) -> str | None:
    """Execute a command and return the output.

    Args:
        command: The command to run.

    Returns:
        The output of the command.
    """
    try:
        return subprocess.check_output(command, shell=True).decode().strip()
    except subprocess.SubprocessError as err:
        error(
            f"The command `{command}` failed with error: {err}. This will return None."
        )
        return None