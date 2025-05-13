# MIT License
#
# Copyright (c) 2021 Sven R. Kunze
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import platform
import sys
from pathlib import Path

system_matcher = re.compile('(?P<configuration>.+)_(?P<stage_name>.+)').match

STAGE_DEV = 3
STAGE_INT = 2
STAGE_QUAL = 1
STAGE_PROD = 0
STAGES = [STAGE_DEV, STAGE_INT, STAGE_QUAL, STAGE_PROD]
DEBUG_STAGES = [STAGE_DEV, STAGE_INT]

STAGE_LETTER_TO_STAGE = {
    'p': STAGE_PROD,
    'q': STAGE_QUAL,
    'i': STAGE_INT,
    'd': STAGE_DEV,
}


class System(object):
    __slots__ = [
        'name',
        'user',
        'group',
        'container',

        'configuration',
        'stage_name',
        'stage',

        'core_repo',
        'core_app',
        'is_debug',

        'base_dir',
        'venv_dir',
        'bin_dir',
        'lib_dir',
        'src_dir',
        'python_path',
        'pip_path',
        'core_repo_dir',
        'static_url',
        'static_dir',
        'media_url',
        'media_dir',

        'application_name',
        'asgi_module',
        'asgi_application',
        'wsgi_module',
        'wsgi_application',

        'django_project',
        'django_application',
        'django_settings',
        'django_rooturls',
        'django_wsgi_application',
        'manage_py_path',

        'database_name',
        'database_user',
        'database_sqlite_path',

        'services',
    ]


def get_actual_system_from_name(name=None, core_repo=None, core_app=None):
    if platform.system() == 'Windows':
        if name:
            raise NotImplementedError
        else:
            pwentry = lambda: 0
            pwentry.pw_name = os.getlogin()
    else:
        import pwd
        if name:
            pwentry = pwd.getpwnam(name)
        else:
            pwentry = pwd.getpwuid(os.getuid())  # current user of process
    basedir = Path(sys.prefix)
    name = name or basedir.name  # usually we do NOT want to override the name given by the directory

    match = system_matcher(name)
    if not match:
        name = Path(__file__).parts[-5]
        match = system_matcher(name)
        basedir = Path(__file__).parents[3]
        if not match:
            raise RuntimeError(f'improperly configured - system_name {name!r} does not match system_naming convention')

    system = System()
    system.name = name
    system.user = pwentry.pw_name
    if platform.system() == 'Windows':
        system.group = ''
    else:
        import grp
        system.group = grp.getgrgid(pwentry.pw_gid).gr_name
    system.container = name.replace('_', '-')

    system.base_dir = basedir

    system.configuration, system.stage_name = match.groups()
    system.core_repo = core_repo or system.configuration
    system.core_app = core_app or system.core_repo
    _populate_derived_attributes(system)
    return system


def get_expected_system_from_name(name=None, base_dir=None, core_repo=None, core_app=None):
    if not name:
        if platform.system() == 'Windows':
            raise NotImplementedError
        else:
            import pwd
            pwentry = pwd.getpwuid(os.getuid())  # current user of process
            name = pwentry.pw_name  # here we still don't have sys.prefix available - fall back to login

    system = System()
    system.name = name
    system.user = name
    system.group = name
    system.container = name.replace('_', '-')

    system.base_dir = Path(base_dir) if base_dir else Path('/home') / name

    match = system_matcher(name)
    system.configuration, system.stage_name = match.groups()
    system.core_repo = core_repo or system.configuration
    system.core_app = core_app or system.core_repo
    _populate_derived_attributes(system)
    return system


def _populate_derived_attributes(system):
    system.stage = STAGE_LETTER_TO_STAGE[system.stage_name[0]]

    system.is_debug = system.stage in DEBUG_STAGES

    system.venv_dir = system.base_dir
    system.bin_dir = system.venv_dir / 'bin'
    system.lib_dir = system.venv_dir / 'lib'
    system.src_dir = system.venv_dir / 'src'
    system.python_path = system.bin_dir / 'python'
    system.pip_path = system.bin_dir / 'pip'
    system.core_repo_dir = system.src_dir / system.core_repo
    system.static_url = 'static/'  # https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    system.static_dir = system.base_dir / 'static'
    system.media_url = 'media/'  # https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    system.media_dir = system.base_dir / 'media'

    system.application_name = 'application'
    system.asgi_module = 'stagetools.asgi'
    system.asgi_application = system.asgi_module + ':' + system.application_name
    system.wsgi_module = 'stagetools.wsgi'
    system.wsgi_application = system.wsgi_module + ':' + system.application_name

    system.django_project = 'stagetools_project'
    system.django_wsgi_application = system.wsgi_module + '.' + system.application_name
    system.django_settings = system.django_project + '.settings'
    system.django_rooturls = system.django_project + '.urls'
    system.manage_py_path = system.core_repo_dir / 'stagetools/manage.py'

    system.database_name = system.configuration + '_' + system.stage_name
    system.database_user = system.database_name
    system.database_sqlite_path = system.venv_dir / f"{system.core_repo}.sqlite"
