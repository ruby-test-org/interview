import argparse
import json
import os
import re
import sys

import requests


API_URL = "https://api.github.com"
REQUEST_TIMEOUT = 30


def fetch_merged_pull_requests(repository, token=None):
    """Return all merged pull requests for an owner/repository."""
    if not re.fullmatch(r"[^/]+/[^/]+", repository):
        raise ValueError("Repository must be in the form owner/repo.")

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    url = f"{API_URL}/repos/{repository}/pulls"
    params = {"state": "closed", "per_page": 100}
    merged_pull_requests = []

    while url:
        response = requests.get(
            url, headers=headers, params=params, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        pull_requests = response.json()
        if not isinstance(pull_requests, list):
            raise ValueError("GitHub API returned an unexpected response.")

        merged_pull_requests.extend(
            pull_request
            for pull_request in pull_requests
            if pull_request.get("merged_at") is not None
        )
        url = response.links.get("next", {}).get("url")
        params = None

    return merged_pull_requests


def main():
    parser = argparse.ArgumentParser(
        description="Fetch merged pull request data from the GitHub API."
    )
    parser.add_argument("repository", help="GitHub repository in owner/repo format")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    try:
        pull_requests = fetch_merged_pull_requests(args.repository, token)
    except (requests.RequestException, ValueError) as error:
        print(f"Error fetching pull requests: {error}", file=sys.stderr)
        return 1

    json.dump(pull_requests, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
