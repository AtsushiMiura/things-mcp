"""Create a Things heading through the user's macOS shortcut."""

import json
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import things


def _matching_ids(project_id: str, title: str) -> set[str]:
    return {
        heading["uuid"]
        for heading in things.tasks(type="heading", project=project_id)
        if heading.get("title") == title
    }


def create_heading(project_id: str, title: str) -> str:
    if not project_id.strip() or not title.strip():
        raise ValueError("A project ID and a heading title are required.")
    before = _matching_ids(project_id, title)
    with TemporaryDirectory() as temp:
        request = Path(temp) / "heading.json"
        result = Path(temp) / "heading-id.txt"
        request.write_text(json.dumps({"project_id": project_id, "title": title}), encoding="utf-8")
        subprocess.run(
            ["/usr/bin/shortcuts", "run", "Things MCP Create Heading",
             "--input-path", str(request), "--output-path", str(result),
             "--output-type", "public.plain-text"],
            check=True, timeout=60,
        )
        heading_id = result.read_text(encoding="utf-8").strip() if result.is_file() else ""

    # Things can commit the heading shortly after Shortcuts exits.
    for delay in (0, 0.1, 0.2, 0.4, 0.8, 1.6):
        if delay:
            time.sleep(delay)
        created = _matching_ids(project_id, title) - before
        if heading_id in created:
            return heading_id
        if len(created) == 1:
            return next(iter(created))
        if len(created) > 1:
            break
    raise ValueError("Could not identify the new heading. Check the project before retrying.")
