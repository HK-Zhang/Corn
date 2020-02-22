import os

basedir = os.path.abspath(os.path.dirname(__file__))

class config:    
    SECRET_KEY = os.environ.get('SECRET_KEY') or """S8LApqTclxj9lfVB7HJP
KJxI2Wnh3kST1Fux9hms
P3i62M8S2mjis96sz0h3
REWiBG0XGX5crKVhvccn
lBra0dBP4yWjgB1F0IWb
uBLBFjCCzldiUnOGsmir
V5XmJf1GRBhWc1SOtQMr
5IiAofvp3sf47f5w0ZAa
KWHkMEWm9BNEC6ssa3gA
CmSwywTaWjfUm1DHzHgx
4iYWXXvcm9ExGurpCtP6
SYJP4GZVdQ3vj9O25ED2"""
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(config):    
    DEBUG = True    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev.db')

class TestingConfig(config):    
    TESTING = True    
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test')

class ProductionConfig(config):    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {    
    'development': DevelopmentConfig,    
    'testing': TestingConfig,    
    'production': ProductionConfig,    
    'default': DevelopmentConfig
}

# to be replaced with real app insight key
appinsightKey='000000-00000-000000-0000000'