# Fetch merged GitHub pull requests

This script fetches merged pull requests from a GitHub repository and prints
their data as JSON. It uses Python's standard library, so no packages need to
be installed.

## Requirements

- Python 3.6 or later
- Git
- Internet access to `api.github.com`

Check that Python and Git are available in your terminal:

```sh
python3 --version
git --version
```

## Download the script

Clone this repository and move into its directory:

```sh
git clone https://github.com/ruby-test-org/interview.git
cd interview
```

## Fetch merged pull requests

Pass the GitHub repository as `owner/repo` (not a full URL). For example:

```sh
python3 fetch_pr_data.py octocat/Hello-World
```

The JSON response is printed to the terminal. To save it to a file instead:

```sh
python3 fetch_pr_data.py octocat/Hello-World > merged-pull-requests.json
```

Replace `octocat/Hello-World` with the repository you want to query. Public
repositories can be queried without a token. For private repositories or a
higher GitHub API rate limit, set a token with access to the repository:

```sh
export GITHUB_TOKEN="your-github-token"
python3 fetch_pr_data.py owner/repo > merged-pull-requests.json
```

The script also recognizes the `GH_TOKEN` environment variable. It retries
GitHub API responses with status 429 or 5xx, honoring `Retry-After` when
provided.
