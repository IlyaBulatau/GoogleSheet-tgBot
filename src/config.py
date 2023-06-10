from environs import Env


class BaseConfig:
    env = Env()
    env.read_env()

    TOKEN = env('TOKEN')