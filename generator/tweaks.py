import logging
from os.path import join

import fontforge

copy_characters = [
    0x069,  # i
    0x06c  # l
]

swap: dict[str, str] = {
    'a': 'a.cv01',
    'g': 'g.cv02',
    'r': 'r.ss01',
    '3': 'three.cv14',
    '$': 'dollar.ss04',
    '%': 'percent.cv18',
    '{': 'braceleft.cv29',
    '}': 'braceright.cv29',
    '|': 'bar.cv30',
}


def patch_tweaks(input_files: list[str], patches_dir: str, stage_dir: str):
    """Patch font files with custom characters."""
    for file in input_files:
        file_path = join(stage_dir, file)
        patch_path = join(patches_dir, file.split('.')[0] + '.sfd')
        logging.debug('Tweaking %s with %s', file_path, patch_path)
        input_file = fontforge.open(file_path)
        patch_file = fontforge.open(patch_path)
        for character in copy_characters:
            patch_file.selection.none()
            input_file.selection.none()
            patch_file.selection.select(character)
            patch_file.copy()
            input_file.selection.select(character)
            input_file.paste()
        for character, alternate in swap.items():
            input_file.selection.none()
            input_file.selection.select(alternate)
            input_file.copy()
            input_file.selection.select(character)
            input_file.paste()
        logging.debug('Tweaked %s', file)
        input_file.generate(file_path)
    logging.info('Tweaked all font files')
