from contextlib import asynccontextmanager
from os import getenv
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Response
from fastapi.responses import FileResponse, HTMLResponse
from app.utilities import render_html
from app.views import generate_files, generate_main_input, generate_media_links


@asynccontextmanager
async def lifespan(_: FastAPI):
    static = Path("static")
    for dir in static.iterdir():
        if dir.is_symlink():
            dir.unlink()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/media_search", response_class=HTMLResponse)
def change_input(dir_name: Annotated[str, Form()], response: Response):
    home = getenv("HOME", "/home")
    home = Path(home) / dir_name
    response.headers["HX-Trigger-After-Settle"] = "refetch"
    return generate_main_input(home)


@app.get("/", response_class=HTMLResponse)
async def index():
    home = getenv("HOME", "/home")
    html = render_html("index.svelte", {"title": "FileSystem", "home": home})
    return HTMLResponse(content=html, status_code=200)


@app.get("/static/{files:path}", response_class=HTMLResponse)
def static(files: str):
    location = Path("static") / files
    if location.exists():
        return FileResponse(location)
    raise HTTPException(status_code=404, detail="file was not found")


@app.post("/showcase", response_class=HTMLResponse)
def data(media: Annotated[str, Form()]):
    html = generate_media_links(media)
    return HTMLResponse(content=html, status_code=200)


@app.post("/filesystem", response_class=HTMLResponse)
def filesystem(search: Annotated[str, Form()]):
    # iteratively symlink path with parts
    home = getenv("HOME", "/home")
    if search == "":
        search = home
    sym_path = search.replace(home, "")
    static_sym = Path(f"static/{sym_path}")
    if not static_sym.exists() and not static_sym.is_symlink():
        static_sym.symlink_to(Path(search))
    html = generate_files(search)
    return HTMLResponse(content=html, status_code=200)
