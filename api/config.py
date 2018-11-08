import os
basedir = os.path.abspath(os.path.dirname(__file__))


class MainConfig(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(MainConfig):
    ENV = 'development'
    DATABASE = 'storemanagerdb'
    USER = 'postgres'
    PASSWORD = 'challenge3'
    DEBUG = True


class TestingConfig(MainConfig):
    ENV = 'testing'
    DATABASE = 'storemanagerdb_test'
    DEBUG = True
    TESTING = True


class ProductionConfig(MainConfig):
    ENV = 'production'
    HOST = 'ec2-54-83-38-174.compute-1.amazonaws.com'
    DATABASE = 'd4eo92qumfels6'
    USER = 'rydoowkieaxjhf'
    PASSWORD = '451025a5501925f1a9c2dad02c65fdd1122b1cc2cfa8d94d021d86e059f74b51'


app_config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)
