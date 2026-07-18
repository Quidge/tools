"""Ensure every redirect stub in _redirects.json is gitignored and untracked.

Each key in `_redirects.json` is the stub filename that `scripts/build_redirects.py`
generates at the repo root (e.g. `soundboard.html`). Those stubs are build
artifacts and must never be committed (same treatment as the generated
`index.html`). It is easy to add a redirect and forget to gitignore the stub it
produces.

This script asks git the real questions rather than managing `.gitignore` text
itself:

  - Is each stub ignored? It runs `git check-ignore` per stub, which honors *any*
    ignore mechanism (a plain line, a glob, a nested .gitignore). For a stub that
    is not ignored, it self-heals by appending a plain line to `.gitignore` (all
    missing entries in one sorted write), then tells the contributor to review,
    `git add .gitignore`, and commit again. If `.gitignore` does not exist yet,
    it is created with those entries.

  - Is each stub already tracked by git? `.gitignore` has no effect on files that
    are already committed, so `git ls-files` is the check that actually closes
    the "a stub got committed" hole. A tracked stub is reported with a
    `git rm --cached` hint. This check runs even when the ignore check already
    failed, so both problems surface in one pass.

Run as a pre-commit hook it behaves like the other autofix hooks
(`end-of-file-fixer`, `trailing-whitespace`): it appends missing entries in place
and exits non-zero when it changed anything, so the commit fails and the
contributor just re-adds `.gitignore` and commits again. Appends keep exactly one
trailing newline so this never fights `end-of-file-fixer`. Pass `--check` to
validate without writing (report what is out of sync and exit non-zero).

Exit status is 0 only when every stub is ignored and none is tracked; otherwise
1.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def stub_names(redirects_file: Path) -> list[str]:
    """Return the sorted stub filenames (the keys) from the redirects map."""
    if not redirects_file.exists():
        return []
    redirects = json.loads(redirects_file.read_text())
    return sorted(redirects)


def unignored_stubs(stubs: list[str], repo_root: Path) -> list[str]:
    """Return the stubs that git does NOT currently ignore.

    Uses `git check-ignore -q` per stub. That command exits 0 when the path is
    ignored, 1 when it is not, and >1 on an actual error (which we surface rather
    than silently treating as "not ignored").
    """
    result = []
    for stub in stubs:
        completed = subprocess.run(
            ["git", "check-ignore", "-q", "--", stub],
            cwd=repo_root,
        )
        if completed.returncode == 0:
            continue  # ignored
        if completed.returncode == 1:
            result.append(stub)  # not ignored
        else:
            raise RuntimeError(
                f"`git check-ignore` failed for {stub!r} "
                f"(exit {completed.returncode})"
            )
    return result


def tracked_stubs(stubs: list[str], repo_root: Path) -> list[str]:
    """Return the stub filenames that git is already tracking (should be none)."""
    if not stubs:
        return []
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", *stubs],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return [name for name in result.stdout.split("\0") if name]


def append_entries(gitignore_file: Path, entries: list[str]) -> None:
    """Append `entries` to `.gitignore` under a comment, with one trailing newline.

    Creates the file if it does not exist. Preserves existing content exactly,
    fixing only a missing trailing newline so appended lines never glue onto the
    last existing line.
    """
    existing = gitignore_file.read_text() if gitignore_file.exists() else ""
    parts = [existing]
    if existing and not existing.endswith("\n"):
        parts.append("\n")
    if existing:
        parts.append("\n")  # blank line separating from prior content
    parts.append(
        "# Generated redirect stubs (appended by scripts/lint_redirect_ignores.py)\n"
    )
    parts.append("".join(f"{entry}\n" for entry in entries))
    gitignore_file.write_text("".join(parts))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--redirects-file",
        type=Path,
        default=Path("_redirects.json"),
        help="Path to the JSON map of source name -> target URL",
    )
    parser.add_argument(
        "--gitignore-file",
        type=Path,
        default=Path(".gitignore"),
        help="Path to the .gitignore file to keep in sync",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate only; do not write. Exit non-zero if anything is out of sync.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    stubs = stub_names(args.redirects_file)
    if not stubs:
        return 0

    repo_root = args.gitignore_file.resolve().parent

    status = 0

    missing = unignored_stubs(stubs, repo_root)
    if missing:
        if args.check:
            print(
                "error: redirect stub(s) not gitignored: "
                f"{', '.join(missing)}. "
                "Run scripts/lint_redirect_ignores.py to fix.",
                file=sys.stderr,
            )
        else:
            append_entries(args.gitignore_file, sorted(missing))
            print(
                f"Added {len(missing)} redirect stub "
                f"entr{'y' if len(missing) == 1 else 'ies'} to "
                f"{args.gitignore_file}: {', '.join(sorted(missing))}. "
                "Review, `git add` it, and commit again.",
                file=sys.stderr,
            )
        status = 1

    tracked = tracked_stubs(stubs, repo_root)
    if tracked:
        print(
            f"error: redirect stub(s) are tracked by git: {', '.join(tracked)}. "
            "These are build artifacts and must not be committed. "
            f"Run `git rm --cached {' '.join(tracked)}` and commit the removal.",
            file=sys.stderr,
        )
        status = 1

    return status


if __name__ == "__main__":
    raise SystemExit(main())
