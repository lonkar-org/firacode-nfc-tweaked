import logging
import os
from subprocess import Popen

from .downloader import nerd_font_patcher_exec, firacode_font_files

# File names the patcher writes for firacode_font_files (family renamed, weight kept).
nerd_font_files = [file.replace('FiraCode-', 'FiraCodeNerdFont-') for file in firacode_font_files]


def patch_nerd_font(patch_files: list[str], stage_dir: str):
    """Patch nerd font."""
    for file in patch_files:
        args = ['--careful', '--complete']
        if 'CI' in os.environ and os.environ['CI'] == 'true':
            args.append('--quiet')
        args.append(file)
        process = Popen([nerd_font_patcher_exec, *args], shell=False, cwd=stage_dir)
        process.communicate()
        if process.returncode != 0:
            raise RuntimeError('Failed to patch font file')
        logging.info('Patched %s with nerd fonts', file)
    logging.info('Patched all font files with nerd font complete and variable width')
