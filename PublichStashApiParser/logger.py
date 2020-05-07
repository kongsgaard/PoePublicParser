import logging

def get_logger(level=logging.INFO):
    logger = logging.getLogger('PoePublicParser')
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s | %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(level)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger