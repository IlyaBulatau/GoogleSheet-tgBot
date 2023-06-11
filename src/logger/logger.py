import logging
from logging.handlers import SMTPHandler


logger = logging.getLogger()
logger.setLevel('DEBUG')
formatter = logging.Formatter(fmt='{asctime}|{levelname}|{message}', style='{')

file_handler = logging.FileHandler('log.log', mode='a', encoding='utf-8')
file_handler.setLevel('DEBUG')
file_handler.setFormatter(formatter)

email_handler = SMTPHandler(
    mailhost=('smtp.gmail.com', 587),
    fromaddr='ilyabulatau@gmail.com',
    toaddrs='ilyabulatau@gmail.com',
    subject='Bot logging',
    credentials=('ilyabulatau@gmail.com', 'vupufa14'),
    secure=(),
)
email_handler.setLevel('WARNING')
email_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# logger.addHandler(email_handler)
