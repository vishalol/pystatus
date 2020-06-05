import argparse
from github import Github

GITHUB_TOKEN = "add_your_token"


class GithubClient:
    client = None
    repo = None

    def __init__(self, repository):
        self.client = Github(GITHUB_TOKEN)
        self.repo = self.client.get_repo(repository)

    def post_status(self, commit_sha):
        res = self.repo.get_commit(sha=commit_sha).create_status(
            state="success",
            target_url="https://FooCI.com",
            description="FooCI is building",
            context="ci/FooCI",
        )
        print("successfully posted")
        print(res)

    def get_status(self, commit_sha):
        response = self.repo.get_commit(sha=commit_sha).get_combined_status()
        print(response)


if __name__ == "__main__":

    argparser = argparse.ArgumentParser(add_help=False)
    argparser.add_argument("--sha", required=True, help="SHA of the commit")
    argparser.add_argument(
        "--repo", required=True, help="Name of the repo: username/repository"
    )
    argparser.add_argument(
        "--get", required=False, default=False, help="set true if get"
    )

    args = argparser.parse_args()
    commit_sha, repository, get = args.sha, args.repo, args.get

    client = GithubClient(repository)

    if get:
        client.get_status(commit_sha)
    else:
        client.post_status(commit_sha)
