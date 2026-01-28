#!/usr/bin/env python3
"""
Programming Fonts Installer
A TUI application to browse and install fonts from the ProgrammingFonts repository
"""

import os
import sys
import platform
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import List, Dict
import requests

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static, Button, ListView, ListItem, Label, Input
from textual.binding import Binding
from textual import events
from rich.text import Text


# Font repository details
REPO_OWNER = "ProgrammingFonts"
REPO_NAME = "ProgrammingFonts"
REPO_BRANCH = "master"
BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{REPO_BRANCH}/font"

# List of all available fonts (from the repository)
AVAILABLE_FONTS = [
    "3270-font", "agave", "anka-coder", "anonymous-pro", "apl-2741", "apl-385",
    "aurulent", "average", "b612-mono", "bedstead", "bitstream-vera", "borg-sans-mono",
    "bpmono", "bront-dejavu", "bront-ubuntu", "camingo-code", "cascadia-code",
    "Classic-X11-6x13", "code-new-roman", "consolamono", "Consolas", "Courier-New",
    "courier-prime", "courier-prime-code", "Cousine", "Crystal", "cutive", "d2coding",
    "daddytimemono", "dank-mono", "DEC-Terminal-Modern", "Deja-Vu-Sans-Mono", "Dina",
    "DM_Mono", "Droid-Sans-Mono", "Edlo", "effects-eighty", "Envy Code R PR7",
    "envy-code-r", "EspressoMono", "fairfax", "fairfax-hd", "fairfax-serif",
    "FantasqueSansMono", "fifteen", "fira", "Fira-Code", "FiraFlott", "fixedsys",
    "fixedsys-ligatures", "generic", "Generic Mono", "gnu-freefont", "gohufont",
    "go-mono", "Hack", "Hasklig", "Hermit", "ia-writer-mono", "IBM Plex Mono",
    "Inconsolata", "Input", "Inter-UI-3", "iosevka", "Jetbrains Mono", "JuliaMono",
    "latin-modern", "league", "lekton", "liberation", "Luculent", "luxi", "M+",
    "Menlo", "mensch", "meslo", "Microsoft-YaHei-Mono", "Monaco", "Monofur",
    "Monoid", "MonoLisa", "Mononoki", "nanum-gothic-coding", "notcouriersans", "noto",
    "nova", "office-code-pro", "Overpass Mono", "Oxygen-Mono", "plex-mono",
    "Pragmata-Pro", "profont", "Proggy", "Pt-Mono", "recursive", "RedHatMono",
    "Ricty-Diminished", "Roboto_Mono", "Sarasa-Gothic", "saxMono", "SomeType-Mono",
    "Source-Code-Pro", "space", "Triskweline", "Ubuntu-Mono", "Unifont",
    "Victor Mono", "Vintage Fonts Pack"
]


class FontInstaller:
    """Handles font installation for different operating systems"""
    
    @staticmethod
    def get_font_directory() -> Path:
        """Get the appropriate font directory for the current OS"""
        system = platform.system()
        
        if system == "Linux":
            # User fonts directory
            font_dir = Path.home() / ".local" / "share" / "fonts"
        elif system == "Darwin":  # macOS
            font_dir = Path.home() / "Library" / "Fonts"
        elif system == "Windows":
            # Windows user fonts
            font_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WindowsFonts"
        else:
            raise RuntimeError(f"Unsupported operating system: {system}")
        
        font_dir.mkdir(parents=True, exist_ok=True)
        return font_dir
    
    @staticmethod
    def download_font_directory(font_name: str, temp_dir: Path) -> bool:
        """Download all font files from a font directory in the repository"""
        try:
            # GitHub API to list directory contents
            api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/font/{font_name}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code != 200:
                return False
            
            files = response.json()
            downloaded = False
            
            for file_info in files:
                if file_info['type'] == 'file':
                    file_name = file_info['name']
                    # Download font files (ttf, otf, woff, woff2, etc.)
                    if any(file_name.lower().endswith(ext) for ext in ['.ttf', '.otf', '.woff', '.woff2', '.ttc']):
                        download_url = file_info['download_url']
                        file_response = requests.get(download_url, timeout=30)
                        
                        if file_response.status_code == 200:
                            file_path = temp_dir / file_name
                            file_path.write_bytes(file_response.content)
                            downloaded = True
            
            return downloaded
        except Exception as e:
            print(f"Error downloading font: {e}")
            return False
    
    @staticmethod
    def install_font(font_name: str) -> tuple[bool, str]:
        """Install a font from the repository"""
        try:
            font_dir = FontInstaller.get_font_directory()
            target_dir = font_dir / font_name
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Create temporary directory for downloads
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Download font files
                if not FontInstaller.download_font_directory(font_name, temp_path):
                    return False, "Failed to download font files"
                
                # Copy font files to target directory
                font_files = list(temp_path.glob("*"))
                if not font_files:
                    return False, "No font files found"
                
                for font_file in font_files:
                    if font_file.is_file():
                        shutil.copy2(font_file, target_dir / font_file.name)
                
                # Refresh font cache on Linux
                if platform.system() == "Linux":
                    os.system("fc-cache -f -v > /dev/null 2>&1")
                
                return True, f"Successfully installed {len(font_files)} font file(s)"
        
        except Exception as e:
            return False, f"Installation error: {str(e)}"


class FontListItem(ListItem):
    """Custom list item for fonts"""

    def __init__(self, font_name: str) -> None:
        super().__init__()
        self.font_name = font_name

    def compose(self) -> ComposeResult:
        yield Label(self.font_name)


class FontBrowser(App):
    """TUI application for browsing and installing programming fonts"""

    TITLE = "Programming Fonts Installer"
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #main-container {
        height: 100%;
    }
    
    #left-panel {
        width: 40%;
        border: solid $primary;
        padding: 1;
    }
    
    #right-panel {
        width: 60%;
        border: solid $accent;
        padding: 1;
    }
    
    #search-box {
        margin-bottom: 1;
    }
    
    #font-list {
        height: 1fr;
        border: solid $secondary;
    }
    
    #info-panel {
        height: 100%;
    }
    
    .info-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    .info-text {
        margin-bottom: 1;
    }
    
    #button-container {
        height: auto;
        margin-top: 1;
    }
    
    Button {
        margin-right: 2;
    }
    
    #status-bar {
        dock: bottom;
        height: 3;
        background: $panel;
        padding: 1;
        text-align: center;
    }
    
    ListView {
        background: $surface;
    }
    
    ListItem {
        padding: 0 1;
    }
    
    ListItem:hover {
        background: $boost;
    }
    
    ListItem.-selected {
        background: $accent;
        color: $text;
    }
    """
    
    BINDINGS = [
        Binding("escape", "quit", "Quit", show=True, priority=True),
        Binding("i", "install", "Install", show=True),
        Binding("/", "focus_search", "Search", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.filtered_fonts = AVAILABLE_FONTS.copy()
        self.selected_font = None
    
    def compose(self) -> ComposeResult:
        """Create the layout"""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal():
                with Vertical(id="left-panel"):
                    yield Label("Search:", classes="info-title")
                    yield Input(placeholder="Type to filter fonts...", id="search-box")
                    yield ListView(
                        *[FontListItem(font) for font in self.filtered_fonts],
                        id="font-list"
                    )
                
                with VerticalScroll(id="right-panel"):
                    yield Label("Font Information", classes="info-title")
                    yield Static(id="info-panel", markup=True)
                    
                    with Horizontal(id="button-container"):
                        yield Button("Install Font", id="install-btn", variant="success")
                        yield Button("Refresh List", id="refresh-btn", variant="primary")
        
        yield Static("Ready. Select a font to view details.", id="status-bar")
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the app when mounted"""
        font_list = self.query_one("#font-list", ListView)
        if font_list.children:
            font_list.index = 0
            self.update_info_panel(AVAILABLE_FONTS[0])
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input"""
        if event.input.id == "search-box":
            search_term = event.value.lower()
            self.filtered_fonts = [
                font for font in AVAILABLE_FONTS
                if search_term in font.lower()
            ]
            self.refresh_font_list()
    
    def refresh_font_list(self) -> None:
        """Refresh the font list based on current filter"""
        font_list = self.query_one("#font-list", ListView)
        font_list.clear()
        
        for font in self.filtered_fonts:
            font_list.append(FontListItem(font))
        
        if self.filtered_fonts:
            font_list.index = 0
            self.update_info_panel(self.filtered_fonts[0])
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle font selection"""
        if isinstance(event.item, FontListItem):
            self.selected_font = event.item.font_name
            self.update_info_panel(self.selected_font)
    
    def update_info_panel(self, font_name: str) -> None:
        """Update the information panel with font details"""
        info_panel = self.query_one("#info-panel", Static)
        
        # Create information text
        info_text = f"""[bold cyan]Font Name:[/bold cyan]
{font_name}

[bold cyan]Repository:[/bold cyan]
ProgrammingFonts/ProgrammingFonts

[bold cyan]Installation Location:[/bold cyan]
{FontInstaller.get_font_directory()}

[bold cyan]Font Directory:[/bold cyan]
{FontInstaller.get_font_directory() / font_name}

[bold yellow]Instructions:[/bold yellow]
1. Click 'Install Font' or press 'i'
2. Wait for download to complete
3. After installation, restart applications to use the font
4. On Linux, font cache will be refreshed automatically

[bold green]Note:[/bold green]
Font will be installed for the current user only.
"""
        
        info_panel.update(info_text)
    
    def action_install(self) -> None:
        """Install the currently selected font"""
        if not self.selected_font:
            self.update_status("Please select a font first", error=True)
            return
        
        self.update_status(f"Installing {self.selected_font}...")
        
        success, message = FontInstaller.install_font(self.selected_font)
        
        if success:
            self.update_status(f"✓ {message}", error=False)
        else:
            self.update_status(f"✗ {message}", error=True)
    
    def action_refresh(self) -> None:
        """Refresh the font list"""
        search_box = self.query_one("#search-box", Input)
        search_box.value = ""
        self.filtered_fonts = AVAILABLE_FONTS.copy()
        self.refresh_font_list()
        self.update_status("Font list refreshed")
    
    def action_focus_search(self) -> None:
        """Focus the search box"""
        search_box = self.query_one("#search-box", Input)
        search_box.focus()

    def action_cursor_down(self) -> None:
        """Move cursor down in font list"""
        font_list = self.query_one("#font-list", ListView)
        font_list.action_cursor_down()

    def action_cursor_up(self) -> None:
        """Move cursor up in font list"""
        font_list = self.query_one("#font-list", ListView)
        font_list.action_cursor_up()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "install-btn":
            self.action_install()
        elif event.button.id == "refresh-btn":
            self.action_refresh()
    
    def update_status(self, message: str, error: bool = False) -> None:
        """Update the status bar"""
        status_bar = self.query_one("#status-bar", Static)
        if error:
            status_bar.update(f"[red]{message}[/red]")
        else:
            status_bar.update(f"[green]{message}[/green]")


def main():
    """Main entry point"""
    app = FontBrowser()
    app.run()


if __name__ == "__main__":
    main()
