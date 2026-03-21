"""GitHub update checker for ZJClaw."""

import json
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from packaging import version as pkg_version


CURRENT_VERSION = "0.1.5"

GITHUB_REPO = "martin202008/ZJClaw"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_DOWNLOAD_URL = f"https://github.com/{GITHUB_REPO}/archive/refs/tags"


class UpdateChecker:
    """Check for updates and perform auto-update from GitHub releases."""
    
    def __init__(self, project_path: Path | None = None):
        self.project_path = project_path or Path(__file__).parent.parent.parent
        self.current_version = CURRENT_VERSION
    
    def get_current_version(self) -> str:
        """Get the current installed version."""
        return self.current_version
    
    def check_for_update(self) -> dict:
        """
        Check GitHub for available updates.
        
        Returns:
            dict with keys: has_update (bool), current_version, latest_version, 
                           download_url, release_notes
        """
        try:
            req = urllib.request.Request(
                GITHUB_API_URL,
                headers={"Accept": "application/vnd.github+json", "User-Agent": "ZJClaw"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
            
            latest_version = data.get("tag_name", "").lstrip("v")
            download_url = data.get("zipball_url", "")
            release_notes = data.get("body", "")[:500]  # First 500 chars
            
            has_update = self._compare_versions(latest_version)
            
            return {
                "has_update": has_update,
                "current_version": self.current_version,
                "latest_version": latest_version,
                "download_url": download_url,
                "release_notes": release_notes,
                "html_url": data.get("html_url", ""),
            }
        except Exception as e:
            return {
                "has_update": False,
                "current_version": self.current_version,
                "latest_version": None,
                "download_url": None,
                "release_notes": None,
                "error": str(e),
            }
    
    def _compare_versions(self, latest: str) -> bool:
        """Compare versions. Returns True if update is available."""
        try:
            current = pkg_version.parse(self.current_version)
            latest_parsed = pkg_version.parse(latest)
            return latest_parsed > current
        except:
            return False
    
    def download_and_install_update(self, download_url: str) -> dict:
        """
        Download and install the latest update.
        
        Returns:
            dict with keys: success (bool), message
        """
        try:
            temp_dir = Path(tempfile.mkdtemp())
            zip_path = temp_dir / "update.zip"
            
            # Download the update
            req = urllib.request.Request(
                download_url,
                headers={"Accept": "application/zip", "User-Agent": "ZJClaw"}
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                with open(zip_path, "wb") as f:
                    shutil.copyfileobj(response, f)
            
            # Extract the zip
            extract_dir = temp_dir / "extracted"
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Find the extracted folder
            extracted_contents = list(extract_dir.iterdir())
            if not extracted_contents:
                return {"success": False, "message": "Extraction failed - empty directory"}
            
            source_dir = extracted_contents[0]
            if not source_dir.is_dir():
                return {"success": False, "message": "Invalid update package"}
            
            # Update files (excluding user data and config)
            exclude_patterns = {
                ".zjclaw", "flask_session", "__pycache__", ".git", 
                "node_modules", ".venv", "venv", ".env"
            }
            
            updated_files = []
            for item in source_dir.rglob("*"):
                if item.is_file():
                    relative = item.relative_to(source_dir)
                    
                    # Skip excluded patterns
                    if any(pattern in relative.parts for pattern in exclude_patterns):
                        continue
                    if any(pattern in relative.name for pattern in exclude_patterns):
                        continue
                    
                    dest = self.project_path / relative.name if relative.name == item.name else self.project_path / str(relative)
                    
                    # Create parent directories
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(item, dest)
                    updated_files.append(str(relative))
            
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return {
                "success": True, 
                "message": f"Update installed successfully! Updated {len(updated_files)} files. Please restart the application.",
                "files_updated": len(updated_files)
            }
            
        except Exception as e:
            return {"success": False, "message": f"Update failed: {str(e)}"}


def get_update_checker() -> UpdateChecker:
    """Get an UpdateChecker instance."""
    return UpdateChecker()
