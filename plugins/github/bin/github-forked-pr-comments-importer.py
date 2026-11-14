#!/usr/bin/env python3
"""Import forked-pull-request comments into its dedicated context directory."""
import _gh


if __name__ == "__main__":
    _gh.import_pr_comments("github-forked-pr-comments-importer", "github.forked_pull_request", "forked-pull-request")
