from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger,swag_from
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
import logging
from config import config,appinsightKey


db = SQLAlchemy()
format_str = '%(asctime)s - %(levelname)-8s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(format_str, date_format)
logger = logging.getLogger("globallogger")

def create_app(config_name):    
    app = Flask(__name__)
    handler = AzureLogHandler(connection_string=f'InstrumentationKey={appinsightKey}')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    middleware = FlaskMiddleware(app,exporter=AzureExporter(connection_string=f'InstrumentationKey={appinsightKey}'),sampler=ProbabilitySampler(rate=1.0))    
    Swagger(app)
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)
    db.init_app(app)
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from app.api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/v1')
    return app