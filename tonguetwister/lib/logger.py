import logging
import sys

from tonguetwister.lib.helper import grouper


class LastPartFilter(logging.Filter):
    def filter(self, record):
        record.name_last = record.name.rsplit('.', 1)[-1]
        return True


def setup_logger(log_level=None):
    if log_level is None:
        log_level = logging.DEBUG

    formatter = logging.Formatter(
        '%(name_last)s [%(levelname)s] %(message)s'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(formatter)
    handler.addFilter(LastPartFilter())

    logger = logging.getLogger('tonguetwister')
    logger.setLevel(log_level)
    logger.addHandler(handler)


def log_expected_trailing_bytes(logger, _bytes, prefix=''):
    logger.info(
        f'{f"{prefix}: " if len(prefix) > 0 else ""}'
        f'Trailing bytes [{grouper(_bytes, 2)}] found. Probably nothing to worry about.'
    )
