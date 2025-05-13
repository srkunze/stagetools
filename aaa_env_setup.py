import os

from stagetools.utils import get_actual_system_from_name

SYSTEM = get_actual_system_from_name(core_repo='myproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', SYSTEM.django_settings)
