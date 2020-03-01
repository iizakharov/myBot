#  log = logging.getLogger('app.' + __name__)
#
# logging.basicConfig(
#     filename="app.log",
#     format="%(levelname)-10s %(asctime)s %(message)s",
#     level=logging.INFO
# )

import logging
import os
import sys


# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s - %(message)s")

# Создаем файловый обработчик логирования (можно задать кодировку):
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "muBot.log")

steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(formatter)
steam.setLevel(logging.ERROR)
log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(formatter)

logger = logging.getLogger('muBot')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования')