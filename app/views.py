import os
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Literal
import urllib.parse


@dataclass
class InputOptions:
    endpoint: str
    event: str
    name: str
    target: str
    border_color: str
    placeholder: str
    value: str = ""
    method: str = "post"
    swap: str = "none"


def generate_plain_input(data: InputOptions) -> str:
    return f"""
    <input
        id="{data.name}"
        type="text"
        name="{data.name}"
        placeholder="{data.placeholder}"
        class="border-4 {data.border_color} mt-2 w-1/3 p-2"
        hx-{data.method}="/{data.endpoint}"
        hx-trigger="{data.event}"
        hx-target="{data.target}"
        hx-swap="{data.swap}"
        value="{data.value}"
    />
    """


def generate_main_input(home: Path | str) -> str:
    return f"""
    <input
        id="dir_search"
        type="text"
        name="search"
        class="border-4 border-purple-500 mt-2 w-1/3 p-2"
        hx-post="/filesystem"
        hx-trigger="refetch from:body, click from:#desktop"
        hx-target="#folder_files"
        value="{home}"
    />
    """


def generate_media_links(media: str) -> str:
    html = ""
    size = 400
    hx_actions = ""
    move_mode = os.getenv("MOVE_MODE")
    if move_mode:
        hx_actions = Template(
            """hx-post="/move_file" hx-target="#video_player" hx-trigger="sendfile from:body" hx-vals='{"filename": "$media"}'"""
        ).safe_substitute({"media": media})
    match Path(media).suffix:
        case ".mp4" | ".mov":
            html += f'<video id="showcase" {hx_actions} controls width="{size}" height="{size}"><source src="{media}"></source></video>'
        case ".jpg" | ".png" | ".jpeg" | ".webp" | ".gif":
            html += (
                f'<img id="showcase" {hx_actions} class="w-48 h-48" src="{media}" />'
            )
    return html


def format_directory(
    dirs: list[Path],
    move: bool,
    original_path: Path,
    sort_by: Literal["abc", "size"] | None = None,
) -> str:
    emoji = "📁"
    subhtml = ""
    if sort_by == "abc":
        dirs = sorted(dirs, key=lambda x: x.name.lower())
    if sort_by == "size":
        dirs = sorted(dirs, key=lambda y: y.stat(follow_symlinks=True).st_size)
    for item in dirs:
        parent = item.parent
        if os.name == "nt":
            parent = str(parent).replace("\\", "/")
        if move:
            emoji = "↪️ "
            subhtml += Template(
                """
                <div 
                    class="text-2xl cursor-pointer"
                    hx-post="/select_directory"
                    hx-vals='{"destination": "$item_name"}' 
                    hx-trigger="click"
                    hx-swap="none"
                >
                        $emoji$item_name
                </div>
            """
            ).safe_substitute(
                {"item_name": item.name, "parent": parent, "emoji": emoji}
            )
        else:
            subhtml += Template(
                """
                <div 
                    class="text-2xl cursor-pointer"
                    hx-post="/media_search"
                    hx-vals='{"dir_name": "$parent/$item_name"}' 
                    hx-trigger="click"
                    hx-target="#dir_search"
                    hx-swap="outerHTML"
                >
                        $emoji$item_name
                </div>
            """
            ).safe_substitute(
                {"item_name": item.name, "parent": parent, "emoji": emoji}
            )
    if not move:
        parent = original_path.parent
        if os.name == "nt":
            parent = str(parent).replace("\\", "/")
        subhtml += Template(
            """
           <div 
               class="text-2xl cursor-pointer"
               hx-post="/media_search"
               hx-vals='{"dir_name": "$parent"}' 
               hx-trigger="click"
               hx-target="#dir_search"
               hx-swap="outerHTML"
           >
                   $emoji$item_name
           </div>

        """
        ).safe_substitute({"item_name": "..", "parent": parent, "emoji": emoji})

    return subhtml


def generate_dirs(path: Path) -> str:
    html = ""
    dirs = [
        dir
        for dir in path.iterdir()
        if dir.is_dir() and dir.name.startswith(".") == False
    ]
    move_mode = bool(os.getenv("MOVE_MODE", 0))
    subhtml = format_directory(dirs, move=move_mode, original_path=path, sort_by="abc")
    html += f"<div id='folder_container' class='flex-wrap inline-flex gap-3 px-2'>{subhtml}</div>"
    return html


def format_files(
    files: list[Path],
    home: str,
    emoji: dict[str, str] = {"video": "📀", "photo": "📷"},
    sort_by: Literal["abc", "size"] | None = None,
) -> str:
    media_html = ""
    if sort_by == "abc":
        files = sorted(files, key=lambda x: x.name.lower())
    if sort_by == "size":
        files = sorted(files, key=lambda y: y.stat(follow_symlinks=True).st_size)
    for each in files:
        plain_filename = str(each).replace(home, "")
        filename = urllib.parse.quote(plain_filename)
        if os.name == "nt":
            filename = plain_filename.replace("\\", "/")
        match each.suffix:
            case ".mp4" | ".mov":
                media_html += media_create(filename, emoji["video"])
            case ".jpg" | ".png" | ".jpeg" | ".webp" | ".gif":
                media_html += media_create(filename, emoji["photo"])
    return media_html


def generate_files(path: Path, home: str) -> str:
    files = [
        file
        for file in path.iterdir()
        if file.is_file() and file.name.startswith(".") == False
    ]
    html = ""
    media_html = format_files(files, home, sort_by="size")
    html += f"<div id='folder_container' class='flex-wrap inline-flex gap-3 px-2'>{media_html}</div>"
    return html


def generate_file_list(directory: str) -> str:
    html = ""
    home = os.getenv("HOME", "/home")
    path = Path(directory)
    if not path.exists():
        return html
    # initialize or prepend with the ..
    html += generate_dirs(path)
    html += generate_files(path, home)
    return html


def media_create(filename: str, emoji: str) -> str:
    normal = urllib.parse.unquote(filename)
    media_link = """
        <div 
             class='cursor-pointer'
             hx-post='/showcase' 
             hx-vals='{"media": "/static$filename"}' 
             hx-target='#video_player' hx-trigger='click'
             hx-swap="innerHTML show:bottom"
        >
             $emoji $normal
        </div>
    """
    media = Template(media_link).safe_substitute(
        {"filename": filename, "normal": Path(normal).name, "emoji": emoji}
    )
    return media
