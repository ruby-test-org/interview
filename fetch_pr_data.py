import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.github.com"
REQUEST_TIMEOUT = 30
PER_PAGE = 100
MAX_RETRIES = 5
BACKOFF_BASE_SECONDS = 1
MAX_BACKOFF_SECONDS = 60


def retry_delay(retry_after, retry_number):
    """Return the server-provided delay or the exponential fallback."""
    if retry_after:
        try:
            return max(0, float(retry_after))
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(retry_after)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(0, (retry_at - datetime.now(timezone.utc)).total_seconds())
            except (TypeError, ValueError, OverflowError):
                pass

    return min(
        BACKOFF_BASE_SECONDS * (2 ** (retry_number - 1)),
        MAX_BACKOFF_SECONDS,
    )


def open_with_retries(request):
    retry_number = 0
    while True:
        try:
            return urlopen(request, timeout=REQUEST_TIMEOUT)
        except HTTPError as error:
            if error.code != 429 and not 500 <= error.code <= 599:
                raise
            if retry_number >= MAX_RETRIES:
                raise

            retry_number += 1
            delay = retry_delay(error.headers.get("Retry-After"), retry_number)
            error.close()
            time.sleep(delay)


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

    merged_pull_requests = []
    seen_pull_request_ids = set()
    page = 1

    while True:
        url = (
            f"{API_URL}/repos/{repository}/pulls"
            f"?state=closed&per_page={PER_PAGE}&page={page}"
        )
        request = Request(url, headers=headers)
        with open_with_retries(request) as response:
            pull_requests = json.load(response)
        if not isinstance(pull_requests, list):
            raise ValueError("GitHub API returned an unexpected response.")

        for pull_request in pull_requests:
            pull_request_id = pull_request["id"]
            if (
                pull_request.get("merged_at") is not None
                and pull_request_id not in seen_pull_request_ids
            ):
                merged_pull_requests.append(pull_request)
                seen_pull_request_ids.add(pull_request_id)

        if len(pull_requests) < PER_PAGE:
            break
        page += 1

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
    except (HTTPError, URLError, TimeoutError, ValueError) as error:
        print(f"Error fetching pull requests: {error}", file=sys.stderr)
        return 1

    json.dump(pull_requests, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
