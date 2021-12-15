from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger,swag_from
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
import logging
from config import config,appinsightKey,apiversion,AZURE_CLIENT_ID,AZURE_CLIENT_SECRET,AZURE_TENANT_ID,KEY_VAULT_NAME,load_config
import uuid
import zipfile
import os
import sys
import socket

# zip = zipfile.ZipFile("C:\\Users\\yxzhk\\Workspace\\x.zip", 'w', zipfile.ZIP_DEFLATED )
# for filename in os.listdir("C:\\Users\\yxzhk\\Workspace\\result"):
#     zip.write(os.path.join("C:\\Users\\yxzhk\\Workspace\\result", filename),filename)
# zip.close()

db = SQLAlchemy()
hostname=socket.gethostname()
format_str = f'{apiversion}@{hostname} says:'+'%(asctime)s - %(levelname)-8s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter(format_str, date_format)
logger = logging.getLogger()



def create_app(config_name):    
    app = Flask(__name__)
    handler = AzureLogHandler(connection_string=f'InstrumentationKey={appinsightKey}')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    try:
        # load_config()
        middleware = FlaskMiddleware(app,exporter=AzureExporter(connection_string=f'InstrumentationKey={appinsightKey}'),sampler=ProbabilitySampler(rate=1.0))    
        Swagger(app)
        app.config.from_object(config[config_name])    
        config[config_name].init_app(app)
        db.init_app(app)
        from app.common import cbp as common_blueprint
        app.register_blueprint(common_blueprint)
        from app.main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        from app.api_1_0 import api as api_1_0_blueprint
        app.register_blueprint(api_1_0_blueprint, url_prefix='/v1')
        logging.info('App Started.')
        # healthy check
        with app.test_request_context('/'):
             with app.test_client() as c:
                 try:
                     r = c.post(url_for('api.create_task'),json={'email': 'flask@example.com', 'title': 'secret'})
                     if r.status_code==200:
                         print("pass")
                     pass
                 except Exception:
                     pass
        return app
    except Exception:
        error_code = str(uuid.uuid1())
        properties = {'custom_dimensions': {'error_code': error_code}}
        logging.exception('Captured an exception.', extra=properties)
        return f'error_code:{error_code}',500,{"error_code": "abcs"}
