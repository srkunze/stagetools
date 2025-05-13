# STAGETOOLS

## Why do you need stagetools?

stagetools is a production-ready staging and structuring framework.

You can use it to standardize your Django installations, but it also works
for flask or starlette.
This also helps during deployment.

It is slightly opinionated to start fast and easy.

There is no need to use all parts of stagetools.
You can also pick only what you need.


## Usage, conventions and `aaa`

To Django, `project` means top-level container (i.e. settings, bracket around apps) and
`app` is a single purpose code part like a plugin or extension.

stagetools expects the Django project to be called `stagetools_project`, and expects
`aaa_env_setup.py` and `aaa_script_setup.py` as top-level importable modules.

If you fulfill these requirements, stagetools will be able to provide:
- `manage.py`
- `asgi.py`
- `wsgi.py`
- `settings_defaults.py`
- `settings_defaults_with_postgresql.py`

`aaa` modules should be placed before all other Django-related modules in the import section.
The prefix `aaa` is used to ensure that when sorting imports alphabetically;


## Integration with ideploy

You can symlink/clone `repo/stagetools/` to your ideploy folder in order to have available:
- `get_expected_system_from_name`
- `get_actual_system_from_name`

The expected system can be used to construct/deploy a new system whereas the actual system
can be used to check whether the expected one was constructed correctly.

Usually, `system.core_repo` and `system.core_app` are inferred from the non-staging part of
the name of the installation.
You can, however, override by specifying `core_repo` and/or `core_app`.


## Example Django installation

This is a usual stagetools Django installation.

This example uses a mono-repo to illustrate the usage of stagetools:

``` shell
~$ find djangoproject/

repo/
repo/setup.py                         # allow installation via pip
repo/stagetools/...                   # stagetools clone (git subtree)

repo/aaa_env_setup.py                 # to be imported by asgi.py, wsgi.py, manage.py
repo/aaa_script_setup.py              # to be imported by console scripts (e.g.cronjob scripts, systemd scripts)

repo/stagetools_project/settings.py   # regular Django settings file
repo/stagetools_project/...           # remainder of Django project

repo/...                              # the remainder of your project's code
repo/app1/...                         # an additional app (git subtree)
repo/app2/...                         # an additional app (git subtree)
```


#### repo/aaa_env_setup.py

```python
import os

from stagetools.utils import get_actual_system_from_name

SYSTEM = get_actual_system_from_name()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', SYSTEM.django_settings)
```


#### repo/aaa_script_setup.py

```python
# noinspection PyUnresolvedReferences
import aaa_env_setup
import django

django.setup()
```


#### repo/stagetools_project/settings.py

```python
# noinspection PyUnresolvedReferences
from stagetools.settings_defaults import *

# other settings ...
```
