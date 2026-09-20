#!/usr/bin/env python3
"""Smoke test the built fonts before they are released.

Usage: ./scripts/verify_fonts.py [dist_dir] [downloads_dir]

Checks what breaks silently when an upstream release changes shape: a patcher
that stops emitting a weight, a subset that drops the Devanagari shaping, a
FiraCode release that renames the stylistic variants so the swap pastes
nothing, a merge that loses the vertical metrics or a copyright line.

The expectations below are deliberately written out again instead of imported
from `generator`: importing that package pulls in fontforge, and a test that
reuses the code under test cannot catch the code being wrong. Keep them in
sync with generator/tweaks.py and generator/nerd_font.py by hand.
"""
import sys
from glob import glob
from os.path import basename, join
from zipfile import ZipFile

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

expected_fonts = [
    'FiraCodeNerdFont-Bold.ttf',
    'FiraCodeNerdFont-Light.ttf',
    'FiraCodeNerdFont-Medium.ttf',
    'FiraCodeNerdFont-Regular.ttf',
    'FiraCodeNerdFont-Retina.ttf',
    'FiraCodeNerdFont-SemiBold.ttf',
]

# Characters that must have a glyph: Latin, a FiraCode ligature component, one
# icon from each of four Nerd Font glyph sets, Devanagari ka, a matra, the
# rupee. The icons are codepoints stock FiraCode does not carry, so they only
# pass if the patcher actually ran; the powerline arrows would not do, FiraCode
# ships those itself. F0001 is beyond the BMP, which --complete must reach.
# The patcher remaps its glyph sources, so these are the target codepoints out
# of glyphnames.json in FontPatcher.zip, not the ones in the source fonts.
# Read that file again on a patcher bump: the Font Awesome set moved once.
expected_characters = [
    0x0041,   # A
    0x003D,   # =, a ligature component
    0xE613,   # seti-folder
    0xED00,   # fa-location_dot
    0xF300,   # linux-alpine, from font-logos
    0xF0001,  # md-vector_square, beyond the BMP
    0x0915,   # क
    0x093F,   # ि
    0x20B9,   # ₹
]

# Stylistic variants swapped in by generator/tweaks.py.
swap = {
    'a': 'a.cv01',
    'g': 'g.cv02',
    'r': 'r.ss01',
    'three': 'three.cv14',
    'dollar': 'dollar.ss04',
    'percent': 'percent.cv18',
    'braceleft': 'braceleft.cv29',
    'braceright': 'braceright.cv29',
    'bar': 'bar.cv30',
}

# Glyphs copied from patches/*.sfd, so they must differ from stock FiraCode.
tweaked_glyphs = ['i', 'l']

vertical_metrics = {
    'hhea': ('ascent', 'descent', 'lineGap'),
    'OS/2': ('sTypoAscender', 'sTypoDescender', 'sTypoLineGap', 'usWinAscent', 'usWinDescent'),
}

devanagari_script = 'dev2'
os2_unicode_range_devanagari_bit = 15
copyright_name_id = 0
license_name_id = 13


def outline(font: TTFont, glyph_name: str) -> list:
    """Drawing commands for `glyph_name`, comparable between fonts."""
    pen = RecordingPen()
    font.getGlyphSet()[glyph_name].draw(pen)
    return pen.value


def check_font(path: str, failures: list):
    """Check one built font, appending one line per problem to `failures`."""
    def fail(message):
        failures.append('{}: {}'.format(basename(path), message))

    font = TTFont(path)
    cmap = font.getBestCmap()
    for code_point in expected_characters:
        if code_point not in cmap:
            fail('no glyph for U+{:04X}'.format(code_point))

    glyph_order = set(font.getGlyphOrder())
    for glyph_name, variant in swap.items():
        if glyph_name not in glyph_order or variant not in glyph_order:
            fail('missing {} or {}, stylistic variant renamed upstream?'.format(glyph_name, variant))
            continue
        if outline(font, glyph_name) != outline(font, variant):
            fail('{} is not the {} outline, the swap did not apply'.format(glyph_name, variant))

    if devanagari_script not in {record.ScriptTag for record in font['GSUB'].table.ScriptList.ScriptRecord}:
        fail('no {} script in GSUB, Devanagari will not shape'.format(devanagari_script))
    if not font['OS/2'].ulUnicodeRange1 & (1 << os2_unicode_range_devanagari_bit):
        fail('OS/2 Devanagari unicode range bit is not set')

    notice = font['name'].getDebugName(copyright_name_id) or ''
    for holder in ['Fira Code', 'Noto']:
        if holder not in notice:
            fail('copyright name record does not mention {}'.format(holder))
    if 'Open Font License' not in (font['name'].getDebugName(license_name_id) or ''):
        fail('license name record does not name the Open Font License')


def check_metrics_match(fonts: dict, failures: list):
    """Every weight must keep one line height, or terminals jump between them."""
    for table, attributes in vertical_metrics.items():
        for attribute in attributes:
            values = {name: getattr(font[table], attribute) for name, font in fonts.items()}
            if len(set(values.values())) > 1:
                failures.append('{}.{} differs between weights: {}'.format(table, attribute, values))


def check_tweaks_applied(fonts: dict, downloads_dir: str, failures: list):
    """Compare against the stock FiraCode in the download cache, when present."""
    archives = glob(join(downloads_dir, 'fira_code_*.zip'))
    if not archives:
        print('SKIP  stock FiraCode comparison, no archive in {}'.format(downloads_dir))
        return
    with ZipFile(archives[0]) as archive:
        for name in archive.namelist():
            if not name.endswith('ttf/FiraCode-Regular.ttf'):
                continue
            with archive.open(name) as file:
                stock = TTFont(file)
            built = fonts['FiraCodeNerdFont-Regular.ttf']
            for glyph_name in tweaked_glyphs:
                if outline(built, glyph_name) == outline(stock, glyph_name):
                    failures.append('FiraCodeNerdFont-Regular.ttf: {} is still the stock outline'.format(glyph_name))
            return
    print('SKIP  stock FiraCode comparison, no FiraCode-Regular.ttf in {}'.format(archives[0]))


def main(dist_dir: str, downloads_dir: str) -> int:
    failures = []
    built = sorted(basename(path) for path in glob(join(dist_dir, '*.ttf')))
    if built != expected_fonts:
        failures.append('{} holds {}, expected {}'.format(dist_dir, built, expected_fonts))
    fonts = {name: TTFont(join(dist_dir, name)) for name in built}
    for name in built:
        check_font(join(dist_dir, name), failures)
    if fonts:
        check_metrics_match(fonts, failures)
    if 'FiraCodeNerdFont-Regular.ttf' in fonts:
        check_tweaks_applied(fonts, downloads_dir, failures)

    for failure in failures:
        print('FAIL  {}'.format(failure))
    if failures:
        print('{} check(s) failed'.format(len(failures)))
        return 1
    print('OK    {} fonts pass all checks'.format(len(built)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'dist',
                  sys.argv[2] if len(sys.argv) > 2 else 'downloads'))
