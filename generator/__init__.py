import logging
import os
import shutil
from glob import glob
from os.path import dirname, realpath, join, basename

from .downloader import FiraCode, firacode_font_files
from .downloader import NerdFontPatcher
from .downloader import NotoDevanagari
from .devanagari import patch_devanagari
from .nerd_font import patch_nerd_font, nerd_font_files
from .tweaks import patch_tweaks

self_dir = dirname(realpath(__file__))
downloads_dir = join(self_dir, '../downloads')
stage_dir = join(self_dir, '../stage')
dist_dir = join(self_dir, '../dist')
patches_dir = join(self_dir, '../patches')


def setup(*dirs: str):
    """Recursively create directories relative to the current working directory"""
    for _dir in dirs:
        _dir = join(self_dir, '..', _dir)
        os.makedirs(_dir, mode=0o755, exist_ok=True)


def cleanup(*dirs: str):
    """Recursively remove directories relative to the current working directory"""
    for _dir in dirs:
        _dir = join(self_dir, '..', _dir)
        shutil.rmtree(_dir, ignore_errors=True)


def copy_to_dist():
    """Copy the built fonts to dist, failing if the patcher produced none."""
    # Was a shelled out `cp` whose exit code nobody read: a renamed patcher
    # output left dist empty and the release still shipped a fontless zip.
    font_files = sorted(glob(join(stage_dir, 'FiraCodeNerdFont*.ttf')))
    if len(font_files) != len(nerd_font_files):
        raise RuntimeError('Expected {} built fonts in {}, found {}'.format(
            len(nerd_font_files), stage_dir, [basename(file) for file in font_files]))
    for file in font_files:
        shutil.copy(file, join(dist_dir, basename(file)))
        logging.debug('Copied %s to dist', basename(file))
    logging.info('Copied all font files to dist')


def generate(fira_code: dict, nerd_font_patcher: dict, noto_devanagari: dict):
    """Build the fonts from the pinned sources, each a {version, sha256} dict."""
    cleanup('dist', 'stage')
    setup('dist', 'stage', 'downloads')
    NerdFontPatcher(version=nerd_font_patcher['version'], sha256=nerd_font_patcher['sha256'],
                    download_dir=downloads_dir, target_dir=stage_dir).download()
    FiraCode(version=fira_code['version'], sha256=fira_code['sha256'],
             download_dir=downloads_dir, target_dir=stage_dir).download()
    NotoDevanagari(version=noto_devanagari['version'], sha256=noto_devanagari['sha256'],
                   download_dir=downloads_dir, target_dir=stage_dir).download()
    input_files = firacode_font_files
    patch_tweaks(input_files=input_files, patches_dir=patches_dir, stage_dir=stage_dir)
    patch_nerd_font(patch_files=input_files, stage_dir=stage_dir)
    patch_devanagari(patch_files=nerd_font_files, stage_dir=stage_dir)
    copy_to_dist()
    cleanup('stage')
