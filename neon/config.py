class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///neon.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # will become default in the future


class ProductionConfig(Config):
    DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
