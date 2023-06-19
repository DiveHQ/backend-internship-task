from api import db, app

if __name__ == '__main__':
    with app.app_context():
        app.config.from_pyfile('config.py')
        db.create_all()
