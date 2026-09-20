#!/usr/bin/env python3
import logging
import os

from generator import generate

# Upstream releases, pinned by version and by the sha256 of the archive that
# version served. The glyphs end up in a font people install system wide, so a
# swapped release asset has to fail the build instead of shipping.
# Bumping a version means replacing its sha256 here, and updating the patcher
# version named in OFL.txt and README.md.
sources = {
    'fira_code': {
        'version': '6.2',
        'sha256': '0949915ba8eb24d89fd93d10a7ff623f42830d7c5ffc3ecbf960e4ecad3e3e79',
    },
    'nerd_font_patcher': {
        'version': 'v3.5.1',
        'sha256': '42bcb32145499a35732274c7fc48deb434ad0d2e0e118f98527c1479c6fa251a',
    },
    'noto_devanagari': {
        'version': 'v2.007',
        'sha256': '820c7da45b1e63562cb41c0a8cac5d9a4202312043a3a040ed1325857ef469b1',
    },
}


class LogFormatter(logging.Formatter):
    grey = '\x1b[30;1m'
    reset = '\x1b[0m'
    log_format = '{grey}%(levelname)-8s | %(asctime)s |{lvl} %(message)s{reset}'

    FORMATS = {
        logging.DEBUG: log_format.format(grey=grey, lvl=grey, reset=reset),
        logging.INFO: log_format.format(grey=grey, lvl='\x1b[36;20m', reset=reset),
        logging.WARNING: log_format.format(grey=grey, lvl='\x1b[33;20m', reset=reset),
        logging.ERROR: log_format.format(grey=grey, lvl='\x1b[31;20m', reset=reset),
        logging.CRITICAL: log_format.format(grey=grey, lvl='\x1b[31;1m', reset=reset),
    }

    def format(self, r): return logging.Formatter(fmt=self.FORMATS.get(r.levelno), datefmt='%H:%M:%S').format(r)


def main():
    ch = logging.StreamHandler()
    ch.setFormatter(LogFormatter())
    logging.basicConfig(level=logging.DEBUG, handlers=[ch])
    generate(fira_code=sources['fira_code'], nerd_font_patcher=sources['nerd_font_patcher'],
             noto_devanagari=sources['noto_devanagari'])
    if 'CI' not in os.environ or os.environ['CI'] != 'true' or 'GITHUB_OUTPUT' not in os.environ:
        return
    version = 'v{}+{}+{}'.format(sources['fira_code']['version'], sources['nerd_font_patcher']['version'],
                                 sources['noto_devanagari']['version'])
    logging.info('Writing version=%s github output', version)
    # Appended: every step of the job shares this file, opening it 'w' drops
    # the outputs the earlier ones wrote.
    with open(os.environ['GITHUB_OUTPUT'], 'a') as file:
        file.write('version={}\n'.format(version))


if __name__ == "__main__":
    __dir__ = os.path.dirname(os.path.abspath(__file__))
    main()
