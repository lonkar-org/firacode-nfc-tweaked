"""Merge Noto Sans Devanagari into the patched FiraCode Nerd Font files.

Why fontTools and not fontforge: Devanagari shaping (conjuncts, reph, rakar,
i-matra reordering) lives in the dev2 GSUB/GPOS lookups. fontforge rewrites
those tables on save and is known to mangle contextual lookups and mark
anchors; fontTools.merge concatenates them untouched. So this runs last,
after the Nerd Font patcher, on the fontforge-generated files.

Why no fixed advance widths: terminals place every grapheme cluster on their
own cell grid and ignore advances between clusters; the advances only position
glyphs *inside* a cluster (base + matra + marks). Forcing them to the FiraCode
cell width would detach matras from their consonants. There is no true
monospace Devanagari font for the same reason; the terminal grid supplies the
monospacing, the font supplies correct shaping.
"""
import logging
from os import remove
from os.path import join

from fontTools.merge import Merger
from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont
from fontTools.ttLib.scaleUpem import scale_upem
from fontTools.varLib.instancer import instantiateVariableFont

from .downloader import noto_devanagari_variable_font

# fontTools narrates every pruned table at DEBUG/INFO; keep the build log readable.
logging.getLogger('fontTools').setLevel(logging.WARNING)

# FiraCode file -> wght axis value of the Devanagari instance to merge into it.
weights: dict[str, int] = {
    'Light': 300,
    'Regular': 400,
    'Retina': 450,
    'Medium': 500,
    'SemiBold': 600,
    'Bold': 700,
}

# Devanagari, Devanagari Extended, Vedic Extensions, dotted circle (mark base),
# ZWNJ/ZWJ (conjunct control), rupee sign.
unicode_ranges = [
    (0x0900, 0x097F),
    (0xA8E0, 0xA8FF),
    (0x1CD0, 0x1CFF),
    (0x25CC, 0x25CC),
    (0x200C, 0x200D),
    (0x20B9, 0x20B9),
]

# Vertical metrics that must stay FiraCode's, otherwise terminals and editors
# change the line height for every font that grew a Devanagari descender.
vertical_metrics = {
    'hhea': ('ascent', 'descent', 'lineGap'),
    'OS/2': ('sTypoAscender', 'sTypoDescender', 'sTypoLineGap', 'usWinAscent', 'usWinDescent'),
}

os2_unicode_range_devanagari_bit = 15


def devanagari_instance(variable_font: str, weight: int, upem: int) -> TTFont:
    """Static Devanagari-only instance at `weight`, rescaled to `upem`."""
    font = instantiateVariableFont(TTFont(variable_font), {'wght': weight}, inplace=True, updateFontNames=False)
    options = Options()
    options.layout_features = ['*']
    options.hinting = False
    options.glyph_names = True
    options.notdef_outline = True
    subsetter = Subsetter(options)
    subsetter.populate(unicodes=[cp for lo, hi in unicode_ranges for cp in range(lo, hi + 1)])
    subsetter.subset(font)
    scale_upem(font, upem)
    return font


def merge_devanagari(font_path: str, variable_font: str, weight: int):
    """Merge a Devanagari instance into the font at `font_path`, in place."""
    base = TTFont(font_path)
    upem = base['head'].unitsPerEm
    devanagari_path = font_path + '.devanagari.ttf'
    devanagari_instance(variable_font, weight, upem).save(devanagari_path)
    # First font wins on cmap conflicts and supplies the name table, so
    # FiraCode's Latin, its ligatures and the Nerd Font names are untouched.
    merged = Merger().merge([font_path, devanagari_path])
    for table, attrs in vertical_metrics.items():
        for attr in attrs:
            setattr(merged[table], attr, getattr(base[table], attr))
    merged['OS/2'].ulUnicodeRange1 |= 1 << os2_unicode_range_devanagari_bit
    merged.save(font_path)
    # copy_to_dist globs FiraCodeNerdFont*.ttf, so the intermediate must not linger.
    remove(devanagari_path)


def patch_devanagari(patch_files: list[str], stage_dir: str):
    """Add Devanagari glyphs and shaping to the Nerd Font patched files."""
    variable_font = join(stage_dir, noto_devanagari_variable_font)
    for file in patch_files:
        weight = file.split('-')[1].split('.')[0]
        font_path = join(stage_dir, file)
        logging.debug('Merging Devanagari wght=%d into %s', weights[weight], font_path)
        merge_devanagari(font_path, variable_font, weights[weight])
        logging.info('Merged Devanagari into %s', file)
    logging.info('Merged Devanagari into all font files')
