import os
basedir = os.path.abspath(os.path.dirname(__file__))


class MainConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(MainConfig):
    DEBUG = True


class TestingConfig(MainConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(MainConfig):
    DEBUG = False


app_config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
