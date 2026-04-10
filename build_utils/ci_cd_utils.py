import sys
import re
from pathlib import Path

# Common blocklist pattern used across the project
BLOCKLIST_PATTERN = r'^(ReadMe\.md|\.gitignore|\.github/.*|\.git.*|tests/.*)$'

def parse_version_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([\d\.]+)["\']', content)
        if not match:
            raise ValueError(f"Could not find version in {file_path}")
        return [int(x) for x in match.group(1).split('.')]

def is_ignored(file_path):
    return re.match(BLOCKLIST_PATTERN, file_path) is not None

def validate_semver(old_file, new_file):
    try:
        old_tuple = parse_version_from_file(old_file)
        new_tuple = parse_version_from_file(new_file)
    except Exception:
        return False
    return new_tuple > old_tuple

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        if is_ignored(sys.argv[2]):
            sys.exit(0)
        sys.exit(1)
    
    # Perform SemVer comparison between two files
    if validate_semver(sys.argv[1], sys.argv[2]):
        sys.exit(0)
    sys.exit(1)
