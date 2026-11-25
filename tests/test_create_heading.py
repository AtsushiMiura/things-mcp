import json
from pathlib import Path

import pytest

from things_mcp.server import add_heading


def test_heading_shortcut_receives_data_and_returns_id(mocker):
    mocker.patch("things.get", return_value={"type": "project"})
    title = '新案 "A" & B'

    mocker.patch('things.tasks', side_effect=[[], [{'title': title, 'uuid': 'heading-id'}]])

    def run(args, *, check, timeout):
        assert args[:3] == ["/usr/bin/shortcuts", "run", "Things MCP Create Heading"]
        assert check and timeout > 0
        request = Path(args[args.index("--input-path") + 1])
        assert json.loads(request.read_text()) == {"project_id": "project-id", "title": title}
        Path(args[args.index("--output-path") + 1]).write_text("heading-id\n")

    mocker.patch("things_mcp.headings.subprocess.run", side_effect=run)
    assert add_heading("project-id", title) == "heading-id"


def test_uncertain_heading_result_is_not_retried(mocker):
    mocker.patch("things.get", return_value={"type": "project"})
    mocker.patch("things.tasks", return_value=[])
    run = mocker.patch("things_mcp.headings.subprocess.run")
    with pytest.raises(ValueError, match="before retrying"):
        add_heading("project-id", "Title")
    run.assert_called_once()


def test_rejects_non_project_before_running_shortcut(mocker):
    mocker.patch("things.get", return_value={"type": "to-do"})
    run = mocker.patch("things_mcp.headings.subprocess.run")
    with pytest.raises(ValueError, match="existing Things project"):
        add_heading("todo-id", "Title")
    run.assert_not_called()


def test_empty_shortcut_output_recovers_only_new_matching_id(mocker):
    mocker.patch("things.get", return_value={"type": "project"})
    existing = {"title": "ダミー", "uuid": "old"}
    created = {"title": "ダミー", "uuid": "new"}
    reads = mocker.patch("things.tasks", side_effect=[
        [existing], [existing], [existing, created, {"title": "Other", "uuid": "other"}],
    ])
    run = mocker.patch("things_mcp.headings.subprocess.run")
    assert add_heading("project-id", "ダミー") == "new"
    assert all(call.kwargs == {"type": "heading", "project": "project-id"} for call in reads.call_args_list)
    run.assert_called_once()


def test_multiple_new_matching_headings_are_ambiguous(mocker):
    mocker.patch("things.get", return_value={"type": "project"})
    mocker.patch("things.tasks", side_effect=[[], [
        {"title": "Title", "uuid": "one"}, {"title": "Title", "uuid": "two"},
    ]])
    run = mocker.patch("things_mcp.headings.subprocess.run")
    with pytest.raises(ValueError, match="before retrying"):
        add_heading("project-id", "Title")
    run.assert_called_once()
