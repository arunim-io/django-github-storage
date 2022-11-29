# django-github-storage

![PyPI - License](https://img.shields.io/pypi/l/django-github-storages?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/arunim-io/django-github-storage?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/django-github-storages?style=flat-square)
![PyPI - Status](https://img.shields.io/pypi/status/django-github-storages?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-github-storages?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-github-storages?style=flat-square)

> A Django file storage backend that leverages GitHub.

**Note**: It currently works only for media files. Support for static files will soon be added.

## Requirements

- Python 3.6+
- Django 3.2, 4.0, 4.1

It is highly recommended to use the latest versions of Python and Django if possible.

## Installation

1. Install the package in 2 ways.

   - Using poetry:

   ```console
   poetry add django-github-storages
   ```

   - Using pip:

   ```console
   pip install django-github-storages
   ```

2. Include the package in the `INSTALLED_APPS` dict in your `<project-dir>/settings.py`.

```python
INSTALLED_APPS = [
    # other apps...
    'github_storage',
]

```

3. Set the following settings:

```python
DEFAULT_FILE_STORAGE = "github_storage.backend.BackendStorage"

GITHUB_USERNAME = ""
GITHUB_ACCESS_TOKEN = ""
GITHUB_REPO_NAME = ""
GITHUB_MEDIA_DIRECTORY = ""

```

## Reference

| Settings               | Description                                                                                                                      | Required | Example                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------ |
| GITHUB_USERNAME        | Your GitHub Username                                                                                                             | ✅       | 'arunim-io'              |
| GITHUB_ACCESS_TOKEN    | Your GitHub access token (Used for accessing the files). [Click here to get one](#getting-a-access-token-from-github).           | ✅       | '\*\*\*\*\*\*\*\*\*\*\*' |
| GITHUB_REPO_NAME       | The name of the repository that will be used for storing.(**Warning**: it must be public or else GitHub won't accept any files.) | ✅       | 'backend-files'          |
| GITHUB_MEDIA_DIRECTORY | The directory inside the repo                                                                                                    | ❌       | 'media'                  |

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2022 [Mugdha Arunim Ahmed](https://github.com/arunim-io).<br />
This project is [BSD-3-Clause](https://github.com/arunim-io/django-github-storage/blob/main/LICENSE) licensed.
