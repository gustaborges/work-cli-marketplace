#!/usr/bin/env python3
"""Import pull-request description into its dedicated context directory."""
import _gh


if __name__ == "__main__":
    _gh.import_pr_description("github-pr-description-importer", "github.pull_request", "pull-request")
