from os import chmod
from os.path import relpath, join

from .url_downloader import UrlDownloader

url_template = 'https://github.com/ryanoasis/nerd-fonts/releases/download/{}/FontPatcher.zip'
nerd_font_patcher_dir = 'nerd-font-patcher'
nerd_font_patcher_exec_name = 'font-patcher'
nerd_font_patcher_exec = join(nerd_font_patcher_dir, nerd_font_patcher_exec_name)


class NerdFontPatcher(UrlDownloader):
    """Nerd Font Patcher downloader."""

    def __init__(self, version: str, download_dir: str, target_dir: str):
        self.version = version
        filename = relpath(join(download_dir, 'FontPatcher.zip'))
        target_dir = join(target_dir, nerd_font_patcher_dir)
        super().__init__(url_template.format(self.version), filename, download_dir, target_dir)

    def extract(self):
        super().extract()
        _exec = join(self.target_dir, nerd_font_patcher_exec_name)
        chmod(_exec, 0o755)
