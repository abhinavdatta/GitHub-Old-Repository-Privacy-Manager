# GitHub Old Repository Privacy Manager

A Python script that identifies older public GitHub repositories and optionally makes them private based on their last push date.

## Features

- Finds public repositories last pushed before the configured cutoff date.
- Previews matching repositories before making changes.
- Requires explicit confirmation before changing visibility.
- Uses GitHub's official REST API.

## Requirements

- Python 3
- A GitHub Personal Access Token with **Administration: Read and write** and **Metadata: Read-only** repository permissions.
- The `requests` package.

## Setup

Install the dependency:

```powershell
py -m pip install requests
```

Set your GitHub token in PowerShell:

```powershell
$env:GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
```

## Customize the Cutoff Date

Open `github_private_old_repos.py` and find this line near the top:

```python
CUTOFF = datetime(2024, 1, 1, tzinfo=timezone.utc)
```

Change `2024, 1, 1` to your desired date in **year, month, day** format.

For example, to use January 1, 2025:

```python
CUTOFF = datetime(2025, 1, 1, tzinfo=timezone.utc)
```

Save the file and run the script again.

The script selects public repositories whose last push occurred **before** the specified cutoff date. The date is interpreted in UTC.

## Usage

**1. Preview — no changes are made**

```powershell
py github_private_old_repos.py
```

**2. Apply changes**

```powershell
py github_private_old_repos.py --apply
```

Review the repository list and type `PRIVATE` when prompted to confirm.

## Important

- Uses the **last push date**, not the repository creation date.
- Excludes the `abhinavdatta` repository by default. Change `EXCLUDED_REPOS` in the Python script if needed.
- Making a repository private can affect public links, GitHub Pages, collaborators, and integrations.
- Never publish your access token.

## License

Choose a license before redistributing this project. See [Choose a License](https://choosealicense.com/).