import os
import platform
import shutil
import subprocess
import json
import base64
import mimetypes
from datetime import datetime
from typing import Any
from urllib.parse import urlparse
from uuid import uuid4

from fastapi import Depends
from jinja2 import Environment, FileSystemLoader

from core.config import get_settings, Settings
from core import context as core_context
from services.storage import StorageService


class PdfGeneratorError(Exception): ...


class PdfGenerator:
    def __init__(self, settings: Settings = Depends(get_settings), storage: StorageService = Depends(StorageService)):
        self.settings = settings
        self._storage = storage
        self.chrome_binary = settings.chrome_binary or _find_chrome_binary()
        self.tmp_dir = os.path.join(settings.storage_data_path, "tmp")
        os.makedirs(self.tmp_dir, exist_ok=True)

        self._validated = None
        self._style_url = None

    async def generate(self, template_file: str, context: dict[str, Any] | None = None) -> str:
        self._validate_chrome()
        html_content = self._render_content(template_file, context)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = os.path.join(self.tmp_dir, f"{timestamp}-{uuid4().hex}.pdf")

        return self._generate_pdf(filename, html_content)

    def _validate_chrome(self) -> None:
        if self._validated is None:
            try:
                result = subprocess.run(
                    [self.chrome_binary, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                self._validated = result.returncode == 0
            except Exception as e:
                raise PdfGeneratorError(f"Error on Chrome binary validation: {str(e)}")

        if not self._validated:
            raise PdfGeneratorError(f"Chrome binary not available: {self.chrome_binary}")

    def _get_style_url(self) -> str:
        if self._style_url is None:
            manifest_file = os.path.join(self.settings.project_dir, "..", "app", "dist", ".vite", "manifest.json")

            if os.path.exists(manifest_file) and not _is_local_url(self.settings.base_url_app):
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)

                pdf_entry = manifest.get('src/pdf.scss')

                if pdf_entry and pdf_entry.get('file'):
                    css_path = pdf_entry['file']
                else:
                    css_path = 'src/pdf.css'
            else:
                # Use the local server
                css_path = 'src/pdf.css'

            self._style_url = f"{self.settings.base_url_app}/{css_path}"

        return self._style_url

    def _render_content(self, template_file: str, context: dict[str, Any] | None = None) -> str:
        template_dir = os.path.join(self.settings.project_dir, "templates", "pdf")
        template_env = Environment(loader=FileSystemLoader(template_dir))

        def asset(path: str) -> str:
            """Convert file to base64 data URL"""
            app_src_dir = os.path.join(self.settings.project_dir, "..", "app", "src")
            file_path = os.path.join(app_src_dir, path)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Asset not found: {path}")

            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"

            with open(file_path, 'rb') as f:
                file_content = f.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')

            return f"data:{mime_type};base64,{encoded_content}"
        
        def storage(path: str | None, global_storage: bool = False) -> str:
            """Convert storage file to base64 data URL"""
            if not path:
                return ''

            file_path = self._storage.get_file_path(path, ensure_exists=False, global_storage=global_storage)

            if not file_path.exists():
                return ''

            mime_type, _ = mimetypes.guess_type(str(file_path))

            if not mime_type:
                mime_type = "application/octet-stream"

            with open(file_path, 'rb') as f:
                file_content = f.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')

            return f"data:{mime_type};base64,{encoded_content}"

        template_env.globals['asset'] = asset
        template_env.globals['storage'] = storage
        template = template_env.get_template(template_file)

        return template.render({
            **(context or {}),
            'style_url': self._get_style_url(),
            'current_workspace': core_context.get_workspace(),
            'current_workspace_user': core_context.get_workspace_user(),
            'current_user': core_context.get_user(),
        })

    def _generate_pdf(self, filename: str, content: str) -> str:
        html_file = os.path.join(self.tmp_dir, f"pdf_{uuid4().hex}.html")

        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

            chrome_args = [
                self.chrome_binary,
                '--headless=new',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--no-pdf-header-footer',
                '--print-background',
                f'--print-to-pdf={filename}',
                f'file://{os.path.abspath(html_file)}'
            ]

            result = subprocess.run(
                chrome_args,
                capture_output=True,
                text=True,
                timeout=30,
            )

            try:
                os.unlink(html_file)
            except OSError:
                pass

            if result.returncode != 0:
                raise PdfGeneratorError(f"PDF Generator Error: {result.stderr}")

            if not os.path.exists(filename):
                raise PdfGeneratorError("PDF file not created")

            return filename

        except Exception:
            if os.path.exists(html_file):
                try:
                    os.unlink(html_file)
                except OSError:
                    pass
            raise PdfGeneratorError(f"PDF Generator Error: {html_file}")


def _find_chrome_binary() -> str:
    system = platform.system().lower()

    if system == "darwin":
        paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/opt/homebrew/bin/chromium",
            "/usr/local/bin/chromium",
        ]
    elif system == "linux":
        paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]
    else:
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

    for path in paths:
        if os.path.isfile(path):
            return path

    for binary in ["google-chrome", "google-chrome-stable", "chromium", "chrome"]:
        if shutil.which(binary):
            return binary

    return "google-chrome"


def _is_local_url(url: str) -> bool:
    if not url:
        return True

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        if not hostname:
            return True

        local_hosts = [
            'localhost',
            '127.0.0.1',
            '0.0.0.0',
            '::1'
        ]

        return hostname.lower() in local_hosts or hostname.startswith('192.168.') or hostname.startswith(
            '10.') or hostname.startswith('172.')
    except:
        return True
