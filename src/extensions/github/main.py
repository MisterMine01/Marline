
import os
import uuid

if 'is_extension' not in globals():
    from src.packages.extension.extension import Extension
    from packages.cache import Cache
    from packages.config import Config
    from ...packages.server import Client


class Github(Extension):
    cache_data: dict
    cache_name: str = "github"

    variables = {
        "url": "${GITHUB_SERVER_URL}${GITHUB_REPOSITORY}.git",
        "name": "${GITHUB_REPOSITORY_ID}",
        "branch": "${GITHUB_BASE_REF}"
    }

    def __init__(self, cache: Cache, config: Config) -> None:
        super().__init__(cache, config)
        self.cache_data = self.cache.get(self.cache_name) or {}
        self.command = {
            "update": self.github,
        }

    def github(self, client: Client) -> dict:
        """Update repository."""
        name = client.variables["github.name"]
        branch = client.variables["github.branch"]
        result = self.git(name, branch)
        if not result["ok"]:
            result = self.start_git(name, client.variables["github.url"],
                                    branch)
            if not result["ok"]:
                return result
            result = self.git(name, branch)
            if not result["ok"]:
                return result
        return result

    def clone(self, repository_name: str, uuid: str, url: str) -> dict:
        """Clone a repository."""
        path = os.path.join(self.config["git_folder"], repository_name, uuid)
        command = f"git clone {url} {path}"
        result = os.system(command)
        if result == 0:
            # get last commit
            command = f"git -C {path} log -1 --pretty=format:%H"
            return {"ok": True, "commit": os.popen(command).read()}
        else:
            return {"ok": False}

    def pull(self, repository_name: str, uuid: str) -> dict:
        """Pull a repository."""
        path = os.path.join(self.config["git_folder"], repository_name, uuid)
        command = f"git -C {path} pull"
        result = os.system(command)
        if result == 0:
            # get last commit
            command = f"git -C {path} log -1 --pretty=format:%H"
            return {"ok": True, "commit": os.popen(command).read()}
        else:
            return {"ok": False}

    def checkout(self, repository_name: str, uuid: str, branch: str) -> dict:
        """Checkout a branch."""
        path = os.path.join(self.config["git_folder"], repository_name, uuid)
        command = f"git -C {path} checkout {branch}"
        result = os.system(command)
        if result == 0:
            # get last commit
            command = f"git -C {path} log -1 --pretty=format:%H"
            return {"ok": True, "commit": os.popen(command).read()}
        else:
            return {"ok": False}

    def start_git(self, repository_name: str, url: str, branch: str) -> dict:
        """Start a git repository."""
        if repository_name not in self.cache_data["repo"]:
            self.cache_data["repo"][repository_name] = {
                "url": url,
                "branches": {}
            }
        identifier = str(uuid.uuid4())
        result = self.clone(repository_name, identifier, url)
        if not result["ok"]:
            return result
        result = self.checkout(repository_name, identifier, branch)
        if not result["ok"]:
            return result

        self.cache_data["repo"][repository_name]["branches"][branch] = {
            "uuid": identifier,
            "commit": result["commit"]
        }
        self.cache.set(self.cache_name, self.cache_data)
        return {"ok": True}

    def git(self, repository_name: str, branch: str) -> dict:
        """Get the last commit of a branch."""
        if repository_name not in self.cache_data["repo"]:
            return {"ok": False, "use": "start_git"}
        if branch not in self.cache_data["repo"][repository_name]["branches"]:
            return {"ok": False, "use": "start_git"}
        identifier = self.cache_data["repo"][repository_name]["branches"][branch]["uuid"]

        result = self.pull(repository_name, identifier)
        if not result["ok"]:
            return result
        self.cache_data["repo"][repository_name]["branches"][branch]["commit"] = result["commit"]
        self.cache.set(self.cache_name, self.cache_data)
        return {"ok": True, "commit": result["commit"]}


if 'is_extension' in globals():
    __extension__ = {
        "class": Github,
        "name": "github"
    }
