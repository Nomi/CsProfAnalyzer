import sys
from .strings import STRINGS as STR, C_YELLOW, C_RESET


def validate_dependencies() -> None:
    required = ["pandas", "numpy", "tqdm", "colorama"]
    missing = [
        pkg for pkg in required if not __import__("importlib").util.find_spec(pkg)
    ]
    if missing:
        pkgs = ", ".join(missing)
        print(STR.MSG_MISSING_DEPS.format(pkg_list=pkgs))
        print(STR.MSG_INSTALL)
        print(STR.MSG_PIP.format(pkg_list=pkgs))
        sys.exit(1)


def show_help_glossary() -> None:
    print(STR.SECTION_GLOSSARY)
    for k, v in STR.GLOSSARY_MAP.items():
        print(f"{C_YELLOW}{k:18}{C_RESET}: {v}")
    print("-" * 50)
