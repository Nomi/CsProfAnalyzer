import sys
import re
from pathlib import Path

# Common blocklist pattern used across the project
BLOCKLIST_PATTERN = r'^(ReadMe\.md|\.gitignore|\.github/.*|\.git.*|tests/.*|CsProfAnalyzer\.spec)$'

def parse_version(v):
    return [int(x) for x in re.findall(r'\d+', v)]

def is_ignored(file_path):
    return re.match(BLOCKLIST_PATTERN, file_path) is not None

def validate_semver(old_v, new_v):
    try:
        old_tuple = parse_version(old_v)
        new_tuple = parse_version(new_v)
    except Exception:
        return False
    return new_tuple > old_tuple

if __name__ == "__main__":
    # If called with 'check', validate a file path against the blocklist
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        if is_ignored(sys.argv[2]):
            sys.exit(0) # Should be ignored
        sys.exit(1) # Should be validated
    
    # Otherwise perform SemVer comparison
    if validate_semver(sys.argv[1], sys.argv[2]):
        sys.exit(0)
    sys.exit(1)
