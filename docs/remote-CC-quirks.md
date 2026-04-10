# Remote Claude Code settings

## Environment

### Envvars

We use a custom environment that sets:
- `GH_TOKEN=...`
    - `Content: write` is one of the permissions; see the adding assets section that requires this

### Specially installed tools
All tools are installed through a session start hook that detects a special envvar Anthropic sets for remote CC sessions. See `.claude/hooks/session-start.sh`

In theory, we could use the special script area that Anthropic allows you to write to, but AFAICT it does not allow you to _persist_ things into the actual CC agent filesystem (meaning if you install something to `~/.local/bin` it's not present once the CC session actually starts). So we have to use a `SessionStart` hook.

Additionally installed binaries:
- `gh` - Anthropic provides a github MCP, but I want the fuller power of `gh`. It

## Adding assets to GitHub

GH doesn't expose a public API for uploading images directly into Issues or PRs. This is rather valuable becauase I want CC remote sessions to be capable of pushing PRs that demonstrate their work, via static images or GIFs.

I don't want to commit these files to the git history itself. I want to upload them just like I would if I was a human creating a PR: adding the image into the Issue or PR directly. That appears to work under the hood in the UI by GH quickly doing an upload to it's own host then adding a reference to that in the PR/Issue. Okay, so we need a host.

Turns out that GH releases can have assets. And API access to assets _does_ exist. I've created a special release just for assets at https://github.com/Quidge/tools/releases/tag/asset-dump .

Two assets cannot have the same name, so we attach a UUID suffix to the end of the uploaded file. You'd normally use `gh release upload asset-dump /path.png ...` to do this but we have a dedicated script that will do this + generate a unique name:
```sh
$ uv run scripts/upload-asset.py /tmp/a-screenshot.png
https://github.com/quidge/tools/releases/download/asset-dump/a-screenshot+<uuid>.png
```

That can now be embedded in a PR with something like:
```sh
gh issue comment 34 --repo quidge/tools \
  --body '![screenshot](https://github.com/Quidge/tools/releases/download/asset-dump/screenshot.png)'
```
