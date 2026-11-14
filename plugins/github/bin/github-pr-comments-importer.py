#!/usr/bin/env python3
"""Import pull-request comments into its dedicated context directory."""
import _gh


if __name__ == "__main__":
    _gh.import_pr_comments("github-pr-comments-importer", "github.pull_request", "pull-request")
