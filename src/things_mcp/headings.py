"""Create a Things heading through the user's macOS shortcut."""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def create_heading(project_id: str, title: str) -> str:
    if not project_id.strip() or not title.strip():
        raise ValueError("A project ID and a heading title are required.")
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
        if not heading_id or any(c.isspace() for c in heading_id):
            raise ValueError("Shortcut returned no valid heading ID. Check the project before retrying.")
        return heading_id
