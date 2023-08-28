import logging
import os
from os.path import dirname, realpath, join

from .downloader import FiraCode, firacode_font_files
from .downloader import NerdFontPatcher
from .nerd_font import patch_nerd_font
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
        os.system('rm -rf {}'.format(_dir))


def copy_to_dist():
    os.system('cd {stage}; cp FiraCodeNerdFont*.ttf {dist}; cd {dist}; ls -1'.format(stage=stage_dir, dist=dist_dir))
    logging.info('Copied all font files to dist')


def generate(fira_code: str, nerd_font_patcher: str):
    cleanup('dist', 'stage')
    setup('dist', 'stage', 'downloads')
    NerdFontPatcher(version=nerd_font_patcher, download_dir=downloads_dir, target_dir=stage_dir).download()
    FiraCode(version=fira_code, download_dir=downloads_dir, target_dir=stage_dir).download()
    input_files = firacode_font_files
    patch_tweaks(input_files=input_files, patches_dir=patches_dir, stage_dir=stage_dir)
    patch_nerd_font(patch_files=input_files, stage_dir=stage_dir)
    copy_to_dist()
    cleanup('stage')
