# firacode-nfc-tweaked

Fira Code font tweaked, patched with Nerd Fonts Complete, and merged with Noto Sans Devanagari

## Generate

### Requirements

- [Python 3]
- [fontforge]
- `pip install -r requirements.txt` (fontTools for the Devanagari merge and the verifier)

To generate the patched font, run:

```shell
./build.py
```

### What build.py does

The build.py performs the following steps:

1. Download, each pinned to a version and a sha256 in `build.py` and verified before use,
   cached copies included
   1. Nerd Fonts font-patcher from [Nerd Fonts releases] [^1]
   2. FiraCode from [FiraCode releases] [^2]
   3. Noto Sans Devanagari from [Noto Sans Devanagari] [^3]
2. Patch Fira Code font variants with
   1. Tweaks to characters `i` and `l`. see sfd files in [patches] for details
   2. Swap glyphs within Fire Code font variants to become default instead of style variants

      | From ->  To              |
      |:-------------------------|
      | `a` -> `a.cv01`          |
      | `g` -> `g.cv02`          |
      | `r` -> `r.ss01`          |
      | `3` -> `three.cv14`      |
      | `$` -> `dollar.ss04`     |
      | `%` -> `percent.cv18`    |
      | `{` -> `braceleft.cv29`  |
      | `}` -> `braceright.cv29` |
      | `\|` -> `bar.cv30`       |
   3. Nerd Fonts complete with `--careful`, `--complete` arguments
   4. Devanagari from [Noto Sans Devanagari] [^3]: the variable font is instanced at
      each FiraCode weight (Light 300 … Bold 700, Retina 450), subset to the Devanagari
      blocks, rescaled to FiraCode's em, and merged with `fontTools.merge`. FiraCode's
      vertical metrics are kept so line height does not change. See
      `generator/devanagari.py` for why fontTools (not fontforge) and why the
      Devanagari glyphs keep their proportional advances. The Noto copyright line is
      added to the font's name table next to FiraCode's, as the OFL asks.
3. Copy patched font variants to `dist` directory

Then `./scripts/verify_fonts.py dist downloads` checks the result, and CI fails the build
if it does not pass: all six weights present, Devanagari and Nerd Font icons reachable,
`dev2` shaping in GSUB, the stylistic swaps and the `i`/`l` tweaks actually applied, one
line height across weights, both copyright lines in the name table.

## Font variants

Six weights, one per FiraCode weight, in FiraCodeNerdFont.zip from the [latest] release.
They share the family name `FiraCode Nerd Font`; the weight is in the subfamily, as the
patcher sets it. There are no italics or obliques, because FiraCode ships none.

| File Name                      | Weight   | Devanagari instance (`wght`) |
|:-------------------------------|:---------|:-----------------------------|
| FiraCodeNerdFont-Light.ttf     | Light    | 300                          |
| FiraCodeNerdFont-Regular.ttf   | Regular  | 400                          |
| FiraCodeNerdFont-Retina.ttf    | Retina   | 450                          |
| FiraCodeNerdFont-Medium.ttf    | Medium   | 500                          |
| FiraCodeNerdFont-SemiBold.ttf  | SemiBold | 600                          |
| FiraCodeNerdFont-Bold.ttf      | Bold     | 700                          |

Each file carries, on top of stock FiraCode: the `i`/`l` tweaks, the stylistic variants
swapped in as defaults, the complete Nerd Fonts icon set, and Noto Sans Devanagari with
full `dev2` shaping (Devanagari, Devanagari Extended, Vedic Extensions, ZWNJ/ZWJ, rupee).
The zip also holds `OFL.txt` and `changelog.md`.

## Why?

I like the Fira Code font, but

- I wanted to use the style variants as default instead of the default variant
- I hate all default `i` and `l` variants
- Nerd Font patched fonts
  - Don't have the complete set of glyphs
  - Are monospaced while many term emulators (including iterm2) support non-monospaced fonts
- I don't want to manually patch the font every time a new version of Fira Code or NerdFont is released
- I write Marathi/Hindi mixed with English in the terminal; one font with correct Devanagari shaping beats
  per-terminal fallback maps, and works the same on Linux where Kohinoor does not exist

## Support

I have not tested each character individually, but it should work.
This project is for my personal use,
I will try to fix any issues reported, but I cannot guarantee any timelines or if I will fix it at all.

## Changelog

See [changelog.md]

## License

Two licenses, split by what the file is:

- **Fonts: [SIL Open Font License 1.1][OFL.txt].** The built `FiraCodeNerdFont-*.ttf` and the glyph sources in
  [patches] are Modified Versions of Fira Code, Noto Sans Devanagari and the Nerd Fonts icon sets, and the OFL
  requires derivatives to stay under the OFL. [OFL.txt] carries every upstream copyright line and ships in the
  release zip next to the fonts.
- **Build code: [MIT][LICENSE].** `build.py`, `generator/` and the CI workflows.

No upstream Reserved Font Name is used by the family name `FiraCode Nerd Font`: Fira Code 6.2 [^2],
Noto Sans Devanagari v2.007 [^3] and Nerd Fonts v3.5.1 [^1] declare none; the Pomicons icon set reserves
"Pomicons" only.


[^1]: https://github.com/ryanoasis/nerd-fonts/blob/v3.5.1/LICENSE
[^2]: https://github.com/tonsky/FiraCode/blob/6.2/LICENSE
[^3]: https://github.com/notofonts/devanagari/blob/main/OFL.txt

[Python 3]: https://www.python.org
[fontforge]: https://fontforge.org
[Nerd Fonts releases]: https://github.com/ryanoasis/nerd-fonts/releases
[FiraCode releases]: https://github.com/tonsky/FiraCode/releases
[Noto Sans Devanagari]: https://github.com/notofonts/devanagari/releases
[patches]: ./patches
[latest]: https://github.com/yogeshlonkar/firacode-nfc-tweaked/releases/latest
[changelog.md]: ./changelog.md
[LICENSE]: ./LICENSE
[OFL.txt]: ./OFL.txt
