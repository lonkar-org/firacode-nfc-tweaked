from os import chmod
from os.path import relpath, join

from .url_downloader import UrlDownloader

url_template = 'https://github.com/ryanoasis/nerd-fonts/releases/download/{}/FontPatcher.zip'
nerd_font_patcher_dir = 'nerd-font-patcher'
nerd_font_patcher_exec_name = 'font-patcher'
nerd_font_patcher_exec = join(nerd_font_patcher_dir, nerd_font_patcher_exec_name)


class NerdFontPatcher(UrlDownloader):
    """Nerd Font Patcher downloader."""

    def __init__(self, version: str, download_dir: str, target_dir: str, sha256: str = None):
        self.version = version
        # Version in the name: the release asset is always FontPatcher.zip, so
        # without it a bump reuses the cached archive of the previous version.
        filename = relpath(join(download_dir, 'FontPatcher_{}.zip'.format(self.version)))
        target_dir = join(target_dir, nerd_font_patcher_dir)
        super().__init__(url_template.format(self.version), filename, download_dir, target_dir, sha256=sha256)

    def extract(self):
        super().extract()
        _exec = join(self.target_dir, nerd_font_patcher_exec_name)
        chmod(_exec, 0o755)
