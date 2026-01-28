# Programming Fonts Installer

A beautiful terminal user interface (TUI) application for browsing and installing programming fonts from the [ProgrammingFonts](https://github.com/ProgrammingFonts/ProgrammingFonts) repository.

## Features

- 📚 Browse 108+ programming fonts
- 🔍 Search/filter fonts in real-time
- 📥 One-click installation
- 💻 Cross-platform support (Linux, macOS, Windows)
- 🎨 Beautiful terminal interface with Textual
- ⚡ Fast and lightweight

## Screenshots

The TUI features:
- Left panel: Searchable font list
- Right panel: Font information and installation details
- Keyboard shortcuts for quick navigation
- Status bar with real-time feedback

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for downloading fonts)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install textual requests
```

## Usage

### Run the Application

```bash
python font_installer.py
```

Or make it executable:

```bash
chmod +x font_installer.py
./font_installer.py
```

### Keyboard Shortcuts

- **Arrow Keys / j/k**: Navigate through font list
- **/** : Focus search box
- **i**: Install selected font
- **r**: Refresh font list
- **q**: Quit application
- **Tab**: Switch focus between panels

### Installing a Font

1. Browse or search for a font using the search box
2. Select a font from the list
3. Press `i` or click "Install Font" button
4. Wait for the download and installation to complete
5. Restart your applications to use the new font

## Font Installation Locations

Fonts are installed in the following locations based on your OS:

- **Linux**: `~/.local/share/fonts/`
- **macOS**: `~/Library/Fonts/`
- **Windows**: `%LOCALAPPDATA%\Microsoft\WindowsFonts\`

## Available Fonts

The application provides access to 108 programming fonts including:

- Fira Code
- JetBrains Mono
- Cascadia Code
- Hack
- Source Code Pro
- Inconsolata
- Monaco
- Consolas
- And 100+ more!

## Requirements

- `textual>=7.0.0` - Modern TUI framework
- `requests>=2.25.0` - HTTP library for downloading fonts

## How It Works

1. **Browse**: The app displays all available fonts from the ProgrammingFonts repository
2. **Search**: Filter fonts in real-time as you type
3. **Preview**: View font information and installation location
4. **Download**: Fetches font files directly from GitHub
5. **Install**: Copies fonts to the appropriate system directory
6. **Cache**: On Linux, automatically refreshes the font cache

## Platform-Specific Notes

### Linux

- Fonts are installed per-user
- Font cache is automatically refreshed using `fc-cache`
- May need to restart applications to see new fonts

### macOS

- Fonts are installed to user Library folder
- Restart applications to see new fonts
- Some apps may require logout/login

### Windows

- Fonts are installed to user AppData folder
- May require administrator privileges for system-wide installation
- Restart applications to see new fonts

## Troubleshooting

### Font not appearing after installation

1. Restart the application you want to use the font in
2. On some systems, you may need to log out and log back in
3. Check the installation directory to verify files were copied

### Download failures

- Check your internet connection
- Some fonts may have been moved or renamed in the repository
- Try refreshing the font list

### Permission errors

- The app installs fonts for the current user only
- If you need system-wide installation, you may need elevated privileges

## Contributing

Issues and pull requests are welcome! This is a community tool.

## Credits

- Font collection: [ProgrammingFonts Repository](https://github.com/ProgrammingFonts/ProgrammingFonts)
- TUI Framework: [Textual](https://textual.textualize.io/)

## License

This installer tool is provided as-is for educational purposes. Please respect the individual licenses of the fonts you install. Refer to the [ProgrammingFonts repository](https://github.com/ProgrammingFonts/ProgrammingFonts) for specific font licenses.

## Author

Created to make programming font installation easier for developers everywhere! 🚀
