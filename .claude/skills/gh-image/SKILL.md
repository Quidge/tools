---
name: gh-image
description: Upload screenshots, images, or GIFs to this repository's GitHub release asset host and produce embeddable GitHub-flavored markdown. Use when the user wants visual proof for PRs, issues, or comments without committing binary files to git history, regardless of which client or workflow is used to publish the markdown.
---

# Publish an image to GitHub and get embeddable markdown

Screenshots and GIFs make PRs, issues, and comments far more convincing — but committing binaries bloats git history permanently. This flow uploads an image to a dedicated GitHub release (`asset-dump` on `quidge/tools`) that acts as a durable asset host, then hands back a URL you can drop into any GitHub-flavored markdown.

## Before you upload

- Confirm the image file exists and is the one you mean to publish — anyone with the asset URL can view it, so this is effectively public.
- Run from inside this repository. The script is invoked with `uv run` and shells out to an authenticated `gh` CLI, so both need to resolve from the repo root.

## Upload the image

Run the script with the path to your image (relative or absolute both work):

```sh
uv run scripts/upload-asset.py path/to/screenshot.png
```

On success it prints the hosted asset URL to stdout — that URL is the one thing you need from this step, so capture it:

```sh
$ uv run scripts/upload-asset.py /tmp/dark-mode-toggle.png
https://github.com/quidge/tools/releases/download/asset-dump/dark-mode-toggle+3f9c1a2e-<uuid>.png
```

A UUID is appended to the filename because a release can't hold two assets with the same name; this also means re-uploading never clobbers an earlier image. If the command exits non-zero it forwards the underlying `gh` error to stderr — read that instead of retrying blindly (a common cause is `gh` not being authenticated).

## Embed it in markdown

Wrap the URL in an image tag:

```md
![what the screenshot proves](https://github.com/quidge/tools/releases/download/asset-dump/<filename>+<uuid>.png)
```

Write alt text that states what the image *demonstrates* ("settings page after the dark-mode fix"), not just what it is ("screenshot"). That alt text is what a reviewer sees if the image ever fails to load, and it's what makes the visual proof legible on its own.

## No cleanup needed

Leave uploaded assets in the release. They're small relative to the host's capacity, nothing depends on stale ones once your markdown points at the current URL, and deleting an asset only risks breaking an embed someone already pasted elsewhere. Skipping cleanup is the intended workflow, not a shortcut — don't spend a turn tidying up.
