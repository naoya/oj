# Claude Code Configuration

This file contains information to help Claude Code understand and work with this project.

## Project Overview

This is the `online-judge-tools` project - a command-line tool for competitive programming that helps with downloading sample cases, testing solutions, and submitting code to online judges.

## Project Structure

- `onlinejudge_command/` - Main package containing the CLI implementation
  - `subcommand/` - Individual subcommands (download, test, submit, etc.)
  - `main.py` - Entry point
- `tests/` - Test suite
- `docs/` - Documentation

## Development Commands

### Testing
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Add linting/formatting commands if available
```

### Installation
```bash
pip install -e .
```

## Notes

- This is a Python package that provides the `oj` command-line tool
- Main functionality includes downloading test cases, running tests, and submitting solutions
- Supports multiple online judge platforms