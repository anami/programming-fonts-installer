# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A TUI (Terminal User Interface) application for browsing and installing programming fonts from the ProgrammingFonts repository. Built with Python using the Textual framework.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python font_installer.py
```

## Architecture

This is a single-file application (`font_installer.py`) with two main components:

- **FontInstaller**: Static utility class handling cross-platform font installation (Linux/macOS/Windows). Downloads fonts from the GitHub ProgrammingFonts repository via the GitHub API.

- **FontBrowser(App)**: Textual TUI application with a two-panel layout (font list + info panel). Uses Textual's reactive patterns for search filtering and list updates.

Key data flow:
1. Font list is hardcoded in `AVAILABLE_FONTS`
2. GitHub API fetches font files on install (`/contents/font/{font_name}`)
3. Fonts are copied to OS-specific user font directories
4. Linux systems get automatic font cache refresh via `fc-cache`

## Dependencies

- `textual>=7.0.0` - TUI framework
- `requests>=2.25.0` - HTTP requests for GitHub API
