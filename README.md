## has

A robust command-line tool to verify if specified commands are installed on your Linux operating system and output their version numbers.

### Features

- Check availability of multiple commands in one go.
- Colorized terminal output for clear visibility.
- Automatic version detection using multiple flags (`--version`, `-v`, etc.)
- Special handling for interpreted commands (e.g., node).
- Supports shell built-in commands.

### Installation

1. Download the script:
```bash
curl -O https://raw.githubusercontent.com/yourusername/has/main/has.py
```
2. Make it executable (Unix-like systems):
```bash
chmod +x has.py
```

### Usage

```bash
python3 has.py [options] <command>...
```

#### Options

| Option          | Description                          |
|-----------------|--------------------------------------|
| `-v, --version` | Show `has` version                  |
| `-h, --help`    | Display help information            |

#### Examples

Check for common tools:
```bash
python3 has.py git curl node
```

Verify built-in shell commands:
```bash
python3 has.py type cd
```

Output version information:
```bash
python3 has.py --version
```

### Sample Output

```text
✓ git 2.39.1
✓ curl 7.81.0
✓ node v18.16.0
✗ rust command not found
```

### Requirements

- Python 3.6+
- Supported on Linux, macOS, and Windows (with Python in PATH)

### How It Works

1. Checks command existence using `shutil.which()`.
2. Attempts multiple version flags for detection.
3. Special handling for:
   - Node.js (uses `-e` to get version).
   - Shell built-ins (checks via `type` command).

### Development

This is a standalone Python script with no external dependencies.

### License

[MIT](LICENSE)
