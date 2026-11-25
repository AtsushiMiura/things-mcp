# Things Ideas

This local plugin gives Codex and Claude Code the same Things MCP tools and the same discussion workflow. Ask either client to “reflect this in Things” or 「Thingsに反映して」. Include the project name the first time. The skill updates matching ideas and places new ideas under the discussion heading. Committed work stays in Linear.

## Load the plugin

Install uv and Things 3 on the Mac, enable Things URLs in Things settings, and make uv available to the client process. Both plugin manifests launch this checkout using its uv.lock. Run these commands from the repository root.

For Claude Code, start a session with `claude --plugin-dir "$PWD"`. For Codex, register the public fork with `codex plugin marketplace add AtsushiMiura/things-mcp --ref codex/things-local-plugin`, then `codex plugin add things-ideas@things-local`, and start a new chat. Use the plugin configuration alone if you previously added the same server separately. The upstream Claude Desktop MCP bundle provides tools only.

## Enable heading creation

対象のMacで同梱の [Things MCP Create Heading.shortcut](../shortcuts/Things%20MCP%20Create%20Heading.shortcut) を開き、名前をそのままにして「追加」を一度クリックしてください。同じMacユーザーで使うCodexとClaude Codeの両方に反映されます。

たとえば「Thingsの『セミナー構想』プロジェクトに『秋の企画案』という見出しを作って、IDを教えて」と頼めます。MCPはプロジェクトIDを指定してThings公式のCreate Headingアクションを実行します。初回の実行時にmacOSがThingsへのアクセス許可を求める場合があります。

## Upstream updates

Reserve the fork’s master branch for fast-forward updates from hald/master. Keep plugin changes on a separate default branch. The included workflow runs on manual dispatch or weekly on Monday at 08:23 JST. It advances master and opens a single PR from master to the default branch when upstream commits are missing. Further updates advance the open PR. Review and merge using a merge commit so future ancestry comparisons remain valid.

Activation requires pushing the plugin branch, selecting it as the fork’s default branch, enabling Actions on the fork, and allowing Actions to create pull requests in repository settings. The workflow skips master as a target. Divergent mirror history or a GitHub permission restriction fails the run for manual review.
