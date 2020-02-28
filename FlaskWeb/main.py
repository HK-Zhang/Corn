from flask import url_for
from app import create_app

if __name__ == '__main__':
    app = create_app('default')
    app.debug = False
    app.run(host='localhost', port=5000)
    with app.test_request_context('/'):
        print(url_for('api.get_todos'))