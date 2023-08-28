# firacode-nfc-tweaked

Fira Code font tweaked and patched with Nerd Fonts Compete

## Generate

### Requirements

- [Python 3]
- [fontforge]

To generate the patched font, run:

```shell
./build.py
```

### What build.py does

The build.py performs the following steps:

1. Download
   1. Nerd Fonts patched from [Nerd Fonts releases] [^1]
   2. FiraCode from [FiraCode release] [^2]
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
3. Copy patched font variants to `dist` directory

## Font variants

Files in FiraCodeNerdFont.zip from [latest] release:

| File Name                        | Font Name              | Family Name        | Name for Humans                 |
|:---------------------------------|:-----------------------|:-------------------|:--------------------------------|
| FiraCodeNerdFont-Regular.ttf     | FiraCodeNF-Regular     | FiraCode Nerd Font | FiraCode Nerd Font Regular      |
| FiraCodeNerdFont-Bold.ttf        | FiraCodeNF-Bold        | FiraCode Nerd Font | FiraCode Nerd Font Bold         |
| FiraCodeNerdFont-Oblique.ttf     | FiraCodeNF-Oblique     | FiraCode Nerd Font | FiraCode Nerd Font Oblique      |
| FiraCodeNerdFont-BoldOblique.ttf | FiraCodeNF-BoldOblique | FiraCode Nerd Font | FiraCode Nerd Font Bold Oblique |

## Why?

I like the Fira Code font, but

- I wanted to use the style variants as default instead of the default variants
- I hate all default `i` and `l` variants
- Nerd Font patched fonts
  - Don't have the complete set of glyphs
  - Are monospaced while many term emulators (including iterm2) support non-monospaced fonts
- I don't want to manually patch the font every time a new version of Fira Code or NerdFont is released

## Support

I have not tested each character individually, but it should work.
This project is for my personal use,
I will try to fix any issues reported, but I cannot guarantee any timelines or if I fix it at all.

## Changelog

See [changelog.md]

## License

This repository is licensed under the MIT License;
Some of the files committed and used during the build process in this repository follow the licenses from their source location,
Which are updated in the [LICENSE] on the best effort basis.


[^1]: https://github.com/ryanoasis/nerd-fonts/blob/v3.0.2/LICENSE
[^2]: https://github.com/tonsky/FiraCode/blob/6.2/LICENSE

[Python 3]: https://www.python.org
[fontforge]: https://fontforge.org
[Nerd Fonts releases]: https://github.com/ryanoasis/nerd-fonts/releases
[FiraCode releases]: https://github.com/tonsky/FiraCode/releases
[patches]: ./patches
[latest]: https://github.com/yogeshlonkar/firacode-nfc-tweaked/releases/latest
[changelog.md]: ./changelog.md
[LICENSE]: ./LICENSE
