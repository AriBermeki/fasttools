<p align="center">
  <a href="https://www.yellow-sic.com/">
    <img width="100" src="./fasttools/app.png">
  </a>
  </br>
</p>

<h2 align="center">Fasttools </h2>
<h3 align="center">a set of python funktions and classes for web development </h3>
<h4 align="center">Please note: this library is currently in early alpha and is NOT ready for production use.</h4>

## 📦 Installation

---------------------
fasttools is available on PyPI and can be installed with pip:

```bash
pip install fasttools
```

---------------------

## Project folder structure

```plaintext
project_folder_struktur/
│
├── client/
│   ├── 
├── .venv
├── main.py
├── build.py

```

## Usage

### main.py
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
from fasttools_ import frontend,shutdown, serve_development
from contextlib import asynccontextmanager

static_directory = Path(__file__).parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await frontend(
        app=app, 
        static_directory=static_directory, 
        status="dev",
        frame="vite"
        )
    yield

app = FastAPI(lifespan=lifespan)

#app.mount("/static", StaticFiles(directory=static_directory), name="static")

@app.get("/exit")
async def exit():
    await shutdown()


if __name__ == "__main__":
    import uvicorn
    serve_development(frontend_dir="client",frame= "vite", app="app:app", title='Hallo')
    # uvicorn.run(app=app)
```






### In June 2024, fasttools was just publicly released by software architecture Malek Ali at Yellow-SiC Group and is in alpha stage.
<p>Anyone can install and use fasttools, There may be issues, but we are actively working to resolve them</p>
