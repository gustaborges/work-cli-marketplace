#!/usr/bin/env python3
"""Import pull-request diff into its dedicated context directory."""
import _gh


if __name__ == "__main__":
    _gh.import_pr_diff("github-pr-diff-importer", "github.pull_request", "pull-request")
