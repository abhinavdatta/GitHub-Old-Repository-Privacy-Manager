# GitHub Old Repository Privacy Manager

## Documentation and User Guide

**Script:** `github_private_old_repos.py`
**Platform:** Windows 10/11 with PowerShell
**Language:** Python 3
**Purpose:** Find old public GitHub repositories and optionally change their visibility to private.

---

## 1. Overview

The GitHub Old Repository Privacy Manager is a Python script designed to help clean up a GitHub account by making older public repositories private.

It communicates with GitHub through the official GitHub REST API. It does not scrape GitHub pages, delete repositories, or modify repository files.

The script uses a cutoff date of **1 January 2024**. A public repository is selected when its most recent push occurred strictly before midnight UTC on that date.

### Main features

- Retrieves repositories owned by the authenticated GitHub account.
- Checks repository visibility and last-push dates.
- Identifies public repositories that match the cutoff.
- Excludes repositories named `abhinavdatta` by default.
- Displays a preview without changing anything.
- Requires an explicit `--apply` option and confirmation before making repositories private.
- Reports successful changes and API errors.

## 2. How the script works

The script follows this sequence:

1. Reads the `GITHUB_TOKEN` environment variable.
2. Connects to the GitHub REST API.
3. Retrieves owned repositories in pages of up to 100 repositories.
4. Skips repositories that do not belong to the configured username.
5. Skips the excluded repository name and repositories that are already private.
6. Skips repositories without a recorded push date.
7. Compares the last-push date against the cutoff.
8. Displays matching repositories and their dates.
9. If `--apply` is supplied, asks for the confirmation word `PRIVATE`.
10. Sends an API request to change each matching repository's visibility to private.
11. Prints a summary of successful and failed changes.

### Date cutoff

The configured cutoff is:

`2024-01-01 00:00:00 UTC`

| Last push date              | Result       |
| --------------------------- | ------------ |
| 31 December 2023            | Selected     |
| 1 January 2024 at 00:00 UTC | Not selected |
| Any date after the cutoff   | Not selected |
| No recorded push date       | Skipped      |
| Repository already private  | Skipped      |

**Important:** The script checks the last push date, not the repository creation date, last commit date, or last time its README was edited. These dates can differ.

## 3. Requirements

Before running the script, ensure you have:

- A Windows computer with PowerShell.
- Python 3 installed and accessible through the `py` command.
- Internet access.
- A GitHub account with administrative permission for the repositories you intend to change.
- A GitHub personal access token with the necessary permissions.
- The Python `requests` package.

Check Python:

```powershell
py --version
```

Install the dependency:

```powershell
py -m pip install requests
```

## 4. Create a GitHub access token

The script needs permission to read repositories and change their visibility.

1. Open the [GitHub personal access token settings](https://github.com/settings/personal-access-tokens).

2. Create a fine-grained personal access token.

3. Select `abhinavdatta` as the resource owner.

4. Select all repositories or only the repositories you want the token to manage.

5. Configure these repository permissions:

   - **Administration:** Read and write
   - **Metadata:** Read-only

6. Set a suitable expiration date.

7. Generate the token and copy it securely.

The exact permissions and available repository selections depend on your GitHub account and organization policies.

**Security:** Never publish your token in a repository, source file, screenshot, or public message. Anyone who obtains a sufficiently privileged token may be able to change your repositories.

## 5. Configure the token in PowerShell

Open PowerShell in the directory containing `github_private_old_repos.py`.

For example:

```powershell
cd "C:\Users\abhi0\Desktop\New folder (2)\abhinavdatta-main"
```

Set the token for the current PowerShell session:

```powershell
$env:GITHUB_TOKEN = "YOUR_ACTUAL_GITHUB_TOKEN"
```

Replace the placeholder with your token.

This environment variable is temporary. Closing the PowerShell window removes it from that session.

You can check whether the variable is present without displaying its value:

```powershell
if ($env:GITHUB_TOKEN) {
    "GitHub token is configured."
} else {
    "GitHub token is missing."
}
```

## 6. Preview the repositories

Run the script without any additional argument:

```powershell
py github_private_old_repos.py
```

The script lists repositories that match the cutoff and shows their last-push dates.

Example output:

```text
Fetching repositories owned by abhinavdatta...

Repositories matching the cutoff:
---------------------------------------------------------------------------
  1. abhinavdatta/old-project       Last push: 2023-08-12
  2. abhinavdatta/college-project   Last push: 2023-11-04
---------------------------------------------------------------------------
Total repositories to make private: 2

PREVIEW ONLY: No repositories were changed.
Review the list, then run:
  py github_private_old_repos.py --apply
```

The names above are illustrative examples, not actual results from your account.

**The preview mode does not change repository visibility.** Always review the list before proceeding.

## 7. Make the selected repositories private

When you are satisfied with the preview, run:

```powershell
py github_private_old_repos.py --apply
```

The script displays a warning and asks for confirmation:

```text
WARNING: This will change the listed public repositories to PRIVATE.
Type PRIVATE to confirm:
```

Type:

```text
PRIVATE
```

The script then processes the selected repositories individually.

If a repository is updated successfully, it prints an `[OK]` message. If GitHub rejects an update, the script prints a `[FAILED]` message with the associated API response.

At the end, it reports the number of successful changes and failures.

Do not assume that every repository was changed successfully just because the script finished. Review the final summary and verify the affected repositories on GitHub.

## 8. What changes when a repository becomes private?

Making a repository private changes who can access its contents.

| Item                         | Effect                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------ |
| Repository code and files    | No longer publicly accessible                                                        |
| Public repository URL        | May no longer be accessible to people without permission                             |
| Existing collaborators       | Access depends on retained permissions and account settings                          |
| GitHub Pages                 | Public site availability or behavior may change, depending on configuration and plan |
| External integrations        | May need additional permissions or configuration                                     |
| Local clone on your computer | Remains on your computer; changing visibility does not delete it                     |
| Repository history           | Remains in the repository                                                            |
| Repository itself            | Is not deleted                                                                       |

Before changing visibility, review repositories used for demonstrations, deployed sites, coursework submissions, open-source projects, or external integrations.

## 9. How to restore public visibility

If you make a repository private by mistake, you can usually restore its public visibility if your account and repository settings permit it.

### Using GitHub's website

1. Open the private repository.
2. Open **Settings**.
3. Locate the repository visibility or danger-zone settings.
4. Choose the option to change visibility to public.
5. Read GitHub's warnings and confirm the change.

GitHub may require additional confirmation or impose restrictions based on repository ownership and organization policies.

### Using the REST API

The same API endpoint used by the script supports changing visibility:

```http
PATCH /repos/OWNER/REPOSITORY
```

To request public visibility, the JSON body is:

```json
{
  "private": false
}
```

This is an alternative recovery method, not a command executed by the supplied script. The script itself only changes matching public repositories to private.

## 10. Common errors and troubleshooting

### Error: `GITHUB_TOKEN environment variable is not set`

**Cause:** The token has not been configured in the current PowerShell session.

**Solution:**

```powershell
$env:GITHUB_TOKEN = "YOUR_ACTUAL_GITHUB_TOKEN"
```

Then rerun the script.

### Error: HTTP 401 Unauthorized

**Possible causes:**

- The token is invalid.
- The token has expired or been revoked.
- The token was copied incorrectly.

Create or configure a valid token and try again.

### Error: HTTP 403 Forbidden

**Possible causes:**

- The token lacks the required permissions.
- Organization policies restrict the operation.
- The API rate limit has been reached.

Review token permissions and organization policies. If rate-limited, wait before retrying.

### Error: HTTP 404 Not Found

The repository may not be accessible to the token, may have been deleted or transferred, or may not be available at the requested API path. Check the repository name and access permissions.

### Some repositories do not appear in the list

Check the following:

- Is the repository owned by the authenticated account?
- Is it already private?
- Was its last push before the cutoff?
- Does it have a recorded push date?
- Is its name in the exclusion list?
- Does the token have access to the repository?

The script does not select repositories solely because they were created before 2024.

## 11. Important limitations

The current version of the script:

- Uses a fixed username and cutoff date in its configuration.
- Uses the last-push date as its selection criterion.
- Excludes repositories by name, not by checking whether they contain a profile README.
- Skips repositories already private.
- Does not delete, archive, transfer, or rename repositories.
- Does not automatically restore visibility if a later update fails.
- Does not perform a separate verification request after each successful update.
- Does not create a backup of repository settings or contents.

For additional safety, retain a copy of the preview output and verify the final visibility of repositories on GitHub.

## 12. Recommended operating procedure

Use the following checklist whenever you run the script:

- [ ] Confirm that the script contains the intended username and cutoff date.
- [ ] Confirm that the profile repository exclusion is correct.
- [ ] Configure a valid GitHub token securely.
- [ ] Run preview mode first.
- [ ] Review every repository in the preview.
- [ ] Check whether any selected project needs to remain public.
- [ ] Run with `--apply` only after reviewing the list.
- [ ] Type `PRIVATE` only when you intend to proceed.
- [ ] Review the success and failure counts.
- [ ] Verify the repository visibility on GitHub.
- [ ] Remove or rotate the token if it is exposed or no longer needed.

---

## 13. Official references

- [List repositories for the authenticated user](https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user)
- [Update a repository](https://docs.github.com/en/rest/repos/repos#update-a-repository)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

**Final note:** The script is intended to help manage repository visibility safely. Preview first, verify the target list, and make changes only after explicit confirmation.
