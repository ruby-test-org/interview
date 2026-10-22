# interview

Fetch merged pull request data from a GitHub repository:

```sh
python3 fetch_pr_data.py owner/repo
```

it paginates through closed PRs, outputs merged PRs as JSON, and optionally uses `GITHUB_TOKEN` or `GH_TOKEN`. It uses Python’s standard library, so it doesn’t require `requests`. For
authenticated API access, set `GITHUB_TOKEN` or `GH_TOKEN` before running it.
