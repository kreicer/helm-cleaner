from pyhelm.tiller import Tiller
from datetime import datetime, timezone, timedelta
import argparse

# List of exceptions
exceptions = ['']

# Number of days parsing, only 1 argument set, default number of days - 7
parser = argparse.ArgumentParser(description='Purge Helm releases')
parser.add_argument('-d', '--days', type=int, default=7, help='provide an integer (default: 7)')
parser.add_argument('--hostname', type=str, default='127.0.0.1', help='set the tiller host (default: 127.0.0.1)')
parser.add_argument('-p', '--purge', action='store_true', help='set this flag to purge releases')
args = parser.parse_args()

# Store number of days to variable
delete_days = args.days

# Get date to start helm releases rip marathon
dt = datetime.now() - timedelta(days=delete_days)

# Convert it into unix time format
# For Python 2: unix_time = int((dt - datetime(1970, 1, 1)).total_seconds())
unix_time = int(dt.replace(tzinfo=timezone.utc).timestamp())

# Make a exemplar of Tiller
host = args.hostname
tiller = Tiller(host=host)

# Get releases list
releases_list = tiller.list_releases()

# Empty dict for future "release": "deploy time" pairs
releases = {}

# Dirty magick
# Tiller give the list of releases with files, templates, etc

# Take each release from list
for release in releases_list:
    # Convert into string
    release = str(release)
    # Looking for name start position and end position, after - get name
    release_name_start = release.find("\"", 0, 7) + 1
    release_name_end = release.find("\"", 7)
    release_name = release[release_name_start:release_name_end]
    # Looking for last deploy start position and end position, after - get value in unix time
    last_deploy_start = release.find("last_deployed") + 29
    last_deploy_end = release.find("nanos", last_deploy_start) - 5
    last_deploy = release[last_deploy_start:last_deploy_end]
    # Add new key-value pair to dict
    releases[release_name] = last_deploy

# Remove releases with exceptions and releases where date of last deploy not in range
releases_copy = releases.copy()
for release_name in list(releases_copy):
    for exception in exceptions:
        if release_name.endswith(exception) or int(releases[release_name]) >= unix_time:
            del releases[release_name]
            break

# If purge flag don't set  - print list of releases for purge
if not args.purge:
    print('Next releases will be purged:')
    print(releases)

# If dict is empty - print message
elif len(releases) == 0:
    print('List of releases for purge is empty')

# If purge flag set - purge the releases
else:
    for release_name in releases:
        tiller.uninstall_release(release_name, False, True)
        print(release_name + ' was purged')
