import datetime
import sys
import os
import configparser


_settings = 'settings.ini'

# Configuration file loading
__config_parser = configparser.ConfigParser()
__config_parser.read(filenames=_settings)

# Current date loading
current_date = datetime.datetime.now()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day

# System detecting
current_platform = sys.platform
current_platform_prefix = current_platform[:3]

# Paths loading
projects_folder = __config_parser.get('PATHS', 'projects')
logs_folder = __config_parser.get('PATHS', 'logs')

# Date update
if(
    current_year != __config_parser.get('DATE', 'year') or
    current_month != __config_parser.get('DATE', 'month') or
    current_day != __config_parser.get('DATE', 'day')
   ):
    __config_parser.set('DATE', 'year', str(current_year))
    __config_parser.set('DATE', 'month', str(current_month))
    __config_parser.set('DATE', 'day', str(current_day))

# System platform update
if(__config_parser.get('SYSTEM', 'platform') != current_platform):
    __config_parser.set('SYSTEM', 'platform', current_platform)

# Save changes
with open(_settings, 'w') as settings_file:
    __config_parser.write(settings_file)
__config_parser.clear()
