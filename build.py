#!/usr/bin/env python3
import logging
import os

from generator import generate

versions = {
    'fira_code': '6.2',
    'nerd_font_patcher': 'v3.1.1',
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
    generate(fira_code=versions['fira_code'], nerd_font_patcher=versions['nerd_font_patcher'])
    if 'CI' not in os.environ or os.environ['CI'] != 'true' or 'GITHUB_OUTPUT' not in os.environ:
        return
    version = 'v{}+{}\n'.format(versions['fira_code'], versions['nerd_font_patcher'])
    logging.info('Writing version={} github output', version)
    with open(os.environ['GITHUB_OUTPUT'], 'w') as file:
        file.write('version={}\n'.format(version))


if __name__ == "__main__":
    __dir__ = os.path.dirname(os.path.abspath(__file__))
    main()
