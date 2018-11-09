import os
basedir = os.path.abspath(os.path.dirname(__file__))


class MainConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(MainConfig):
    ENV = 'development'
    DEBUG = True


class TestingConfig(MainConfig):
    ENV = 'testing'
    DATABASE = 'storemanagerdb_test'
    DEBUG = True
    TESTING = True


class ProductionConfig(MainConfig):
    ENV = 'production'

app_config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
