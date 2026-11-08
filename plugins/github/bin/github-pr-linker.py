#!/usr/bin/env python3
"""github-pr-linker: finds the pull request of the Work's current branch.

  stdin  {"inputs": {"worktree_path": "<abs>"}}
  stdout {"value": "<pull request url>"} or {} when the branch has no pull request

Asks `gh pr view` from inside the worktree, so the answer follows whatever
repository and branch the Work checked out. No pull request is not an error.
"""
import json
import sys

import _gh

NAME = "github-pr-linker"


def main():
    worktree = _gh.read_stdin(NAME).get("inputs", {}).get("worktree_path")
    if not worktree:
        _gh.fail(NAME, "missing input: worktree_path")

    proc = _gh.gh_in(worktree, ["pr", "view", "--json", "url"])
    if proc is None:
        _gh.fail(NAME, "gh not found on PATH")
    if proc.returncode != 0:
        if "no pull requests found" in proc.stderr.lower():
            print("{}")
            return
        _gh.fail(NAME, f"gh pr view failed: {proc.stderr.strip() or proc.returncode}")

    url = json.loads(proc.stdout).get("url")
    json.dump({"value": url} if url else {}, sys.stdout)
    print()


if __name__ == "__main__":
    main()
