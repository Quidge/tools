---
name: gh-image
description: Publish visual proof — screenshots, images, or GIFs — as GitHub release assets and produce embeddable GitHub-flavored markdown, keeping binaries out of git history. Use when the user wants images in a PR, issue, or comment, or when another skill needs a hosted image URL for markdown.
---

# GitHub Image Asset and Markdown Workflow

## Upload the asset

Run from the repo root, so `uv run` resolves the relative script path:

```sh
$ uv run scripts/upload-asset.py path/to/image.png
https://github.com/quidge/tools/releases/download/asset-dump/image+<uuid>.png
```

The script prints the hosted URL on success; no URL means the upload failed, so read stderr. The `+<uuid>` suffix is required — two release assets cannot share a name.

## Embed the markdown

Drop the printed URL into a GitHub-flavored markdown image:

```md
![alt-text](https://github.com/quidge/tools/releases/download/asset-dump/<filename>+<uuid>.png)
```

Alt text states what the image proves.

No cleanup needed — leaving many assets in the release is fine.
