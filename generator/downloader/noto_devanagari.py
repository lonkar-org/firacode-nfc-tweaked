from os.path import relpath, join

from .url_downloader import UrlDownloader

url_template = 'https://github.com/notofonts/devanagari/releases/download/NotoSansDevanagari-{0}/NotoSansDevanagari-{0}.zip'
# Unhinted weight-axis-only variable font: one file instanced per FiraCode weight.
# Unhinted because the glyphs get rescaled to FiraCode's em and hints would not survive.
noto_devanagari_variable_font = 'NotoSansDevanagari[wght].ttf'


class NotoDevanagari(UrlDownloader):
    """Noto Sans Devanagari font downloader."""

    def __init__(self, version: str, download_dir: str, target_dir: str, sha256: str = None):
        self.version = version
        filename = relpath(join(download_dir, 'noto_sans_devanagari_{}.zip'.format(self.version)))
        super().__init__(url_template.format(self.version), filename, download_dir, target_dir,
                         [noto_devanagari_variable_font], sha256)

    def extract_zip(self, archive):
        # The release zip ships the same file name under hinted/, unhinted/ and
        # googlefonts/; keep only the unhinted slim (wght-only) variable font.
        for zip_info in archive.infolist():
            if zip_info.is_dir() or not zip_info.filename.endswith('unhinted/slim-variable-ttf/' + noto_devanagari_variable_font):
                continue
            zip_info.filename = noto_devanagari_variable_font
            archive.extract(zip_info, self.target_dir)
            return
        raise FileNotFoundError('{} not found in {}'.format(noto_devanagari_variable_font, self.filename))
