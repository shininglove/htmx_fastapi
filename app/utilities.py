from pathlib import Path
from string import Template


def render_html(filename: str, data: dict) -> str:
    templates = Path(".") / "templates"
    with open(templates / filename) as f:
        html = Template(f.read())
    return html.safe_substitute(**data)


def render_string(html: str, data: dict | None) -> str:
    if data is None:
        data = {}
    parsed_html = Template(html)
    return parsed_html.safe_substitute(**data)
