#!/usr/bin/env python3
# Python 3 implementation of 'has' script - checks for command availability
# Usage: python3 has.py git curl node

import os
import sys
import subprocess
import shutil
import re
from typing import Optional, List, Tuple

# Constants
BINARY_NAME = "has"
VERSION = "v2.0.0"

# Terminal colors
def setup_colors():
    if not sys.stdout.isatty():
        return {"reset": "", "bold": "", "red": "", "green": "", "yellow": ""}

    try:
        import curses
        curses.setupterm()

        # Function to output ESC sequence for color
        def color(code):
            return f"\033[{code}m"

        return {
            "reset": color(0),
            "bold": color(1),
            "red": color(31),
            "green": color(32),
            "yellow": color(33)
        }
    except Exception:
        return {"reset": "", "bold": "", "red": "", "green": "", "yellow": ""}

COLORS = setup_colors()

# Unicode symbols
CHECKMARK = "✓"
FANCYX = "✗"

# Decorated symbols
PASS = f"{COLORS['bold']}{COLORS['green']}{CHECKMARK}{COLORS['reset']}"
FAIL = f"{COLORS['bold']}{COLORS['red']}{FANCYX}{COLORS['reset']}"

# Output decorations
NAME_DECORATION = ""  # COLORS['bold']
VERSION_DECORATION = ""  # COLORS['green']
HELP_DECORATION = ""  # COLORS['yellow']

def show_help():
    """Display help message."""
    print(f"{HELP_DECORATION}{BINARY_NAME} - checks presence of various command line tools\n"
          f"usage:\n"
          f"  {BINARY_NAME} tool [tool]...\n\n"
          f"examples:\n"
          f"  {BINARY_NAME} git curl node\n"
          f"  {BINARY_NAME} -v\n"
          f"  {BINARY_NAME} --help{COLORS['reset']}")

def detect_command(cmd: str) -> bool:
    """
    Detect if a command exists and print its version if available.
    Returns True if command was found, False otherwise.
    """
    # Check if command exists using shutil.which
    if shutil.which(cmd):
        version = get_command_version(cmd)

        if version:
            # Remove redundant command name from version output
            # Common patterns: 'cmd version', 'cmd (details) version'
            pattern = f'^{re.escape(cmd)}\s*(\([^)]*\))?\s*'
            version = re.sub(pattern, '', version)

            # Truncate version if too long
            if version and len(version) > 50:
                version = version[:47] + "..."

            print(f"{PASS} {NAME_DECORATION}{cmd}{COLORS['reset']} {VERSION_DECORATION}{version}{COLORS['reset']}")
        else:
            # Command exists but no version info
            print(f"{PASS} {NAME_DECORATION}{cmd}{COLORS['reset']}")

        return True
    else:
        print(f"{FAIL} {NAME_DECORATION}{cmd}{COLORS['reset']} command not found")
        return False

def get_command_version(cmd: str) -> Optional[str]:
    """Try multiple methods to get command version."""
    version_flags = ["--version", "-version", "-v", "version", "-V"]

    # Special case for node
    if cmd == "node":
        try:
            result = subprocess.run(
                [cmd, "-e", "console.log(process.version)"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    # Special case for builtins like 'type' which are shell builtins
    if cmd in ['type', 'alias', 'bg', 'bind', 'break', 'builtin', 'caller', 'cd',
               'command', 'compgen', 'complete', 'continue', 'declare', 'dirs',
               'disown', 'echo', 'enable', 'eval', 'exec', 'exit', 'export', 'fc',
               'fg', 'getopts', 'hash', 'help', 'history', 'jobs', 'kill', 'let',
               'local', 'logout', 'mapfile', 'popd', 'printf', 'pushd', 'pwd',
               'read', 'readarray', 'readonly', 'return', 'set', 'shift', 'shopt',
               'source', 'suspend', 'test', 'times', 'trap', 'typeset', 'ulimit',
               'umask', 'unalias', 'unset', 'wait']:
        try:
            # Use 'bash -c' to check shell builtins
            result = subprocess.run(
                ["bash", "-c", f"type {cmd}"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and "shell builtin" in result.stdout:
                return f"shell builtin"
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    # Try standard version flags
    for flag in version_flags:
        try:
            result = subprocess.run(
                [cmd, flag],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0 and result.stdout:
                # Return first line of output
                return result.stdout.strip().split('\n')[0]
        except (subprocess.SubprocessError, FileNotFoundError):
            continue

    return None

def main():
    # Check arguments
    if len(sys.argv) == 1:
        show_help()
        sys.exit(1)

    # Parse options
    if sys.argv[1].startswith('-'):
        if sys.argv[1] in ['-v', '--version']:
            print(f"{BINARY_NAME} {VERSION}")
            sys.exit(0)
        elif sys.argv[1] in ['-h', '--help']:
            show_help()
            sys.exit(0)
        else:
            print(f"Unknown option: {sys.argv[1]}")
            show_help()
            sys.exit(1)

    # Check for each command
    fail_count = 0
    for cmd in sys.argv[1:]:
        if not detect_command(cmd):
            fail_count += 1

    sys.exit(fail_count)

if __name__ == "__main__":
    main()
