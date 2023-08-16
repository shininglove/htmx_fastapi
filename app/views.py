import os
from pathlib import Path
from string import Template
import urllib.parse


def generate_media_links(media: str) -> str:
    html = ""
    size = 400
    match Path(media).suffix:
        case ".mp4" | ".mov":
            html += f'<video controls width="{size}" height="{size}"><source src="{media}"></source></video>'
        case ".jpg" | ".png" | ".jpeg" | ".webp" | ".gif":
            html += f'<img class="w-48 h-48" src="{media}" />'
    return html


def generate_files(directory: str, hidden: bool = False) -> str:
    html = ""
    home = os.getenv("HOME", "/home")
    path = Path(directory)
    if not path.exists():
        return html
    dirs = [
        dir
        for dir in path.iterdir()
        if dir.is_dir() and dir.name.startswith(".") == hidden
    ]
    files = [
        file
        for file in path.iterdir()
        if file.is_file() and file.name.startswith(".") == hidden
    ]
    # initialize or prepend with the ..
    subhtml = ""
    for item in dirs:
        subhtml += Template(
            """
            <div 
                class="text-2xl cursor-pointer directory"
                hx-post="/media_search"
                hx-vals='{"dir_name": "$parent/$item_name"}' 
                hx-trigger="click"
                hx-target="#dir_search"
                hx-swap="outerHTML"
            >
                    📁$item_name
            </div>
        """
        ).safe_substitute({"item_name": item.name, "parent": item.parent})
    html += f"<div class='inline-flex gap-3'>{subhtml}</div>"
    media_html = ""
    for each in files:
        plain_filename = str(each).replace(home, "")
        filename = urllib.parse.quote(plain_filename)
        if os.name == "nt":
            filename = plain_filename.replace("\\", "/")
        match each.suffix:
            case ".mp4" | ".mov":
                media_html += media_create(filename, "📀")
            case ".jpg" | ".png" | ".jpeg" | ".webp" | ".gif":
                media_html += media_create(filename, "📷")
    html += f"<div class='inline-flex flex-wrap gap-3'>{media_html}</div>"
    return html


def media_create(filename: str, emoji: str) -> str:
    normal = urllib.parse.unquote(filename)
    media_link = """
        <div 
             class='cursor-pointer'
             hx-post='/showcase' 
             hx-vals='{"media": "/static$filename"}' 
             hx-target='#video_player' hx-trigger='click'>
             $emoji $normal
        </div>
    """
    media = Template(media_link).safe_substitute(
        {"filename": filename, "normal": Path(normal).name, "emoji": emoji}
    )
    return media
