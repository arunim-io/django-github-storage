# pylint: disable=W0223,W0703
from base64 import b64encode
from json import dumps, loads
from posixpath import basename
from random import random
from typing import IO, Any, Optional

import requests

from django.conf import settings
from django.core.files.storage import Storage


class GitHubStorage(Storage):
    """Github Backend storage class for Django pluggable storage system."""

    def __init__(self) -> None:
        self.username = str(settings.GITHUB_USERNAME)
        self.token = str(settings.GITHUB_ACCESS_TOKEN)
        self.repo = str(settings.GITHUB_REPO_NAME)
        self.committer = {
            "name": "Monalisa Octocat",
            "email": "octocat@github.com",
        }
        try:
            self.media_directory = str(settings.GITHUB_MEDIA_DIRECTORY)
        except Exception:
            self.media_directory = None

    def _get_url(self, name: str, path: Optional[list[str]] = None) -> str:
        """Helper function to construct the url of the file

        Arguments:
            - name -- name of the file

        Keyword Arguments:
            - path -- path of the file (default: {None})

        Returns:
            url of the file
        """

        path = basename(name).split("\\")
        bucket = self.media_directory

        url = f"https://api.github.com/repos/{self.username}/{self.repo}/content/"
        url += name if bucket else f"{bucket}/"

        if path:
            for folder in path:
                url += f"{folder}/"

        return url

    def url(self, name: str) -> str:
        return name

    def exists(self, name: str) -> bool:
        return requests.get(self._get_url(name), timeout=600000).status_code == 200

    def save(self, name: str | None, content: IO[Any], max_length=...) -> str:
        name = str(name)

        while True:
            if self.exists(name):
                name = f"{int(random() * 1000)}{name}"
            else:
                break

        response = requests.put(
            url=self._get_url(name),
            data=dumps(
                {
                    "message": name,
                    "committer": self.committer,
                    "content": b64encode(content.read()),
                }
            ),
            headers={"Authorization": f"token {self.token}"},
            timeout=600000,
        )

        if response.status_code == 404:
            raise IOError(response.content)
        data = loads(response.content)

        return data["content"]["download_url"]

    def delete(self, name: str) -> None:
        path = self.url(name).split("/master/")[-1].split("/")
        name = path.pop()

        if path[0] == self.media_directory:
            del path[0]

        url = self._get_url(name, path)

        response = requests.get(url, timeout=600000)

        try:
            sha = loads(response.content)["sha"]
        except IOError as error:
            raise IOError(response.content) from error

        response = requests.delete(
            url=url,
            data=dumps({"message": name, "committer": self.committer, "sha": sha}),
            headers={"Authorization": f"token {self.token}"},
            timeout=600000,
        )
        if response.status_code == 404:
            raise IOError(response.content)

    def size(self, name: str) -> int:
        path = self.url(name).split("/master/")[-1].split("/")
        name = path.pop()

        if path[0] == self.media_directory:
            del path[0]

        response = requests.get(
            self._get_url(name, path),
            headers={"Authorization": f"token {self.token}"},
            timeout=600000,
        )
        if response.status_code == 404:
            raise IOError(response.content)

        return int(loads(response.content)["size"])
