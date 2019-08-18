from app import create_app

if __name__ == '__main__':
    app = create_app('default')
    app.debug = False
    app.run(host='localhost', port=5000)