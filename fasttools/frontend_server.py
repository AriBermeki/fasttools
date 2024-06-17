from multiprocessing import Process
from pathlib import Path
from typing import Any, Dict, Optional, Union
import uvicorn
from fastapi import FastAPI
import subprocess
import os
import asyncio
import sys
import pkg_resources as pkg
from pywry import PyWry

def native(
        host: str = "127.0.0.1",
        port: int = 8000,
        *,
        width: int = 800,
        height: int = 600,
        title: str,
        icon: Optional[Union[Path, str]] = None,
        json_data: Dict[str, Any] = None,
        download_path: Optional[Union[Path, str]] = None
    ):
    html = f"<script>window.location.replace('http://{host}:{port}')</script>"
    
    async def main_loop():
        while True:
            await asyncio.sleep(1)
    
    try:
        handler = PyWry()
        outgoing = dict(
            html=html,
            width=width,
            height=height,
            title=title,
            icon=icon,
            json_data=json_data,
            download_path=download_path
        )
        handler.send_outgoing(outgoing)
        handler.start()
        
        # PyWry creates a new thread for the backend,
        # so we need to run the main loop in the main thread.
        # otherwise, the program will exit immediately.
        handler.loop.run_until_complete(main_loop())
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
        sys.exit(0)

def frontend_server(frontend: str, frame: str):
    frontend_path = Path(frontend).resolve()
    
    # Define commands based on the framework type
    frame_commands = {
        "react": "npm start",
        "vite": "npm run dev",
        "next": "npm run dev"
    }

    if frame not in frame_commands:
        raise ValueError(f"Unknown frame type: {frame}. Expected one of {', '.join(frame_commands.keys())}.")

    # Commands for running the server and installing dependencies
    run_server_command = frame_commands[frame]
    install_command = ["npm", "install"]
    node_modules_path = frontend_path / "node_modules"
    
    # Ensure the frontend directory exists
    if not frontend_path.is_dir():
        raise FileNotFoundError(f"The directory {frontend_path} does not exist.")

    # Install dependencies if node_modules does not exist
    if not node_modules_path.is_dir():
        subprocess.run(install_command, cwd=frontend_path, shell=True, check=True)
    
    # Run the frontend server
    subprocess.run(run_server_command, cwd=frontend_path, shell=True, check=True)

def backend_server(app: FastAPI, port: int = 8000, host: str = "127.0.0.1", reload: bool = False, workers: int = 1, log_config = None):
    uvicorn.run(app, host=host, port=port, reload=reload, workers=workers, log_config=log_config)

def serve_development(
        frontend_dir: str,
        frame: str,
        app: FastAPI,
        port: int = 8000,
        host: str = "127.0.0.1",
        reload: bool = True,
        workers: int = 1,
        log_config = None,
        width: int = 800,
        height: int = 600,
        icon: Optional[Union[Path, str]] = None,
        json_data: Dict[str, Any] = None,
        download_path: Optional[Union[Path, str]] = None,
        *,
        title: str,
    ):
    # Thread for Backend server
    backend_thread = Process(target=backend_server, args=(app, port, host, reload, workers, log_config))
    backend_thread.start()
    
    # Thread for Native Window
    native_thread = Process(target=native, kwargs={
        'host': host,
        'port': port,
        'width': width,
        'height': height,
        'title': title,
        'icon': icon if icon else pkg.resource_filename('fasttools', "app.png"),
        'json_data': json_data,
        'download_path': download_path,
    })
    native_thread.start()
    
    # Thread for Frontend server
    frontend_thread = Process(target=frontend_server, args=(frontend_dir, frame))
    frontend_thread.start()

    # Wait for threads to finish
    backend_thread.join()
    native_thread.join()
    frontend_thread.join()
