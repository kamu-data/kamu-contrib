import json
import os
import requests
import time
import random
import sys
import argparse


per_page = int(os.environ.get("GH_PER_PAGE", "100"))
retries = int(os.environ.get("GH_RETRIES", "3"))
back_off = int(os.environ.get("GH_BACK_OFF", "10"))


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def list_repos(token, orgs):
    repos = []

    for org in orgs:
        page = 1
        while True:
            resp = requests.get(
                f"https://api.github.com/orgs/{org}/repos?per_page={per_page}&page={page}",
                headers={
                    "X-GitHub-Api-Version": "2022-11-28",
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {token}",
                }
            )

            resp.raise_for_status()
            repos_page = resp.json()
            repos.extend(repos_page)

            page += 1
            if len(repos_page) < per_page:
                break
    
    return repos


def repo_alias(repo):
    return repo["owner"]["login"] + "/" + repo["name"]


def views(token, repo):
    repo_name = repo["name"]
    owner = repo["owner"]["login"]
    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/traffic/views",
        headers={
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        }
    )

    resp.raise_for_status()
    resp = resp.json()

    for record in resp["views"]:
        print(json.dumps({
            "owner_id": repo["owner"]["id"],
            "owner_login": repo["owner"]["login"],
            "repo_id": repo["id"],
            "repo_name": repo["name"],
            "timestamp": record["timestamp"],
            "count": record["count"],
            "uniques": record["uniques"],
        }))


def clones(token, repo):
    repo_name = repo["name"]
    owner = repo["owner"]["login"]
    resp = requests.get(
        f"https://api.github.com/repos/{owner}/{repo_name}/traffic/clones",
        headers={
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        }
    )

    resp.raise_for_status()
    resp = resp.json()

    for record in resp["clones"]:
        print(json.dumps({
            "owner_id": repo["owner"]["id"],
            "owner_login": repo["owner"]["login"],
            "repo_id": repo["id"],
            "repo_name": repo["name"],
            "timestamp": record["timestamp"],
            "count": record["count"],
            "uniques": record["uniques"],
        }))


def stargazers(token, repo):
    page = 1
    retries_left = retries
    while True:
        repo_name = repo["name"]
        owner = repo["owner"]["login"]
        resp = requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}/stargazers?per_page={per_page}&page={page}",
            headers={
                "X-GitHub-Api-Version": "2022-11-28",
                "Accept": "application/vnd.github.star+json",
                "Authorization": f"Bearer {token}",
            }
        )

        # Handle rate limiting by backing off
        if retries_left > 0 and (resp.status_code == 429 or (resp.status_code == 403 and "rate limit" in resp.reason)):
            retries_left -= 1
            sleep = random.random() * back_off
            log(f"Backing off for {sleep} seconds due to rate limiting\nresponse headers: {resp.headers}")
            time.sleep(sleep)
            continue

        resp.raise_for_status()
        records = resp.json()

        for record in records:
            print(json.dumps({
                "owner_id": repo["owner"]["id"],
                "owner_login": repo["owner"]["login"],
                "repo_id": repo["id"],
                "repo_name": repo["name"],
                "starred_at": record["starred_at"],
                "user_id": record["user"]["id"],
                "user_login": record["user"]["login"],
            }))

        page += 1
        if len(records) < per_page:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--access-token', default=os.environ.get("GH_TOKEN"))
    parser.add_argument('--owner', action='append', required=True)
    subparsers = parser.add_subparsers(dest='cmd', required=True)
    parser_stars = subparsers.add_parser('stargazers')
    parser_views = subparsers.add_parser('views')
    parser_clones = subparsers.add_parser('clones')

    args = parser.parse_args()
    log("Parsed args:", args)

    repos = list_repos(args.access_token, args.owner)
    repos = [
        r for r in repos
        if not r["fork"] and not r["private"] and not r["archived"]
    ]
    repos.sort(key=lambda r: repo_alias(r))
    log("Listed repos:", [repo_alias(r) for r in repos])

    if args.cmd == 'views':
        for repo in repos:
            views(args.access_token, repo)
    elif args.cmd == 'clones':
        for repo in repos:
            clones(args.access_token, repo)
    elif args.cmd == 'stargazers':
        for repo in repos:
            stargazers(args.access_token, repo)
