from environs import Env


class BaseConfig:
    env = Env()
    env.read_env()

    TOKEN = env('TOKEN')
    BOT_EMAIL=env('BOT_EMAIL')
    BOT_ID = env('BOT_ID')

    _status = 'dev'

    EMAIL_ADRESS = env('EMAIL_ADRESS')
    EMAIL_PASSWORD = env('EMAIL_PASSWORD')

    ADMIN_ID = env('ADMIN_ID')

class DevelopmentConfig(BaseConfig):
    
    DB_NAME = BaseConfig.env('DB_NAME_DEV')
    DB_LOGIN = BaseConfig.env('DB_LOGIN_DEV')
    DB_PASSWORD = BaseConfig.env('DB_pASSWORD_DEV')
    DB_HOST = BaseConfig.env('DB_HOST_DEV')
    DB_URL = f'postgresql+psycopg2://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    REDIS_HOST = BaseConfig.env('REDIS_HOST_DEV')

class ProductConfig(BaseConfig):
    ...

config = DevelopmentConfig if BaseConfig._status == 'dev' else ProductConfig