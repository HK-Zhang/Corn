from flask import Blueprint, jsonify
import logging
import uuid

cbp = Blueprint('common', __name__)
logger = logging.getLogger("globallogger")

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@cbp.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    error_code = str(uuid.uuid1())
    properties = {'custom_dimensions': {'error_code': error_code}}
    logger.exception('Captured an exception.', extra=properties)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    response.headers["error_code"] = error_code
    return response