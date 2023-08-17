from contextlib import asynccontextmanager
import shutil
import urllib.parse
from os import environ, getenv
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Response
from fastapi.responses import FileResponse, HTMLResponse
from app.utilities import render_html
from app.views import (
    InputOptions,
    generate_file_list,
    generate_main_input,
    generate_media_links,
    generate_plain_input,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    static = Path("static")
    for dir in static.iterdir():
        if dir.is_symlink():
            dir.unlink()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/search_input", response_class=HTMLResponse)
def gen_input():
    options = InputOptions(
        color="pink",
        color_strength=500,
        method="post",
        endpoint="new_directory",
        target="this",
        event="click from:#changemenu",
        name="new_folder"
    )
    return generate_plain_input(options)

@app.post("/new_directory", response_class=HTMLResponse)
def new_directory(new_folder: Annotated[str, Form()], response: Response):
    filesystem = getenv("CURRENT_FILESYSTEM")
    if filesystem is not None:
        create_folder = Path(filesystem) / new_folder
        create_folder.mkdir(exist_ok=True)
    response.headers["HX-Trigger-After-Settle"] = "refetch"
    return ""



@app.post("/media_search", response_class=HTMLResponse)
def change_input(dir_name: Annotated[str, Form()], response: Response):
    home = getenv("HOME", "/home")
    home = Path(home) / dir_name
    response.headers["HX-Trigger-After-Settle"] = "refetch"
    return generate_main_input(home)


@app.post("/move_mode", response_class=HTMLResponse)
def move_mode(response: Response):
    mode = getenv("MOVE_MODE")
    if mode is not None:
        environ.pop("MOVE_MODE")
    if mode is None:
        environ["MOVE_MODE"] = str(not mode)
    response.headers["HX-Trigger-After-Settle"] = "refetch"
    return ""


@app.post("/move_file", response_class=HTMLResponse)
def move_file(filename: Annotated[str, Form()], response: Response):
    home = getenv("HOME", "/tmp")
    home_location = Path(home)
    basefilename = filename.replace("/static/", "")
    basefilename = urllib.parse.unquote(basefilename)
    true_location = home_location / basefilename
    target = getenv("TARGET_MEDIA_DIR", "/tmp")
    target_location = Path(true_location).parent / target
    if target_location.exists():
        shutil.move(true_location, target_location)
    response.headers["HX-Trigger-After-Settle"] = "refetch"
    return ""


@app.post("/select_directory", response_class=HTMLResponse)
def select_directory(destination: Annotated[str, Form()], response: Response):
    target = getenv("TARGET_MEDIA_DIR")
    if target is not None:
        environ.pop("TARGET_MEDIA_DIR")
    if target is None:
        environ["TARGET_MEDIA_DIR"] = destination
    response.headers["HX-Trigger-After-Settle"] = "sendfile"
    return ""


@app.get("/", response_class=HTMLResponse)
async def index():
    if getenv("MOVE_MODE") is not None:
        environ.pop("MOVE_MODE")
    if getenv("TARGET_MEDIA_DIR") is not None:
        environ.pop("TARGET_MEDIA_DIR")
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
    environ["CURRENT_FILESYSTEM"] = search
    if not static_sym.exists() and not static_sym.is_symlink():
        static_sym.symlink_to(Path(search))
    html = generate_file_list(search)
    return HTMLResponse(content=html, status_code=200)
