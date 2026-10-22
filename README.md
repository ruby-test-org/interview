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

## Run with GitHub Actions

The **Fetch merged pull requests** workflow can also run manually in GitHub:

1. Open the repository's **Actions** tab.
2. Select **Fetch merged pull requests**, then choose **Run workflow**.
3. When the run completes, download the `merged-pull-requests` artifact from
   the run's summary page.

The workflow automatically uses the current repository and the built-in
`GITHUB_TOKEN`; no token secret needs to be configured.

### Download the artifact with GitHub CLI

Install and authenticate the [GitHub CLI](https://cli.github.com/) first:

```sh
gh auth login
```

List recent runs and copy the run ID from the output:

```sh
gh run list --workflow fetch-merged-prs.yml --limit 5
```

Download the artifact for that run into the current directory (replace
`RUN_ID` with the ID you copied):

```sh
gh run download RUN_ID \
  --repo ruby-test-org/interview \
  --name merged-pull-requests
```
