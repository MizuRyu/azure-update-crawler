import logging

def get_logger(name=None, level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        # ハンドラの作成
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        logger.setLevel(level)
    return logger