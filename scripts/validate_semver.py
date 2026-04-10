import sys
import re

def parse_version(v):
    return [int(x) for x in re.findall(r'\d+', v)]

def validate():
    try:
        old_v = parse_version(sys.argv[1])
        new_v = parse_version(sys.argv[2])
    except Exception:
        sys.exit(1)

    # Compare SemVer tuple (major, minor, patch)
    if new_v > old_v:
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    validate()
