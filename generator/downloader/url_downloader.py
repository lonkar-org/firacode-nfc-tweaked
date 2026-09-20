import hashlib
import logging
import tarfile
import zipfile
from os.path import exists, basename
from urllib.request import urlretrieve

from .progress import show_progress

read_block_size = 1024 * 1024


class UrlDownloader:
    """URL file downloader."""

    def __init__(self, url: str, filename: str, download_dir: str, target_dir: str, files: list[str] = None,
                 sha256: str = None):
        self.url = url
        self.filename = filename
        self.files = files
        self.sha256 = sha256
        self.strip = 0
        self.download_dir = download_dir
        self.target_dir = target_dir

    def strip_members(self, members):
        for member in members:
            member.path = member.path.split('/', self.strip)[-1]
            yield member

    def extract(self):
        """Extract files from archive."""
        if self.filename.endswith('.tar.bz2'):
            archive = tarfile.open(self.filename, 'r:bz2')
        elif self.filename.endswith('.tar.gz'):
            archive = tarfile.open(self.filename, 'r:gz')
        elif self.filename.endswith('.zip'):
            archive = zipfile.ZipFile(self.filename)
        else:
            raise ValueError('Unsupported archive format')
        if isinstance(archive, tarfile.TarFile):
            self.extract_tar(archive)
        else:
            self.extract_zip(archive)
        logging.info('Extracted all files from %s', self.filename)
        archive.close()

    def extract_tar(self, archive):
        members = [
            info for info in archive.getmembers()
            if info.name in self.files
        ]
        archive.extractall(members=self.strip_members(members), path=self.target_dir)
        logging.info('Extracted %s from %s', self.files, self.filename)

    def extract_zip(self, archive):
        if self.files is None:
            archive.extractall(path=self.target_dir)
        else:
            for zip_info in archive.infolist():
                if zip_info.is_dir():
                    continue
                zip_info.filename = basename(zip_info.filename)
                if zip_info.filename not in self.files:
                    # logging.debug('Skipped %s from %s', zip_info.filename, self.filename)
                    continue
                archive.extract(zip_info, self.target_dir)

    def verify(self):
        """Fail unless the archive matches the pinned sha256."""
        if self.sha256 is None:
            return
        digest = hashlib.sha256()
        with open(self.filename, 'rb') as file:
            for block in iter(lambda: file.read(read_block_size), b''):
                digest.update(block)
        if digest.hexdigest() != self.sha256:
            raise ValueError('{} sha256 is {}, expected {}'.format(self.filename, digest.hexdigest(), self.sha256))
        logging.debug('Verified sha256 of %s', self.filename)

    def download(self):
        """Download and process the file."""
        if exists(self.filename):
            logging.debug('Skipped %s download, required file already exists', self.url.split('/')[-1].split('?')[0])
            # Cached copies are verified too: the CI cache is writable by any
            # workflow run, so it is not more trusted than the network.
            self.verify()
            self.extract()
            return
        logging.info('Downloading %s to %s', self.url, self.filename)
        urlretrieve(self.url, self.filename, show_progress)
        self.verify()
        self.extract()
