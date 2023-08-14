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


def generate_files(directory: str, hidden: bool =False) -> str:
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
    subhtml = ""
    for item in dirs:
        subhtml += f'<div class="text-2xl cursor-pointer">📁{item.name}</div>'
    html += f"<div class='inline-flex gap-3'>{subhtml}</div>"
    media_html = ""
    for each in files:
        plain_filename = str(each).replace(home, "")
        filename = urllib.parse.quote(plain_filename)
        size = 200
        match each.suffix:
            case ".mp4" | ".mov":
                media_html += video_create(filename, size)
            case ".jpg" | ".png" | ".jpeg" | ".webp" | ".gif":
                media_html += image_create(filename, each.name)
    html += f"<div class='inline-flex flex-wrap gap-3'>{media_html}</div>"
    return html


def video_create(filename: str, size: int) -> str:
    video_link = "<video width='$size' height='$size' hx-post='/showcase' hx-vals='{\"media\": \"/static$filename\"}' hx-target='#video_player' hx-trigger='click'><source src='/static$filename'></source></video>"
    video = Template(video_link).safe_substitute({"filename": filename, "size": size})
    return video


def image_create(filename: str, each_name: str) -> str:
    img_link = "<img hx-post='/showcase' hx-vals='{\"media\": \"/static$filename\"}' hx-target='#video_player' hx-trigger='click' class='flex-row cursor-pointer w-20 h-20 border border-orange-400' src='/static$filename' alt='$each_name'/>"
    img = Template(img_link).safe_substitute(
        {"filename": filename, "each_name": each_name}
    )
    return img
