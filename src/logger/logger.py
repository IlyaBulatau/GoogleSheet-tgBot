import logging
from logging.handlers import SMTPHandler

from config import config

logger = logging.getLogger()
logger.setLevel('DEBUG')
formatter = logging.Formatter(fmt='{asctime} - {levelname} - {message}', style='{')

file_handler = logging.FileHandler('log.log', mode='a', encoding='utf-8')
file_handler.setLevel('DEBUG')
file_handler.setFormatter(formatter)

email_handler = SMTPHandler(
    mailhost=('smtp.yandex.ru', 587),
    fromaddr=config.EMAIL_ADRESS,
    toaddrs=config.EMAIL_ADRESS,
    subject='Bot logging',
    credentials=(config.EMAIL_ADRESS, config.EMAIL_PASSWORD),
    secure=(),
)
email_handler.setLevel('WARNING')
email_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(email_handler)
logger.addHandler(console_handler)
