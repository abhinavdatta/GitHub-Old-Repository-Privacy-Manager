
import os
import sys
import requests
from datetime import datetime, timezone

# ---------------- CONFIGURATION ----------------
USERNAME = "abhinavdatta"
CUTOFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

# Never make your profile README repository private.
EXCLUDED_REPOS = {
    "abhinavdatta",
}

API = "https://api.github.com"
# ------------------------------------------------


def main():
    token = os.getenv("GITHUB_TOKEN")
    apply_changes = "--apply" in sys.argv

    if not token:
        print("ERROR: GITHUB_TOKEN environment variable is not set.")
        print("Set it to a GitHub token with permission to administer your repositories.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    old_repos = []
    page = 1

    print(f"Fetching repositories owned by {USERNAME}...")

    # Fetch every page of repositories owned by the authenticated user.
    while True:
        response = requests.get(
            f"{API}/user/repos",
            headers=headers,
            params={
                "visibility": "all",
                "affiliation": "owner",
                "per_page": 100,
                "page": page,
                "sort": "pushed",
                "direction": "desc",
            },
            timeout=30,
        )

        if not response.ok:
            print(f"GitHub API error ({response.status_code}): {response.text}")
            return

        repos = response.json()
        if not repos:
            break

        for repo in repos:
            # Only process repositories belonging to the configured account.
            if repo["owner"]["login"].lower() != USERNAME.lower():
                continue

            if repo["name"].lower() in {
                name.lower() for name in EXCLUDED_REPOS
            }:
                continue

            # Avoid accidentally changing repositories already private.
            if repo["private"]:
                continue

            # Repositories without a push date are not automatically changed.
            pushed_at = repo.get("pushed_at")
            if not pushed_at:
                continue

            pushed_date = datetime.fromisoformat(
                pushed_at.replace("Z", "+00:00")
            )

            # Strictly BEFORE 1 January 2024 UTC.
            if pushed_date < CUTOFF:
                old_repos.append(repo)

        page += 1

    print("\nRepositories matching the cutoff:")
    print("-" * 75)

    if not old_repos:
        print("No public repositories matched the cutoff.")
        return

    for index, repo in enumerate(old_repos, start=1):
        print(
            f"{index:>3}. {repo['full_name']:<40} "
            f"Last push: {repo['pushed_at'][:10]}"
        )

    print("-" * 75)
    print(f"Total repositories to make private: {len(old_repos)}")

    if not apply_changes:
        print("\nPREVIEW ONLY: No repositories were changed.")
        print("Review the list, then run:")
        print("  py github_private_old_repos.py --apply")
        return

    print(
        "\nWARNING: This will change the listed public repositories to PRIVATE."
    )
    confirmation = input('Type PRIVATE to confirm: ').strip()

    if confirmation != "PRIVATE":
        print("Cancelled. No changes were made.")
        return

    successful = 0
    failed = 0

    for repo in old_repos:
        url = f"{API}/repos/{repo['full_name']}"

        response = requests.patch(
            url,
            headers=headers,
            json={"private": True},
            timeout=30,
        )

        if response.ok:
            print(f"[OK] Made private: {repo['full_name']}")
            successful += 1
        else:
            print(
                f"[FAILED] {repo['full_name']}: "
                f"{response.status_code} {response.text}"
            )
            failed += 1

    print("\nFinished.")
    print(f"Successfully made private: {successful}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
