CHANGELOG
================================================================================
Versions are SemVer, kept in the `VERSION` file. The FiraCode, Nerd Fonts and Noto Sans
Devanagari versions a release was built from are listed in its release notes. Releases
before v1.0.0 were tagged `v<FiraCode>+<Nerd Fonts>[+<Noto Sans Devanagari>]` instead.

## v1.0.0

Same fonts as `v6.2+v3.5.1+v2.007`, released under the right license with a verified build.

* Fonts are licensed under the SIL OFL 1.1 in `OFL.txt`, which ships in the release zip and
  carries every upstream copyright line; the MIT `LICENSE` now covers only the build code
* Built fonts carry the Noto copyright line in their name table alongside FiraCode's
* Downloads pinned by sha256 in `build.py` and verified before use, cached copies included
* `scripts/verify_fonts.py` smoke tests the build, and CI fails on a bad one
* Fixed the CI download cache never refreshing, so version bumps re-downloaded every run
* Build fails instead of releasing a fontless zip when the patcher produces nothing
* Pinned the CI runner to ubuntu-24.04, since fontforge draws the outlines
* Versions are SemVer from the `VERSION` file; a release is only cut when it is bumped, and
  a published tag is never moved

## v6.2+v3.5.1+v2.007

* Merge [Noto Sans Devanagari v2.007](https://github.com/notofonts/devanagari/releases/tag/NotoSansDevanagari-v2.007)
  into every variant (U+0900-097F, Devanagari Extended, Vedic Extensions, dotted circle, ZWNJ/ZWJ, rupee)
  with full dev2 shaping; FiraCode vertical metrics unchanged
* Version tag now `v<FiraCode>+<Nerd Fonts>+<Noto Sans Devanagari>`
* Bump nerd fonts to v3.5.1

## v6.2+v3.2.1

* Bump nerd fonts to v3.2.1
* Bump gh actions

## v6.2+v3.1.1

* Bump nerd fonts to v3.1.1

## v6.2+v3.0.2

**Initial release**

Using [FirCode v6.2](https://github.com/tonsky/FiraCode/releases/6.2)
and [Nerd Fonts v3.0.2](https://github.com/ryanoasis/nerd-fonts/releases/v3.0.2)

Patches:

1. Tweaks to characters `i` and `l`
2. Swap glyphs within Fire Code font variants:
    - `a -> a.cv01`
    - `g -> g.cv02`
    - `r -> r.ss01`
    - `3 -> three.cv14`
    - `$ -> dollar.ss04`
    - `% -> percent.cv18`
    - `{ -> braceleft.cv29`
    - `} -> braceright.cv29`
    - `| -> bar.cv30`
3. Nerd Fonts complete
