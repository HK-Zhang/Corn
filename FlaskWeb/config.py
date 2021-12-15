import os
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

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
appinsightKey='a21ddd3c-22e4-4b73-a3e9-1cc93adde3fb'

apiversion='0.87'

AZURE_CLIENT_ID = "cd9f0f18-ee13-4327-b67b-7776c8ae8961"
AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
AZURE_TENANT_ID = "adf10e2b-b6e9-41d6-be2f-c12bb566019c"
KEY_VAULT_NAME = "kvNdtAiWewb"

global sas
sas = ""


def set_sas(val):
    global sas
    sas = val


def get_sas():
    global sas
    if sas == "":
        load_config()
    return sas


def load_config():
    credential = ClientSecretCredential(AZURE_TENANT_ID, AZURE_CLIENT_ID,
                                        AZURE_CLIENT_SECRET)
    KVUri = "https://" + KEY_VAULT_NAME + ".vault.azure.net"
    client = SecretClient(vault_url=KVUri, credential=credential)
    retrieved_secret = client.get_secret("blobSasToken")
    set_sas(retrieved_secret.value)