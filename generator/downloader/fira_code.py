from os.path import relpath, join

from .url_downloader import UrlDownloader

url_template = 'https://github.com/tonsky/FiraCode/releases/download/{0}/Fira_Code_v{0}.zip'
firacode_font_files = [
    'FiraCode-Bold.ttf',
    'FiraCode-Light.ttf',
    'FiraCode-Medium.ttf',
    'FiraCode-Regular.ttf',
    'FiraCode-Retina.ttf',
    'FiraCode-SemiBold.ttf',
]


class FiraCode(UrlDownloader):
    """Fira Code Font downloader."""

    def __init__(self, version: str, download_dir: str, target_dir: str):
        self.version = version
        filename = relpath(join(download_dir, 'fira_code_{}.zip'.format(self.version)))
        super().__init__(url_template.format(self.version), filename, download_dir, target_dir, firacode_font_files)
        self.strip = 1
